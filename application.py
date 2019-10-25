from flask import Flask, render_template, request, session
import os

from Imported import Connector as cn
from content_management import content

TOPIC_DICT = content()
app = Flask(__name__)
user_host = 'localhost'
user_login = 'root'
password = 'razzmatazz'
schema = 'Test_schema'

@app.route('/')
def homepage():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session["username"] == "admin":
        return render_template('/Main/admin.html')
    else:
        connection, curr = cn.connect(user_host, user_login, password, schema)
        question_list = cn.get_value_list(curr, "Questions Order By QuestionID")
        question_list = cn.convert(question_list)
        connection.close()

        return render_template('/Main/question.html', username = session["username"], toPass = question_list)

@app.route('/login_request', methods=["POST"])
def login_request():
    '''
    :return:
    '''
    connection, curr = cn.connect(user_host, user_login, password, schema)
    tutor_value = cn.get_value_list(curr, "Tutor")
    student_value = cn.get_value_list(curr, "Student")
    connection.close()

    final_value = tutor_value + student_value
    username_list = cn.combine(final_value, 1)
    username = request.form['username']

    if (username in username_list) or (username == 'admin'):
        session['logged_in'] = True
        login = final_value[username.index(username)]
        session['username'] = login
        return homepage()
    else:
        error = 'Invalid Credentials, Please try again'
        connection.close()
        return render_template('login.html', error = error)

@app.route('/question', methods=["POST"])
def get_question():
    if request.method == "POST":

        result = request.form
        print(result)
        print(session['username'])
        for question in result:
            print(result[question])
        return render_template("/Main/result.html", result = result)

@app.route('/signup', methods=["POST"])
def sign_up():
    session['logged_in'] = False
    return render_template("/signup.html")

# @app.route('app_cancel', methods=["POST"])
# def cancell
#
# # @app.route('/addusername', methods=["POST"])
# # def add_username():
# #     if request.method == "POST":
# #         if
# #         result = request.form
# #         print(result)

if __name__ == "__main__":
    connection, curr = cn.connect(user_host, user_login, password, schema)
    cn.delete(connection, curr, "schedule")
    cn.delete(connection, curr, "Matching")
    connection.close()

    app.secret_key = os.urandom(12)
    app.run(debug=False)
