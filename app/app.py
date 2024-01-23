#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Vendor, Sweet, VendorSweet, ma, VendorSchema, SweetSchema, VendorSweetSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the Sweets Vendor API!'

@app.route('/vendors')
def get_vendors():
  vendors = Vendor.query.all()
  vendor_schema = VendorSchema(many=True)
  return jsonify(vendor_schema.dump(vendors))

@app.route('/vendors/<int:id>')  
def get_vendor(id):
  vendor = Vendor.query.get(id)
  if vendor:
    vendor_schema = VendorSchema()
    return jsonify(vendor_schema.dump(vendor))
  else: 
    return jsonify({"error": "Vendor not found"}), 404

@app.route('/sweets')
def get_sweets():
  sweets = Sweet.query.all()
  sweet_schema = SweetSchema(many=True)
  return jsonify(sweet_schema.dump(sweets)) 

@app.route('/sweets/<int:sweet_id>')
def get_sweet(sweet_id):
  sweet = Sweet.query.get(sweet_id)
  if sweet:
    sweet_schema = SweetSchema()
    return jsonify(sweet_schema.dump(sweet))
  else:
    return jsonify({"error": "Sweet not found"}), 404
        
@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()
    price = data['price']
    vendor_id = data['vendor_id']
    sweet_id = data['sweet_id']

    try:
        vendor_sweet = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
        db.session.add(vendor_sweet)
        db.session.commit()

        vendor_sweet_schema = VendorSweetSchema()
        return jsonify(vendor_sweet_schema.dump(vendor_sweet))
    except AssertionError as exception_message:
        return jsonify(msg='Error: {}. '.format(exception_message)), 400

    
@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.get(id)
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({})
    else:
        return jsonify({"error": "Vendor sweet not found"}), 404

if __name__ == '__main__':
    app.run(port=5555)