from flask import request, jsonify, current_app as app
from app import db
from app.models import Book, Borrower
from datetime import datetime

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        serial_number=data['serial_number'],
        title=data['title'],
        author=data['author']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added"}), 201

@app.route('/books/<int:serial_number>', methods=['DELETE'])
def delete_book(serial_number):
    book = Book.query.get_or_404(serial_number)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'serial_number': book.serial_number,
        'title': book.title,
        'author': book.author,
        'is_borrowed': book.is_borrowed,
        'borrowed_by': {
            'id': book.borrower.id,
            'card_number': book.borrower.card_number,
            'first_name': book.borrower.first_name,
            'last_name': book.borrower.last_name
        } if book.borrower else None,
        'borrowed_date': book.borrowed_date
    } for book in books])

@app.route('/books/<int:serial_number>', methods=['PUT'])
def update_book(serial_number):
    data = request.get_json()
    book = Book.query.get_or_404(serial_number)
    book.is_borrowed = data['is_borrowed']
    if data['is_borrowed']:
        borrower = Borrower.query.filter_by(card_number=data['borrowed_by']).first()
        if not borrower:
            return jsonify({"message": "Borrower not found"}), 404
        book.borrowed_by = borrower.id
        if 'borrowed_date' in data and data['borrowed_date']:
            book.borrowed_date = datetime.strptime(data['borrowed_date'], '%Y-%m-%d').date()
    else:
        book.borrowed_by = None
        book.borrowed_date = None
    db.session.commit()
    return jsonify({"message": "Book status updated"}), 200

@app.route('/borrowers', methods=['POST'])
def add_borrower():
    data = request.get_json()
    new_borrower = Borrower(
        card_number=data['card_number'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    db.session.add(new_borrower)
    db.session.commit()
    return jsonify({"message": "Borrower added"}), 201

@app.route('/borrowers', methods=['GET'])
def get_borrowers():
    borrowers = Borrower.query.all()
    return jsonify([{
        'id': borrower.id,
        'card_number': borrower.card_number,
        'first_name': borrower.first_name,
        'last_name': borrower.last_name
    } for borrower in borrowers])
