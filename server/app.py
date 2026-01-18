#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)


@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    if request.method == 'PATCH':
        if 'name' in request.form:
            bakery.name = request.form['name']
        db.session.commit()
        return make_response(jsonify(bakery.to_dict()), 200)

    return make_response(jsonify(bakery.to_dict()), 200)


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    baked_good = BakedGood(
        name=request.form['name'],
        price=request.form['price'],
        bakery_id=request.form['bakery_id']
    )

    db.session.add(baked_good)
    db.session.commit()

    return make_response(jsonify(baked_good.to_dict()), 201)


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if not baked_good:
        return make_response(jsonify({"error": "Baked good not found"}), 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response(jsonify({"message": "Baked good deleted"}), 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response(jsonify([bg.to_dict() for bg in baked_goods]), 200)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(jsonify(baked_good.to_dict()), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
