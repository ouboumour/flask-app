CREATE TABLE IF NOT EXISTS profile (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(46)
);

CREATE TABLE IF NOT EXISTS utilisateur (
    id INT PRIMARY KEY AUTO_INCREMENT,
    prenom VARCHAR(46),
    nom VARCHAR(46),
    tel VARCHAR(15),
    username VARCHAR(46) UNIQUE ,
    password VARCHAR(46),
    profile_id INT,
    FOREIGN KEY (profile_id) REFERENCES profile(id)
);

CREATE TABLE IF NOT EXISTS salle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(46)
);

CREATE TABLE IF NOT EXISTS etudiant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    prenom VARCHAR(46),
    nom VARCHAR(46),
    tolerance BOOL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS matiere (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(46)
);

CREATE TABLE IF NOT EXISTS cours (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(46),
    description VARCHAR(300),
    matiere_id INT,
    cout_seance DECIMAL(6,2),
    FOREIGN KEY (matiere_id) REFERENCES matiere(id)
);

CREATE TABLE IF NOT EXISTS inscription (
    cours_id INT,
    etudiant_id INT,
    credit DECIMAL(6,2),
    en_attente BOOL,
    FOREIGN KEY (cours_id) REFERENCES cours(id),
    FOREIGN KEY (etudiant_id) REFERENCES etudiant(id)
);

CREATE TABLE IF NOT EXISTS categorie (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(46)
);

CREATE TABLE IF NOT EXISTS niveau (
    id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    nom VARCHAR(46),
    categorie_id INT,
    FOREIGN KEY (categorie_id) REFERENCES categorie(id)

);

CREATE TABLE IF NOT EXISTS niveau_etudiant (
    niveau_id INT,
    etudiant_id INT,
    FOREIGN KEY (niveau_id) REFERENCES niveau(id),
    FOREIGN KEY (etudiant_id) REFERENCES etudiant(id)
);

CREATE TABLE IF NOT EXISTS niveau_cours (
    niveau_id INT,
    cours_id INT,
    FOREIGN KEY (niveau_id) REFERENCES niveau(id),
    FOREIGN KEY (cours_id) REFERENCES cours(id)
);

CREATE TABLE IF NOT EXISTS enseignant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    prenom VARCHAR(46),
    nom VARCHAR(46)
);

CREATE TABLE IF NOT EXISTS cours_enseignant (
    cours_id INT,
    enseignant_id INT,
    FOREIGN KEY (cours_id) REFERENCES cours(id),
    FOREIGN KEY (enseignant_id) REFERENCES enseignant(id)
);

CREATE TABLE IF NOT EXISTS seance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    debut_seance DATETIME,
    fin_seance DATETIME,
    salle_id INT,
    enseignant_id INT,
    cours_id INT,
    FOREIGN KEY (salle_id) REFERENCES salle(id),
    FOREIGN KEY (enseignant_id) REFERENCES enseignant(id),
    FOREIGN KEY (cours_id) REFERENCES cours(id)
);


CREATE TABLE IF NOT EXISTS seance_etudiant (
    seance_id INT,
    etudiant_id INT,
    est_present BOOL,
    FOREIGN KEY (etudiant_id) REFERENCES etudiant(id),
    FOREIGN KEY (seance_id) REFERENCES seance(id)
);

CREATE TABLE IF NOT EXISTS matiere_niveau (
    matiere_id INT,
    niveau_id INT,
    FOREIGN KEY (matiere_id) REFERENCES matiere(id),
    FOREIGN KEY (niveau_id) REFERENCES niveau(id)
);

