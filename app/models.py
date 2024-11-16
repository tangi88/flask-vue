from datetime import datetime
from app import db


class Products(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    active = db.Column(db.Boolean)
    interval = db.Column(db.Integer)
    url_1 = db.Column(db.Text)
    url_2 = db.Column(db.Text)
    url_3 = db.Column(db.Text)
    url_4 = db.Column(db.Text)
    url_5 = db.Column(db.Text)

    prices = db.relationship('Prices', backref='product', passive_deletes=True, cascade="all,delete,delete-orphan")
    errors = db.relationship('Errors', backref='product', passive_deletes=True, cascade="all,delete,delete-orphan")

    def __repr__(self):
        return '<Product {}>'.format(self.name)

    def get_url(self, i):
        name_url = f'url_{i}'
        url = ''
        if name_url in self.__dict__:
            url = getattr(self, name_url)

        return url


class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    price = db.Column(db.Float)
    product_id = db.Column(db.String(100), db.ForeignKey('products.id', ondelete='CASCADE'))


class Errors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    text = db.Column(db.Text)
    product_id = db.Column(db.String(100), db.ForeignKey('products.id', ondelete='CASCADE'))

