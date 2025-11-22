from db import db

class TagModel(db.Model):

    # Create a table called tags
    __tablename__ = "tags"     

    # Define the columns in this table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),  nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="item_tags", order_by="ItemModel.id")  # ordina per id
