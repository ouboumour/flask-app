import mysql.connector
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "admin123"

connection = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='PHW#84#jeor',
    database='centre_formation',
    port='3307'
)


# def toListMatrix():


def check_login():
    if not session.get('logged_in', False) and request.endpoint not in ['login']:
        return redirect(url_for('login'))


app.before_request(check_login)

if __name__ == "_main_":
    app.run(debug=True)


def get_columns(cursor):
    return [desc[0] for desc in cursor.description]


def fetchAll(table_name):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    return get_columns(cursor), cursor.fetchall()


def are_credentials_ok(username, password):
    cursor = connection.cursor()
    query = f'''SELECT * from utilisateur WHERE username LIKE '{username}' AND password LIKE '{password}' LIMIT 1;'''
    cursor.execute(query)
    return cursor.fetchone() is not None


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('logged_in', False):
        return redirect(url_for('home'))

    if len(request.form) and are_credentials_ok(request.form['email'], request.form['password']):
        session['logged_in'] = True
        return redirect(url_for('home'))

    return render_template("login-form.html",
                           error_message="" if request.method == 'GET' else "Invalid username or password")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return  redirect(url_for('login'))

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/categories")
def afficher_categories():
    columns, rows = fetchAll("categorie")
    return render_template("rows-table.html",
                           page_name='Catégorie',
                           title="Liste des catégories",
                           columns=columns,
                           rows=rows
                           )


@app.route("/cours")
def afficher_cours():
    cursor = connection.cursor()
    query = f'''
        SELECT c.id, 
               c.nom, 
               c.description as 'Description du cours', 
               CONCAT(c.cout_seance, ' DH') as 'Prix de la séance', 
               m.nom as 'Nom de la matière',
               n.nom as 'Niveau',
               cat.nom as 'Catégorie' 
        FROM cours c 
              INNER JOIN niveau_cours nc on c.id = nc.cours_id 
              INNER JOIN niveau n on nc.niveau_id = n.id 
              INNER JOIN categorie cat on n.categorie_id = cat.id   
              INNER JOIN matiere m on c.matiere_id = m.id;
        '''
    cursor.execute(query)
    return render_template("rows-table.html",
                           page_name='Cours',
                           title="Liste des cours",
                           columns=get_columns(cursor),
                           rows=cursor.fetchall()
                           )

@app.route("/cours/categories/<categorie>")
def afficher_cours_par_categorie(categorie):
    cursor = connection.cursor()
    query = f'''
        SELECT c.id, c.nom, c.description, c.cout_seance, m.nom, n.nom, cat.nom FROM cours c 
                              INNER JOIN niveau_cours nc on c.id = nc.cours_id 
                              INNER JOIN niveau n on nc.niveau_id = n.id 
                              INNER JOIN categorie cat on n.categorie_id = cat.id   
                              INNER JOIN matiere m on c.matiere_id = m.id   
        WHERE cat.nom LIKE '{categorie}';
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/cours/categories/<categorie>/niveau/<niveau>")
def afficher_cours_par_categorie_par_niveau(categorie, niveau):
    cursor = connection.cursor()
    query = f'''
        SELECT c.id, c.nom, c.description, c.cout_seance, m.nom, n.nom, cat.nom FROM cours c 
                              INNER JOIN niveau_cours nc on c.id = nc.cours_id 
                              INNER JOIN niveau n on nc.niveau_id = n.id 
                              INNER JOIN categorie cat on n.categorie_id = cat.id   
                              INNER JOIN matiere m on c.matiere_id = m.id   
        WHERE cat.nom LIKE '{categorie}' AND n.nom LIKE '{niveau}';
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/cours/enseignants/<enseignant_id>")
def afficher_cours_par_enseignant(enseignant_id):
    cursor = connection.cursor()
    query = f'''
        SELECT c.id, c.nom, c.description, c.cout_seance, m.nom, n.nom, cat.nom FROM cours c 
                              INNER JOIN niveau_cours nc on c.id = nc.cours_id 
                              INNER JOIN niveau n on nc.niveau_id = n.id 
                              INNER JOIN categorie cat on n.categorie_id = cat.id   
                              INNER JOIN matiere m on c.matiere_id = m.id
           
                              INNER JOIN cours_enseignant ce on c.id = ce.cours_id
                              INNER JOIN enseignant e on ce.enseignant_id = e.id
        WHERE e.id = {enseignant_id};
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/cours/matieres/<matiere_id>")
def afficher_cours_par_matiere(matiere_id):
    cursor = connection.cursor()
    query = f'''
        SELECT c.id, c.nom, c.description, c.cout_seance, m.nom, n.nom, cat.nom FROM cours c 
                              INNER JOIN niveau_cours nc on c.id = nc.cours_id 
                              INNER JOIN niveau n on nc.niveau_id = n.id 
                              INNER JOIN categorie cat on n.categorie_id = cat.id   
                              INNER JOIN matiere m on c.matiere_id = m.id
        WHERE m.id = {matiere_id};
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/enseignants")
def afficher_enseignants():
    columns, rows = fetchAll("enseignant")
    return render_template("rows-table.html",
                           page_name='Enseignants',
                           title="Liste des enseignants",
                           columns=columns,
                           rows=rows
                           )

@app.route("/enseignants/seance/<seance_id>")
def afficher_enseignants_par_seance(seance_id):
    cursor = connection.cursor()
    query = f'''
        SELECT e.* FROM enseignant e INNER JOIN centre_formation.seance s on e.id = s.enseignant_id WHERE s.id={seance_id};
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/etudiants")
def afficher_etudiants():
    columns, rows = fetchAll("etudiant")
    return render_template("rows-table.html",
                           page_name='Etudiants',
                           title="Liste des étudiants",
                           columns=columns,
                           rows=rows
                           )


@app.route("/etudiants/seances/<seance_id>")
def afficher_groupe_etudiants_par_seance(seance_id):
    cursor = connection.cursor()
    query = f'''
        SELECT e.* FROM etudiant e
            INNER JOIN seance_etudiant se on e.id = se.etudiant_id
            INNER JOIN seance s on s.id = se.seance_id
        WHERE s.id={seance_id};
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/inscriptions")
def afficher_inscriptions():
    en_attente = request.args.get('en_attente')
    cursor = connection.cursor()
    query = f'''
                SELECT 
                    e.id,
                    e.prenom, 
                    e.nom, 
                    i.credit,
                    i.en_attente as 'En attente d''un groupe ?',
                    c.nom,
                    c.cout_seance as 'Prix de la séance'
                FROM inscription i
                    INNER JOIN etudiant e on e.id = i.etudiant_id
                    INNER JOIN cours c on c.id = i.cours_id
                '''

    if en_attente is not None:
        query += f'''WHERE i.en_attente = {en_attente}'''

    cursor.execute(query)
    return render_template("rows-table.html",
                           page_name='Inscriptions',
                           title="Liste des inscriptions",
                           columns=get_columns(cursor),
                           rows=cursor.fetchall()
                           )


@app.route("/inscriptions/etudiants/<etudiant_id>")
def afficher_inscriptions_par_etudiant(etudiant_id):
    cursor = connection.cursor()
    query = f'''
        SELECT e.id, e.prenom, e.nom, i.credit, i.en_attente, c.nom, c.cout_seance FROM inscription i
            INNER JOIN etudiant e on e.id = i.etudiant_id
            INNER JOIN cours c on c.id = i.cours_id
        WHERE e.id = {etudiant_id};
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/inscriptions/cours/<cours_id>")
def afficher_inscriptions_par_cours(cours_id):
    en_attente = request.args.get('en_attente')
    print()
    cursor = connection.cursor()
    query = f'''
        SELECT e.id, e.prenom, e.nom, i.credit, i.en_attente, c.nom, c.cout_seance FROM inscription i
            INNER JOIN etudiant e on e.id = i.etudiant_id
            INNER JOIN cours c on c.id = i.cours_id
        WHERE c.id = {cours_id}
        '''

    if en_attente is not None:
        query += f'''AND i.en_attente = {en_attente}'''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/matieres")
def afficher_matieres():
    columns, rows = fetchAll("matiere")
    return render_template("rows-table.html",
                           page_name='Matieres',
                           title="Liste des matières",
                           columns=columns,
                           rows=rows
                           )


@app.route("/matieres/categories/<categorie_id>")
def afficher_matieres_par_categorie(categorie_id):
    cursor = connection.cursor()
    query = f'''
        SELECT m.id, m.nom FROM cours c 
                              INNER JOIN niveau_cours nc on c.id = nc.cours_id 
                              INNER JOIN niveau n on nc.niveau_id = n.id 
                              INNER JOIN categorie cat on n.categorie_id = cat.id   
                              INNER JOIN matiere m on c.matiere_id = m.id   
        WHERE cat.id = {categorie_id};
        '''

    cursor.execute(query)
    return cursor.fetchall()


@app.route("/matieres/niveau/<niveau_id>")
def afficher_matieres_par_niveau(niveau_id):
    cursor = connection.cursor()
    query = f'''
        SELECT m.id, m.nom FROM matiere m 
            INNER JOIN matiere_niveau mn on mn.matiere_id = m.id
            INNER JOIN niveau n on n.id = mn.niveau_id
        WHERE n.id = {niveau_id};
        '''
    cursor.execute(query)
    return cursor.fetchall()


@app.route("/profiles")
def afficher_profiles():
    return fetchAll("profile")


@app.route("/salles")
def afficher_salles():
    columns, rows = fetchAll("salle")
    return render_template("rows-table.html",
                           page_name='Salles',
                           title="Liste des salles",
                           columns=columns,
                           rows=rows
                           )


@app.route("/seances")
def afficher_seances():
    cursor = connection.cursor()
    query = f'''
        SELECT 
            s.id,
            s.debut_seance as 'Début de la séance',
            s.fin_seance as 'Fin de la séance',
            sa.nom as 'Salle',
            e.prenom as 'Prenom de l''enseignant',
            e.nom as 'Nom de l''enseignant', 
            c.nom as 'Cours',
            CONCAT(c.cout_seance, ' DH') as 'Prix de la séance'
        FROM seance s 
            INNER JOIN salle sa on sa.id = s.salle_id
            INNER JOIN enseignant e on e.id = s.enseignant_id
            INNER JOIN cours c on c.id = s.cours_id
        '''
    cursor.execute(query)
    return render_template("rows-table.html",
                           page_name='Séance',
                           title="Liste des séances",
                           columns=get_columns(cursor),
                           rows=cursor.fetchall()
                           )


@app.route("/seances/enseignant/<enseignant_id>")
def afficher_seances_par_enseignant(enseignant_id):
    cursor = connection.cursor()
    query = f'''
        SELECT s.id, s.debut_seance, s.fin_seance, sa.nom, e.prenom, e.nom, c.nom, c.cout_seance FROM seance s 
            INNER JOIN salle sa on sa.id = s.salle_id
            INNER JOIN enseignant e on e.id = s.enseignant_id
            INNER JOIN cours c on c.id = s.cours_id
        WHERE enseignant_id = {enseignant_id}
        '''
    cursor.execute(query)
    return cursor.fetchall()


@app.route("/presence/seance/<seance_id>")
def afficher_feuille_de_presence(seance_id):
    cursor = connection.cursor()
    query = f'''
        SELECT e.id, e.prenom, e.nom, se.est_present FROM etudiant e
            INNER JOIN seance_etudiant se on se.etudiant_id=e.id
        WHERE se.seance_id = {seance_id}
        '''
    cursor.execute(query)
    return cursor.fetchall()


@app.route("/utilisateurs")
def afficher_utilisateurs():
    cursor = connection.cursor()
    query = '''
        SELECT
            u.id,
            u.prenom,
            u.nom,
            u.tel as 'Numéro de téléphone',
            u.username as 'email',
            p.nom as 'Profile'
        FROM utilisateur u 
            INNER JOIN profile p on u.profile_id = p.id;
        '''

    cursor.execute(query)
    return render_template("rows-table.html",
                           page_name='Utilisateurs',
                           title="Liste des utilisateurs",
                           columns=get_columns(cursor),
                           rows=cursor.fetchall()
                           )