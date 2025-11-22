FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 
CMD ["flask", "run", "--host", "0.0.0.0"]

# Every task represents a layer for the image
# Remember to run Docker desktop beforehand