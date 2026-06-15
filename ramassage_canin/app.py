import os
import requests
from flask import Flask, render_template, request
from database import db, Demande

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ramassage_canin.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "devkey")

db.init_app(app)

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

SECTEUR_SERVICE = [
    "saint-pierre", "st-pierre", "saint-jean", "saint-damase",
    "manseau", "saint-alphonse", "saint-frédéric",
    "mélancon", "mélançon", "marchand", "bruno",
    "cockburn", "surprenant", "rajotte", "savard",
    "faucher", "désilet", "desilet", "saint-antoine",
    "saint-marc", "saint-ambroise", "villeneuve",
    "saint-paul", "saint-lucien", "saint-marcel",
    "saint-albert", "sylvain", "saint-alfred",
    "turcotte", "du drapeau", "notre-dame",
    "ringuet", "pelletier", "ferland", "chassé",
    "mathieu", "6e avenue", "7e avenue",
    "8e avenue", "9e avenue"
]


def envoyer_discord(message):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": message})


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        nom = request.form.get("nom")
        adresse = request.form.get("adresse", "").lower()
        telephone = request.form.get("telephone")
        frequence = request.form.get("frequence")
        chiens = request.form.get("chiens")
        acces = request.form.get("acces")
        moment = request.form.get("moment")
        notes = request.form.get("notes")

        # vérification secteur
        if not any(r in adresse for r in SECTEUR_SERVICE):
            return "Hors zone de service."

        # sauvegarde DB
        demande = Demande(
            nom=nom,
            adresse=adresse,
            telephone=telephone,
            frequence=frequence,
            chiens=chiens,
            acces=acces,
            moment=moment,
            notes=notes
        )

        db.session.add(demande)
        db.session.commit()

        # prix simple
        prix = 25
        try:
            c = int(chiens)
            if c == 2:
                prix = 35
            elif c >= 3:
                prix = 45
        except:
            pass

        # message discord
        message = (
            "🐶 NOUVELLE DEMANDE RAMASSAGE CANIN\n\n"
            f"Nom: {nom}\n"
            f"Adresse: {adresse}\n"
            f"Téléphone: {telephone}\n"
            f"Chiens: {chiens}\n"
            f"Fréquence: {frequence}\n"
            f"Accès: {acces}\n"
            f"Moment: {moment}\n"
            f"Prix: {prix}$\n"
            f"Notes: {notes}"
        )

        envoyer_discord(message)

        return f"Demande envoyée. Prix estimé : {prix}$"

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=8080)