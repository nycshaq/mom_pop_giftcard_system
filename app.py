from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")



db = SQLAlchemy(app)

class GiftCard(db.Model):
    __tablename__ = 'giftcards'  # Specify the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    giftcard_number = db.Column(db.BigInteger, unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now())
    last_used_time = db.Column(db.TIMESTAMP(timezone=True), nullable=True)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/giftcard/<int:giftcard_number>', methods=['GET'])
def get_giftcard(giftcard_number):
    giftcard = GiftCard.query.filter_by(giftcard_number=giftcard_number).first()
    if giftcard:
        return jsonify({
            'id': giftcard.id,
            'giftcard_number': giftcard.giftcard_number,
            'amount': str(giftcard.amount),
            'created_time': giftcard.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_used_time': giftcard.last_used_time.strftime('%Y-%m-%d %H:%M:%S') if giftcard.last_used_time else None
        })
    else:
        return jsonify({'message': 'Giftcard not found'}), 404

@app.route('/giftcards', methods=['GET'])
def get_giftcards():
    sort_by = request.args.get('sort_by', 'amount')  # Default sorting by amount
    if sort_by == 'amount':
        giftcards = GiftCard.query.order_by(GiftCard.amount.desc()).all()
    elif sort_by == 'last_used':
        giftcards = GiftCard.query.order_by(GiftCard.last_used_time.desc()).all()
    else:
        return jsonify({'message': 'Invalid sort_by parameter. Use "amount" or "last_used".'}), 400

    result = []
    for giftcard in giftcards:
        result.append({
            'id': giftcard.id,
            'giftcard_number': giftcard.giftcard_number,
            'amount': str(giftcard.amount),
            'created_time': giftcard.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_used_time': giftcard.last_used_time.strftime('%Y-%m-%d %H:%M:%S') if giftcard.last_used_time else None
        })
    return jsonify(result)

@app.route('/giftcard', methods=['POST'])
def add_giftcard():
    data = request.json
    giftcard_number = data.get('giftcard_number')
    amount = data.get('amount', 0.00)

    if giftcard_number is None:
        return jsonify({'message': 'Giftcard number is required'}), 400

    if GiftCard.query.filter_by(giftcard_number=giftcard_number).first():
        return jsonify({'message': 'Giftcard already exists'}), 400

    giftcard = GiftCard(giftcard_number=giftcard_number, amount=amount)
    db.session.add(giftcard)
    db.session.commit()
    return jsonify({'message': 'Giftcard added successfully'}), 201

@app.route('/giftcard/<int:giftcard_number>', methods=['PUT'])
def update_giftcard(giftcard_number):
    data = request.json
    amount = data.get('amount')

    if amount is None:
        return jsonify({'message': 'Amount is required'}), 400

    giftcard = GiftCard.query.filter_by(giftcard_number=giftcard_number).first()
    if giftcard:
        giftcard.amount = amount
        db.session.commit()
        return jsonify({'message': 'Giftcard amount updated successfully'}), 200
    else:
        return jsonify({'message': 'Giftcard not found'}), 404

if __name__ == '__main__':
    # Code to run when this is the main program here
    app.run()