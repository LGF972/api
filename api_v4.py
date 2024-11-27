from flask import Flask, request, jsonify
import mysql.connector
from db import Database
import hashlib

    
app = Flask(__name__)

db = Database("127.0.0.1", "root","", "ciel_2025_micaa")

@app.route('/v4/etudiants/', methods=['GET'])
def getEtudiants():
    auth = request.authorization
    username = auth.username
    password = auth.password

    if ' ' in username or ' ' in password:
            return jsonify("Accès refusé !"), 400
    
    data = db.log(request)
    if data != 401:
        etudiants = []
        result = db.readAllStudents()
        for row in result:
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }
            etudiants.append(etudiant)
        return jsonify(etudiants), 200
    
@app.route('/v4/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    if not db.authorized(request):
        return jsonify({"Message": "Accès non autorisé !"}), 401
    
    result = db.readOneStudent(id)

    if result:
        etudiant = {
            "idetudiant": result[0],
            "nom": result[1],
            "prenom": result[2],
            "email": result[3],
            "telephone": result[4]
        }
        return jsonify(etudiant), 200

@app.route('/v4/etudiants/', methods=['POST'])
def postEtudiant():
    if not db.authorized(request):
        return jsonify({"Message": "Accès non autorisé !"}), 401
    
    data = request.json
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    telephone = data['telephone']

    result = db.createStudent(nom, prenom, email, telephone)

    if result > 0:
        return jsonify({"Message": "Étudiant supprimé !"}), 200

    return jsonify({"Message": "Étudiant créé avec succès !"}), 201
    

@app.route('/v4/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    if not db.authorized(request):
        return jsonify({"Message": "Accès non autorisé !"}), 401
    
    result = db.deleteStudent(id)

    if result > 0:
        return jsonify({"Message": "Étudiant supprimé !"}), 200
    else:
        return jsonify({"MEssage": "Pas d'étudiant correspondant ou déjà supprimé !"}), 404

@app.route('/v4/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if not db.authorized(request):
        return jsonify({"Message": "Accès non autorisé !"}), 401
    
    data = request.json
    nom = data['nom']
    prenom = data['prenom']
    email = data['email']
    telephone = data['telephone']

    result = db.updateStudent(nom, prenom, email, telephone, id)

    if result > 0:
        return jsonify({"Message": "Étudiant modifié avec succès !"}), 200
    else:
        return jsonify({"Message": "Étudiant introuvable !"}), 404

@app.route("/v4/login", methods=["GET"])
def login():
    auth = request.authorization
    username = auth.username
    password = auth.password

    if ' ' in username or ' ' in password:
            return jsonify("Accès refusé !"), 400
    
    data = db.log(request)
    if data != 401:
        user = {
            "username": data[0],
            "password": data[1]
        }
        return jsonify(user), 200
    else:
        return jsonify(password), 404

if __name__ == '__main__':
    context = ( 'cert.pem', 'key.pem' )
    app.run(host = '0.0.0.0', ssl_context=context, debug=True)