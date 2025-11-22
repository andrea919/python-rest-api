import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema


# Blueprint divides APIs into multiple segments
blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        # Raise the error to communicate with the client
        if store.tags.count() != 0:
            abort(400, message="Cannot delete store with tags. Remove or reassign tags first.")
        
        db.session.delete(store)
        db.session.commit()
        
        return {"message":"Store deleted."}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):

        store = StoreModel(**store_data)   # Passed as kw arguments

        try:
            db.session.add(store)    # Add multiple items
            db.session.commit()     # Saving to database
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        
        return store