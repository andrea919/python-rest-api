from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

def validate_same_store(item, tag):
    if item.store_id != tag.store_id:
        abort(400, message="Item and tag do not belong to the same store.")
        # return False sarebbe inutile perche abort già interrompe la funzione
    

blp = Blueprint("Tags", "tags", description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(int(store_id))
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # Check unique name in that store - double control
        store_id = int(store_id)
        if TagModel.query.filter(TagModel.store_id == store_id, 
                              TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, 
                  message=str(e)
                )

        return tag 
    
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItems(MethodView):
    @blp.response(201, TagAndItemSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        validate_same_store(item, tag)
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag
        
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        validate_same_store(item, tag)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message":"Item removed from tag.", "item":item, "tag":tag}

    
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202, description="Deletes a tag if no item is tagged with it", example="Tag deleted.")
    @blp.response(400, description="Returned if the tag is assigned to one or more items. Tags is not deleted")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        if len(tag.items) == 0:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted."}
        # else:
        abort(400, message="Could not delete tag, Make sure tag is not associated with any items.")