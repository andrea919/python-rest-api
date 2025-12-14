import os
import requests
import jinja2

from dotenv import load_dotenv

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

load_dotenv()


def send_simple_message(to, subject, body, html):
    domain = os.getenv("MAILGUN_DOMAIN")
    key = os.getenv("MAILGUN_API_KEY")
    if not domain or not key:
        print("❌ Mailgun not configured: MAILGUN_DOMAIN or MAILGUN_API_KEY missing")
        return
    
    print(f"📧 Sending email via Mailgun domain={domain} to={to}")

    response = requests.post(
  		f"https://api.mailgun.net/v3/{domain}/messages",
  		auth=("api", key),
  		data={"from": f"Andrea: <mailgun@{domain}>",
			"to": [to],
  			"subject": subject,
  			"text": body, 
            "html":html
            })
            

    try:
        response.raise_for_status()
    except Exception as e:
        print("Error sending email: ", e)

    return response

def send_user_registration_email(email, username):
    html = render_template("email/action.html", username=username)
    return send_simple_message(
        email, 
        "Successfully signed up", 
        f"Hi {username}, thanks for registering to the Stores Rest API.",
        # code from action.html
        html
    )