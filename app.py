"""
IFRI_MentorLink - Version simplifiée (rattrapage)
Backend Flask : recherche de mentors compatibles sans authentification.
"""

import os
import re
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

# -------------------------------------------------------------------
# Configuration de la base de données
# -------------------------------------------------------------------
# Modifie cette variable d'environnement selon ta base (PostgreSQL ou MySQL).
# Exemples :
#   PostgreSQL : postgresql+psycopg2://user:password@localhost:5432/mentorlink
#   MySQL      : mysql+pymysql://user:password@localhost:3306/mentorlink
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+pg8000://postgres:postgres@localhost:5432/mentorlink"
)

engine = create_engine(DATABASE_URL)

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


# -------------------------------------------------------------------
# Fonctions utilitaires de matching
# -------------------------------------------------------------------
def parse_disponibilites(dispo_str):
    """
    Transforme "Lundi 14:00-16:00;Mercredi 10:00-12:00"
    en [{"jour": "lundi", "debut": time, "fin": time}, ...]
    """
    slots = []
    for part in dispo_str.split(";"):
        part = part.strip()
        if not part:
            continue
        match = re.match(r"(\w+)\s+(\d{1,2}:\d{2})-(\d{1,2}:\d{2})", part)
        if match:
            jour, debut, fin = match.groups()
            slots.append({
                "jour": jour.strip().lower(),
                "debut": datetime.strptime(debut, "%H:%M"),
                "fin": datetime.strptime(fin, "%H:%M"),
            })
    return slots


def horaire_compatible(slots, jour_demande, heure_demande, tolerance_minutes=60):
    """
    Vérifie si un créneau du mentor correspond au jour demandé,
    avec une tolérance de ±1h par rapport au créneau [debut, fin].
    """
    jour_demande = jour_demande.strip().lower()
    try:
        heure_dt = datetime.strptime(heure_demande, "%H:%M")
    except ValueError:
        return False

    tolerance = timedelta(minutes=tolerance_minutes)

    for slot in slots:
        if slot["jour"] != jour_demande:
            continue
        debut_tolerant = slot["debut"] - tolerance
        fin_tolerant = slot["fin"] + tolerance
        if debut_tolerant <= heure_dt <= fin_tolerant:
            return True
    return False


def compute_score(matieres_communes, nb_matieres_demandees, horaire_ok):
    """Score simple de compatibilité sur 100."""
    score_matieres = (len(matieres_communes) / nb_matieres_demandees) * 70 if nb_matieres_demandees else 0
    score_horaire = 30 if horaire_ok else 0
    return round(score_matieres + score_horaire)


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()

    matieres_demandees = [
        m.strip().lower() for m in data.get("matieres", "").split(",") if m.strip()
    ]
    jour_demande = data.get("jour", "")
    heure_demande = data.get("heure", "")
    filiere_demandee = (data.get("filiere") or "").strip().lower()

    if not matieres_demandees or not jour_demande or not heure_demande:
        return jsonify({"error": "Merci de renseigner les matières, le jour et l'heure."}), 400

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM mentors")).mappings().all()

    resultats = []
    for row in rows:
        matieres_mentor = [m.strip().lower() for m in row["matieres"].split(",")]
        communes = set(matieres_demandees) & set(matieres_mentor)

        if not communes:
            continue  # au moins une matière en commun est requise

        slots = parse_disponibilites(row["disponibilites"])
        horaire_ok = horaire_compatible(slots, jour_demande, heure_demande)

        if not horaire_ok:
            continue  # tolérance horaire ±1h non respectée

        if filiere_demandee and row["filiere"] and filiere_demandee != row["filiere"].strip().lower():
            # La filière est optionnelle : on ne l'utilise pas pour exclure,
            # seulement si on veut être strict, décommenter la ligne suivante :
            # continue
            pass

        score = compute_score(communes, len(matieres_demandees), horaire_ok)

        resultats.append({
            "nom": row["nom"],
            "matieres_communes": sorted(communes),
            "disponibilites": row["disponibilites"],
            "format": row["format"],
            "filiere": row["filiere"],
            "score": score,
        })

    resultats.sort(key=lambda m: m["score"], reverse=True)

    return jsonify({"resultats": resultats, "total": len(resultats)})


if __name__ == "__main__":
    app.run(debug=True)
