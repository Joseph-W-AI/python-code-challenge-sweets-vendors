from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class Vendor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

  vendor_sweets = db.relationship('VendorSweet', backref='vendor')

class VendorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'created_at', 'updated_at')
    

class Sweet(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

  vendor_sweets = db.relationship('VendorSweet', backref='sweet')

class SweetSchema(ma.Schema):
  class Meta: 
    fields = ('id', 'name', 'created_at', 'updated_at')


class VendorSweet(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  price = db.Column(db.Integer, nullable=False)
  vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
  sweet_id = db.Column(db.Integer, db.ForeignKey('sweet.id'), nullable=False)
  
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

  @validates('price')
  def validate_price(self, key, price):
    if price is None:
      raise AssertionError('No price provided')
    if price < 0:
      raise AssertionError('Price cannot be a negative number')
    return price

class VendorSweetSchema(ma.Schema):
  class Meta:
    fields = ('id', 'price', 'vendor_id', 'sweet_id', 'created_at', 'updated_at')

