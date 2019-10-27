from flask import Flask, render_template, request, session
import os

from Imported import Connector as cn
from content_management import content
from algorithm import matching, send_email_matching


TOPIC_DICT = content()
app = Flask(__name__)
# user_host = 'srvr-ustudentlab.ssis.edu.vn'
# user_login = 'qle20'
# password = 'ssis12345!'
# schema = 'qle20'

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

    if username == "admin":
        session["logged_in"] = True
        session['username'] = "admin"
        return homepage()
    if username in username_list:
        session['logged_in'] = True
        login = final_value[username_list.index(username)]
        print(login)
        session['username'] = login
        session['username'] = login
        print(session['username'])
        return homepage()
    else:
        error = 'Invalid Credentials, Please try again'
        connection.close()
        return render_template('login.html', error = error)

@app.route('/question/<user>', methods=["POST"])
def get_question(user):

    if request.method == "POST":
        connection,curr = cn.connect(user_host, user_login, password, schema)
        result = request.form
        index = 0
        if "T" in (session["username"])[0] :
            table = "AnswerTutor"
            tableid = "TutorID"
        else:
            table = "AnswerStudent"
            tableid = "StudentID"
        cn.delete(connection, curr, table, tableid, session["username"][0])

        for question in result:
            index += 1
            values = [index, session["username"][0], result[question]]
            cn.add_value(connection, curr, table, values)
        connection.close()

        return render_template("/Main/result.html", result = result,  name = session["username"][2])

@app.route('/signup', methods=["POST"])
def sign_up():
    session['logged_in'] = False
    return render_template("/signup.html")

@app.route('/admin', methods=["POST"])
def admin():
    if request.method == "POST":
        result = request.form
        connection, curr = cn.connect(user_host, user_login, password, schema)
        for value in result:
            if str(value) == "matching":
                if result[value] == "Yes":
                    for i in range(0 , 5):
                        try:
                            matching(connection,
                                     curr,
                                     "AnswerTutor",
                                     "AnswerStudent",
                                     "Matching",
                                     str(i),
                                     "TutorID",
                                     "StudentID",
                                     "schedule")
                        except:
                            print("Hello")
                error = "Successfully matched"
                return render_template("/Main/admin.html", error=result)

            if str(value) == "email":
                if result[value] == "Yes":
                    result = send_email_matching(curr, "schedule", email_address, email_pass)
                    return render_template("/Main/admin.html", error= result )


@app.route("/display_database", methods=["POST"])
def display():
    if request.method == "POST":
        database = request.form["database"]
        if database == "Yes":
            connection, curr = cn.connect(user_host, user_login, password, schema)
            answerStudent = cn.get_value_list(curr, "AnswerStudent")
            answerTutor = cn.get_value_list(curr, "AnswerTutor")
            tutor = cn.get_value_list(curr, "Tutor")
            student = cn.get_value_list(curr, "Student")
            matching = cn.get_value_list(curr, "matching")
            connection.close()
            return render_template("/Main/DisplayDatabase.html",
                                   database="Yes",
                                   answerStudent=answerStudent,
                                   answerTutor=answerTutor,
                                   tutor=tutor,
                                   student=student,
                                   matching=matching)



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
    email_address = os.environ.get("DB_USER")
    email_pass = os.environ.get("DB_PASS")

    app.secret_key = os.urandom(12)
    app.run(debug=False)
