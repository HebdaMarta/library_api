from app import db
from datetime import date

class Borrower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(6), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='borrower', lazy=True)

class Book(db.Model):
    serial_number = db.Column(db.String(6), primary_key=True, unique=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)
    borrowed_by = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=True)
    borrowed_date = db.Column(db.Date, nullable=True)