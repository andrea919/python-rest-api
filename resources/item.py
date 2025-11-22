from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema



# Blueprint divides APIs into multiple segments
blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()  
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Query attribute to retrieve from db by primary key
        item = ItemModel.query.get_or_404(item_id)
        return item
    

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(403, message="Admin privileges required.")  # 403 = forbidden
        
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message":"Item deleted."}

    @jwt_required()  
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        # If it exists, it will be updated
        if item: 
            item.price = item_data["price"]
            item.name = item_data["name"]

        # If it does not exist, it will be created
        # Has to be fixed or eliminated 
        # It does not create item 
        else:
            # Ensure that client is providing store_id
            if "store_id" not in item_data or item_data["store_id"] is None:
                abort(400, message="Item cannot be created. store_id is required.")
            item = ItemModel(id=item_id, **item_data)    

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()  
    @blp.response(200, ItemSchema(many=True)) # This will return a list of items 
    def get(self):
        return ItemModel.query.all()    # Go through every item
    
    @jwt_required(fresh=True)     # Request a JWT for creating an item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data): # second parameter will contain json 
        # item_data = request.get_json()

        item = ItemModel(**item_data)   # Passed as kw arguments

        try:
            db.session.add(item)    # Add multiple items
            db.session.commit()     # Saving to database
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        
        return item