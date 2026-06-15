from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Demande(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(100))
    adresse = db.Column(db.String(255))

    telephone = db.Column(db.String(30))
    frequence = db.Column(db.String(50))

    chiens = db.Column(db.String(10))

    acces = db.Column(db.String(255))
    moment = db.Column(db.String(255))

    notes = db.Column(db.Text)