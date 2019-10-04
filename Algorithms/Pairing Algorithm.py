### Paring algorithm, I need to do this in 3 hours esketit


## Standard Library Immports
import sys
sys.path.append("Imported")
import Connector as cn

def dd_array(col,row):
    """
    Returns a 2d array with specifics dimensions.
    :param width:
    :param length:
    :return:
    """

    empty = [None]
    array = [empty*row] * col
    return(array)


def person_info_list(cursor, table, QuestionID, freeday, PersonID):
    """
    ("SELECT " + return_value + " From " + table + " Where " + column + " " + condition + ' "' + equal_to + '"' )
    :param array:
    :return:
    """
    sql = ("SELECT " + PersonID + " From " + table + " Where QuestionID=" + QuestionID + " and " \
           "Answers='" + freeday +"'")

    cursor.execute(sql)
    db_list = cursor.fetchall()

    sql_get_info = ("SELECT " + PersonID+ ",QuestionID, Answers From " + table + " where QuestionID != 1 and " +\
                    PersonID + "='")

    information_list = []

    for value in db_list:
        tutorID = value[0] # relies on the database outlined

        cursor.execute(sql_get_info + tutorID + "'")

        fetchall = cursor.fetchall()

        data_value = [tutorID]
        for row in fetchall:

            data_value.append(row[2])

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
        """
        Looping through the tutor list
        """
        tutorID = tutor[0]
        score = 0 # score indicates the compatibility with the student

        for student in student_matrix:
            studentID = student[0]
            for index in range(1, len(student)):
                if student[index] == tutor[index]:
                    score += 1

            compatibility_list =  [tutorID, studentID, score]
            tutor_student_list.append(compatibility_list)

    return (tutor_student_list)

def add_data(conn, cursor, table, input_list):

    for value_list in input_list:
        cn.add_value(conn, cursor, table, value_list)

def matching():
    '''

    '''


if __name__ == "__main__":

    SPACE_HOLDER = "%s,"
    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'

    conn, curr = cn.connect(user_host, user_login, password, schema)

    tutor_freetime = person_info_list(curr, "AnswerTutor", "1", "Thursday", "TutorID")
    student_freetime = person_info_list(curr, "AnswerStudent", "1", "Thursday", "StudentID")


    pairing = compatibility((tutor_freetime), (student_freetime))

    add_data(conn, curr, "Matching", pairing)

    print(cn.get_value_list(curr, "Matching"))


    # curr.execute("Delete from matching")
    # conn.commit()

'''
If you are presenting on a different platform, it must be one application
Shw database on school server
Succes Crit = script
Make Slider
'''