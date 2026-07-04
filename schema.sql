-- Schéma de la base de données IFRI_MentorLink
-- Compatible PostgreSQL (par défaut). Pour MySQL, voir les notes en bas.

CREATE TABLE IF NOT EXISTS mentors (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    matieres TEXT NOT NULL,              -- ex: "Algorithmique, Bases de données, Python"
    disponibilites TEXT NOT NULL,        -- ex: "Lundi 14:00-16:00;Mercredi 10:00-12:00"
    filiere VARCHAR(100),                -- ex: "IA", "GL", "SI"
    format VARCHAR(20) NOT NULL          -- 'presentiel', 'en_ligne' ou 'les_deux'
);

-- === Données de test (matières réelles du programme IFRI, Licence 1) ===

INSERT INTO mentors (nom, matieres, disponibilites, filiere, format) VALUES
('Aïcha Kouassi', 'Algorithmique, Langage C, Programmation Python, Logique et arithmétique', 'Lundi 14:00-16:00;Mercredi 10:00-12:00', 'GL', 'les_deux'),
('Bruno Djossou', 'Architecture et topologie des réseaux, Administration des réseaux Windows/Linux, Système d''exploitation', 'Mardi 09:00-11:00;Jeudi 15:00-17:00', 'SE&IoT', 'en_ligne'),
('Claire Amoussou', 'Bases de données relationnelles, SGBD et langage SQL, Développement web', 'Lundi 09:00-11:00;Vendredi 13:00-15:00', 'GL', 'presentiel'),
('David Hounsou', 'Analyse et applications, Algèbre linéaire et applications, Probabilités et statistiques, Suites et séries numériques', 'Mercredi 14:00-16:00;Samedi 10:00-12:00', 'IA', 'les_deux'),
('Estelle Fanou', 'Théorie des graphes et applications, Recherche opérationnelle, Mathématiques appliquées', 'Jeudi 09:00-11:00;Lundi 16:00-18:00', 'SI', 'en_ligne'),
('Fabrice Agossou', 'Équations différentielles et calcul intégral, Analyse combinatoire, Statistiques inférentielles', 'Mardi 14:00-16:00;Vendredi 09:00-11:00', 'IM', 'les_deux'),
('Gloria Sossou', 'Infographie, Développement web, Techniques d''expression écrite et orale', 'Lundi 11:00-13:00;Mercredi 15:00-17:00', 'GL', 'presentiel'),
('Hervé Zannou', 'Anglais technique, Déontologie et droit liés aux TIC, Outils de base en informatique', 'Jeudi 13:00-15:00;Samedi 09:00-11:00', 'SI', 'en_ligne');

-- === Notes pour MySQL ===
-- Remplacer "SERIAL" par "INT AUTO_INCREMENT" et ajouter "AUTO_INCREMENT" sur la colonne id.
-- Exemple :
-- CREATE TABLE mentors (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     nom VARCHAR(150) NOT NULL,
--     matieres TEXT NOT NULL,
--     disponibilites TEXT NOT NULL,
--     filiere VARCHAR(100),
--     format VARCHAR(20) NOT NULL
-- );
