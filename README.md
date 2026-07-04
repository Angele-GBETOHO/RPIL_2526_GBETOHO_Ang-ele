# IFRI_MentorLink — Version simplifiée (Rattrapage)

Application web permettant à un mentoré de rechercher un mentor compatible,
sans authentification, via un algorithme de matching basé sur :
- la compatibilité des matières/compétences (au moins une matière en commun),
- la compatibilité horaire (tolérance de ±1 heure).

## Stack technique
- **Frontend** : HTML / CSS / JavaScript + Bootstrap 5
- **Backend** : Python (Flask) + SQLAlchemy
- **Base de données** : PostgreSQL (ou MySQL, voir plus bas)

## Structure du projet
```
mentorlink/
├── app.py                 # Backend Flask + logique de matching
├── schema.sql              # Création de la table + données de test
├── requirements.txt
├── templates/
│   └── index.html          # Formulaire de recherche
└── static/
    ├── script.js            # Appel API + affichage des résultats
    └── style.css
```

## Installation

### 1. Cloner le dépôt et installer les dépendances
```bash
git clone https://github.com/<ton-compte>/RPIL_2526_<nom>_<prenom>.git
cd RPIL_2526_<nom>_<prenom>
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Créer la base de données

**Avec PostgreSQL :**
```bash
createdb mentorlink
psql mentorlink < schema.sql
```

**Avec MySQL :**
```bash
mysql -u root -p -e "CREATE DATABASE mentorlink;"
mysql -u root -p mentorlink < schema.sql
```
(Pense à adapter `schema.sql` : remplacer `SERIAL` par `INT AUTO_INCREMENT` — voir note en bas du fichier.)

### 3. Configurer la connexion

Définis la variable d'environnement `DATABASE_URL` :

```bash
# PostgreSQL
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/mentorlink"

# MySQL
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/mentorlink"
```

### 4. Lancer l'application
```bash
python app.py
```
Puis ouvrir : http://127.0.0.1:5000

## Fonctionnement du matching
1. Le mentoré saisit les matières recherchées, un jour, une heure et (en option) une filière.
2. Le backend compare les matières demandées à celles de chaque mentor (au moins une matière commune requise).
3. Il vérifie que le mentor a un créneau ce jour-là, avec une tolérance de ±1h par rapport à l'heure souhaitée.
4. Un score de compatibilité (sur 100) est calculé : 70% basé sur le taux de matières en commun, 30% si l'horaire est compatible.
5. Les résultats sont triés par score décroissant et affichés côté client.

## À personnaliser avant la soumission
- Ajouter/adapter les mentors de test dans `schema.sql` si besoin.
- Ajuster le style (couleurs, logo IFRI) dans `static/style.css`.
- Vérifier le nom du dépôt GitHub : `RPIL_2526_nom_prenom`.
- Préparer une courte présentation (fonctionnement du matching, choix techniques) pour la soutenance du lundi 06/07 à 16h.
