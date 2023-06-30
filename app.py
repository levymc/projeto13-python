from flask import Flask
from waitress import serve
from pymongo_get_database import get_database

db = get_database()
collection_name = db["test"]['messages']

item_details = collection_name.find()
for item in item_details:
   print(item)


mode = "dev" #prod ou dev
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5005)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=5, url_scheme='https')