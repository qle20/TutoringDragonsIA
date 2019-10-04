from flask import Flask, render_template
import json
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# TODO TODO TODO GOODLUCK
@app.route('/login_request', methods=['POST'])
def login_request():
    username = request.form["username"]
    password = request.form["password"]
    return json.dumps({'status':'OK','user':username,'pass':password});

if __name__ == "__main__":
    app.run(debug=True)