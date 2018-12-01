from db import db


class StoreModel(db.Model):
    # sqlalchemy set up
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # need lazy for speed
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "name": self.name,
            # user .all to retrieve from table cause lazy
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # both work
        # return ItemModel.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
