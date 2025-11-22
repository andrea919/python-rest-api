from db import db

class StoreModel(db.Model):
    # Create a table called items
    __tablename__ = "stores"     

    # Define the columns in this table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # See associates items to the store
    items = db.relationship("ItemModel", 
                            back_populates="store", 
                            lazy="dynamic", 
                            cascade="all, delete"   # Delete store = delete items
                            )
    # Lazy = "dynamic" is needed not to fetch several things together
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
