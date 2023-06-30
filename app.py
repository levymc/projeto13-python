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


async def foo():
    await print("hello")


# using
# setInterval(foo,5)
timeStamp = time.time()
mode = 'dev'  #prod ou dev
app = Flask(__name__)
db = get_database()



schemaName = Schema().string().min(1).required()

# try:
#     print(schemaName.validate("a"))
# except DontTrustBaseException as e:
#     print(e.message)

# item_details = collection_name.find()
# for item in item_details:
#    print(item)



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
    # print(json_util.dumps(participants))
    return jsonify(json_util.dumps(participants))


if __name__ == '__main__':
    if mode == 'dev':
        print(f'Servidor iniciando em: http://localhost:{5005}')
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=5, url_scheme='https')