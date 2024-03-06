from flask import Flask, request, make_response, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    if request.method == 'GET':
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return make_response(jsonify(bakeries), 200)
    elif request.method == 'POST':
        data = request.form
        name = data.get('name')
        if name:
            new_bakery = Bakery(name=name)
            db.session.add(new_bakery)
            db.session.commit()
            return make_response(jsonify(new_bakery.to_dict()), 201)
        else:
            return make_response(jsonify({'error': 'Name is required'}), 400)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    
    if request.method == 'GET':
        return make_response(jsonify(bakery.to_dict()), 200)
    elif request.method == 'PATCH':
        data = request.form
        name = data.get('name')
        if name:
            bakery.name = name
            db.session.commit()
            return make_response(jsonify(bakery.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Name is required'}), 400)
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = data.get('price')

    if not name or not price:
        return jsonify({'error': 'Name and price are required fields'}), 400

    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()

    return jsonify({'message': 'Baked good created successfully', 'id': new_baked_good.id}), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return make_response(jsonify({'error': 'Baked good not found'}), 404)
    
    db.session.delete(baked_good)
    db.session.commit()
    return make_response(jsonify({'message': 'Baked good deleted successfully'}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
