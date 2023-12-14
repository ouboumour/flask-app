INSERT INTO categorie (id, nom)
    VALUES
        (1, 'Cours de soutien'),
        (2, 'Langues'),
        (3, 'Soft skills');

INSERT INTO niveau (id, nom, categorie_id)
    VALUES
        (1, '2ème année lycée', 1),
        (2, '3ème année lycée', 1),
        (3, 'Debutant', 2),
        (4, '1ère année lycée', 1),
        (5, '1ère année collège', 1),
        (6, '2ème année collège', 1),
        (7, '3ème année collège', 1),
        (8, 'Intermédiaire', 2),
        (9, 'Avancée', 2);



INSERT INTO matiere (id, nom)
    VALUES
        (1, 'Math'),
        (2, 'PC'),
        (3, 'SVT'),
        (4, 'Espagnol');

INSERT INTO cours (id, nom, description, matiere_id, cout_seance)
    VALUES
        (1, 'Les nombres complexes', 'Dans ce cours, on va voir le chapitre 1 des nombres complexes', 1, 200),
        (2, 'Les fonctions', 'Dans ce cours, on va voir le chapitre 3 des fonctions', 1, 150),
        (3, 'Mécanique', 'Dans ce cours, on va voir le dernier chapitre de la partie mécanique', 2, 200),
        (4, 'Conjugación', 'Dans ce cours, on va voir comment conjuguer quelques verbes de base', 4, 150);

INSERT INTO niveau_cours (niveau_id, cours_id)
    VALUES
        (2, 1),
        (1, 2),
        (2, 3),
        (3, 4);

INSERT INTO enseignant (id, prenom, nom)
    VALUES
        (1, 'Jean', 'Dupont'),
        (2, 'Marie', 'Martin'),
        (3, 'Pierre', 'Dubois');

INSERT INTO cours_enseignant (cours_id, enseignant_id)
    VALUES
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3);


insert into profile (id, nom)
values
    (1, 'admin'),
    (2, 'teacher'),
    (3, 'student');


INSERT INTO utilisateur (id, prenom, nom, tel, username, password, profile_id)
    VALUES
        (1, 'admin', 'admin', '0000000000', 'contact@courses.com', 'admin', 1),
        (2, 'Marwa', 'BOUMOUR', '0612345678', 'tmarwa@courses.com', 'tmarwa', 2),
        (3, 'Marwa', 'BOUMOUR', '0612345679', 'smarwa@courses.com', 'smarwa', 3);

INSERT INTO etudiant (id, prenom, nom)
    VALUES
        (1, 'Yassine', 'Bounou'),
        (2, 'Naruto', 'Uzumaki'),
        (3, 'Zineb', 'Benjelloun'),
        (4, 'John', 'Doe'),
        (5, 'Alice', 'Smith'),
        (6, 'Mohammed', 'Ali'),
        (7, 'Emma', 'Johnson'),
        (8, 'Ahmed', 'Khan');


INSERT INTO salle (id, nom)
    VALUES
        (1, 'A404'),
        (2, 'B32'),
        (3, 'F202');

INSERT INTO seance (id, debut_seance, fin_seance, salle_id, enseignant_id, cours_id)
    VALUES
        (1, '2023-01-23 19:00:00', '2023-01-23 21:00:00', 1, 1, 1),
        (2, '2023-01-23 19:00:00', '2023-01-23 21:00:00', 2, 3, 4);

INSERT INTO seance_etudiant (seance_id, etudiant_id, est_present)
    VALUES
        (1, 1, FALSE),
        (1, 2, FALSE),
        (1, 3, FALSE),
        (1, 4, TRUE),
        (2, 5, TRUE),
        (2, 6, TRUE),
        (2, 7, TRUE),
        (2, 8, TRUE);


INSERT INTO inscription (cours_id, etudiant_id, credit, en_attente)
    VALUES
        (1, 1, 500, FALSE),
        (1, 2, 500, FALSE),
        (1, 3, 500, FALSE),
        (1, 4, 200, FALSE),
        (1, 5, 150, TRUE),
        (1, 6, 150, TRUE),
        (2, 5, 500, FALSE),
        (2, 6, 1000, FALSE),
        (2, 7, 500, FALSE),
        (2, 8, 500, FALSE);

INSERT INTO matiere_niveau (matiere_id, niveau_id)
    VALUES
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (2, 1),
        (2, 2),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (3, 1),
        (3, 2),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (4, 3),
        (4, 8),
        (4, 9);