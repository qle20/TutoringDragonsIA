

from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import sys

sys.path.append("Algorithms/Imported")
import Connector as cn

app = Flask(__name__)

user_host = 'localhost'
user_login = 'root'
password = 'razzmatazz'
schema = 'Test_schema'

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        connection, curr = cn.connect(user_host, user_login, password, schema)
        value = cn.get_value_list(curr, "Questions Order by QuestionID")
        cn.end_connection(connection)
        print(username)
        return render_template('/Main/question.html', data=value[0][1])

@app.route('/login_request', methods=["POST"])
def login_request():
    username = request.form["username"]
    connection, curr = cn.connect(user_host, user_login, password, schema)
    tutor_value = cn.get_value_list(curr, "Tutor", 1)
    student_value = cn.get_value_list(curr, "Student", 1)
    cn.end_connection(connection)
    final_value = tutor_value + student_value
    print username
    if username in final_value:
        return home(username)
    return json.dumps({'status': 'OK', 'user': username})

@app.route('/main/question')
def question():
    # connection, curr = cn.connect(user_host, user_login, password, schema)
    # value = cn.get_value_list(curr, "Questions Order by QuestionID")
    # cn.end_connection(connection)

    # print(username)
    return render_template('/Main/question.html', data=value[0][1]);

@app.route('/main/admin')
def admin():
    print("10")


if __name__ == "__main__":
    app.run(debug=True)




