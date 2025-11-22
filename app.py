import os
import secrets 
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db

# Import ALL models 
from models.store import StoreModel
from models.item import ItemModel  
from models.tag import TagModel
from models.item_tags import ItemTags
from models.user import UserModel
from models.revoked_token import RevokedToken

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # Register blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)
    
    # JWT Configuration
    # Set your JWT secret key here or load it from an environment variable
    app.config["JWT_SECRET_KEY"] = ""
    jwt = JWTManager(app)

    #  JWT callbacks...
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        revoked = RevokedToken.query.filter_by(jti=jwt_payload["jti"]).first()
        return revoked is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "description": "The token is not fresh.",    
                "error": "fresh_token_required"            
            }
        ), 401


    # Add additional functions when access token is created
    # For example this function assign admin to user with id = 1 
    # The first user ever created will have admin permissions
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if int(identity) == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(
            {
                "description": "Signature verification failed.", 
                "error": "invalid_token",
            }
        ), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {
                "description": "Request does not contain an access token.", 
                "error": "authorization_required",
            }
        ), 401
    
    with app.app_context():
        db.create_all()

    return app