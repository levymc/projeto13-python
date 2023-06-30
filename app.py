from flask import Flask, request
from flask import jsonify
from pymongo_get_database import get_database
from datetime import datetime
from donttrust import Schema
from donttrust.exceptions import DontTrustBaseException
from waitress import serve
import time  
from setInterval import setInterval
from bson import json_util
from flask_cors import cross_origin


timeStamp = time.time()
mode = 'dev'  #prod ou dev
app = Flask(__name__)
db = get_database()

schemaName = Schema().string().min(1).required()
schemaMessage = {
    "to": Schema().string().min(1).required(),
    "text": Schema().string().min(1).required(),
    "type": Schema().string().min(1).required(),
    "from": Schema().string().min(1).required()
}

@app.route("/participants", methods=["POST"])
@cross_origin()
def create_participant():
    name = request.json.get("name")
    print(name)
    try: 
        schemaName.validate(name)
    except DontTrustBaseException as e:
        return jsonify({"error": str(e.message)}), 422

    participant = db["test"]['participants'].find_one({"name": name})
    if not participant:
        message = {
            "from": name,
            "to": "Todos",
            "text": "entra na sala...",
            "type": "status",
            "time": datetime.now().strftime("%H:%M:%S")
        }

        db["test"]['participants'].insert_one({"name": name, "lastStatus": timeStamp})
        db["test"]['messages'].insert_one(message)

        return jsonify({"message": "Participante criado"}), 201
    else:
        return jsonify({"error": "Participante já existe"}), 409

@app.route("/participants", methods=["GET"])
@cross_origin()
def get_participants():
    participants = list(db["test"].participants.find())
    return jsonify(json_util.dumps(participants))


@app.route("/messages", methods=["POST"])
@cross_origin()
def create_message():
    data = request.json
    to, text, type = data["to"], data["text"], data["type"]
    from_header = request.headers.get("user")
    
    participant = db["test"]['participants'].find_one({"name": from_header})
    if not participant:
        return jsonify({"error": "Participante inválido"}), 422

    try:
        schemaMessage["to"].validate(to)
        schemaMessage["text"].validate(text)
        schemaMessage["type"].validate(type)
        schemaMessage["from"].validate(from_header)
    except DontTrustBaseException as e:
        return jsonify({"error": str(e.message)}), 422

    message = {
        "from": from_header,
        "to": data["to"],
        "text": data["text"],
        "type": data["type"],
        "time": datetime.now().strftime("%H:%M:%S")
    }
    print(message)

    try:
        db["test"]["messages"].insert_one(message)
        print("Mensagem:", message)
        return jsonify(json_util.dumps(message)), 201
    except Exception as e:
        print(str(e))
        return jsonify({"error": "Ocorreu um erro no banco de dados"}), 409


if __name__ == '__main__':
    if mode == 'dev':
        print(f'Servidor iniciando em: http://localhost:{5005}')
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=5, url_scheme='https')