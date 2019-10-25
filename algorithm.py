### Paring algorithm, I need to do this in 3 hours esketit
## Standard Library Immports
import sys
sys.path.append("Imported")
from Imported import Connector as cn
from Imported import Email as e
import os

def max_index(matrix, index):
    max = -1
    for value in matrix:
        cur = value[index]
        if cur > max:
            max = cur
    return(max)

def in_matrix(matrix, input_value):
    for row in matrix:
        for col in row:
            if input_value == col:
                return True
    return False

def amount_matrix(matrix, input_value):
    value_occur = 0
    for row in matrix:
        for col in row:
            if input_value == col:
                value_occur += 1
    return value_occur

def person_info_list(cursor, table, questionID, personID):
    """
    ("SELECT " + return_value + " From " + table + " Where " + column + " " + condition + ' "' + equal_to + '"' )
    :param array:
    :return:
    """

    sql = ("SELECT " + personID + " From " + table + " Where QuestionID=" + questionID + " and " \
           "Answers='Yes'")

    cursor.execute(sql)
    db_list = cursor.fetchall()

    #Get PersonID where it corresponds to the day of the week that they are free in

    sql_get_info = ("SELECT " + personID + ", Answers From " + table +
                    " where QuestionID NOT IN (1,2,3,4,5) and " + personID + "='")
    information_list = []

    for value in db_list:
        id = value[0] # relies on the database outlined
        cursor.execute(sql_get_info + id + "'")
        fetchall = cursor.fetchall() # More questions means large 2d array
        data_value = [id]
        for row in fetchall:
            data_value.append(row[1])
        information_list.append(data_value)

    return information_list

def compatibility(tutor_matrix, student_matrix):
    '''
    Making a list of tutors and students with compatibility score, must be protrayed with the list for each specific day
    This is because if students and tutors are on different days, then they could not be taught together.
    :param tutor_matrix:
    :param student_matrix:
    :return:
    '''
    tutor_student_list = []

    for tutor in tutor_matrix:
    #Looping through tutor List
        tutorID = tutor[0]
    # score indicates the compatibility with the student

        for student in student_matrix:

            score = 0
            studentID = student[0]
            length_student = len(student)

            for index in range(1, length_student):
                score_add = (length_student - index)
                if student[index] == tutor[index]:
                    score += score_add

            compatibility_list =  [tutorID, studentID, score]
            tutor_student_list.append(compatibility_list)

    return (tutor_student_list)

def matching(conn, cursor, tutor_table, student_table, score_table, freedayID, tutorID, studentID, final_table):
    '''
    Fix this crap
    '''
    cn.delete(conn, cursor, score_table)
    cn.delete(conn, cursor, final_table)

    tutor_freetime = person_info_list(cursor, tutor_table, freedayID, tutorID)
    student_freetime = person_info_list(cursor, student_table, freedayID, studentID)
    pairing = compatibility((tutor_freetime), (student_freetime))

    for value_list in pairing:
        cn.add_value(conn, cursor, score_table, value_list)

    try:
        max_student = (len(tutor_freetime)/len(student_freetime)) + 1
    except:
        max_student = 1

    max_pair = max_index(pairing, 2)
    student_teacher_pair = []

    for value in range(max_pair, -1, -1):
        for pair in pairing:
            if (pair[2] == value) and not(in_matrix(student_teacher_pair, pair[1])):
                if amount_matrix(student_teacher_pair, pair[0]) < max_student:
                    student_teacher_pair.append([pair[0], pair[1], freedayID])

    for day_values in student_teacher_pair:
        cn.add_value(conn, cursor, final_table, day_values)

def send_email_matching(cursor, matching, sender, password):

    value_list = cn.get_value_list(cursor, matching)

    tutor_list = []
    student_list = []
    freeday_list = []

    for value in value_list:
        tutor_list.append(value[0])
        student_list.append(value[1])
        freeday_list.append(value[2])

    tutor_tuple = tuple(tutor_list)
    student_tuple = tuple(student_list)
    freeday_tuple = tuple(freeday_list)

    sql_tutor = ("Select Email, TutorID from Tutor where TutorID IN{}").format(tutor_tuple)
    tutor_email_list = cn.select_where(cursor, sql_tutor)

    sql_student = ("Select Email, StudentID from Student where StudentID IN{}").format(student_tuple)
    student_email_list = cn.select_where(cursor, sql_student)

    sql_freeday = ("Select freeday, FreedayID from freeday where freedayID IN{}").format(freeday_tuple)
    freeday_list = cn.select_where(cursor, sql_freeday)

    send_email_pair(value_list, tutor_email_list, student_email_list, freeday_list, sender, password)

def send_email_pair(value_list, tutor_email_list, student_email_list, freeday_list, sender, password):

    error_list = []
    for value in value_list:
        for tutor in tutor_email_list:
            if tutor[1] == value[0]:
                tutor_email = tutor[0]
        for student in student_email_list:
            if student[1] == value[1]:
                student_email = student[0]
        for freeday in freeday_list:
            if freeday[1] == value[2]:
                freeday_pair = freeday[0]

        pairing_list = [tutor_email, student_email]
        subject = "Pairing"
        message = tutor_email, student_email, freeday_pair

        error = e.send_multiple(sender, password, pairing_list, subject, message)
        error_list.append(error)

    return

if __name__ == "__main__":

    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'

    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'
    subject = "Nani"
    message = '''
     I love CS
     '''

    email_address = os.environ.get("DB_USER")
    email_pass = os.environ.get("DB_PASS")

    conn, curr = cn.connect(user_host, user_login, password, schema)
    cn.delete(conn, curr, "schedule")
    cn.delete(conn, curr, "Matching")
    matching(conn, curr, "AnswerTutor", "AnswerStudent", "Matching", "5", "TutorID", "StudentID","schedule")
    send_email_matching(curr, "schedule", email_address, email_pass)

