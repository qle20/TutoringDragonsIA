import mysql.connector

def connect(user_host, user_login, password, db):
    '''
    Connects to a database with the parameters given.
    :param user_host:
    :param user_login:
    :param password:
    :param db:
    :return:
    '''
    connection = mysql.connector.connect(host=user_host, user=user_login, passwd=password, database=db)
    curr = connection.cursor()

    return connection, curr

def end_connection(connection):

    connection.close()

def get_value_list(cursor, table, index=None):
    '''
    This function collects a certain value in a specified table, returns it as a list.
    :param cursor:
    :param table:
    :param index:
    :return:
    '''

    cursor.execute("SELECT * FROM " + table)
    db_list = cursor.fetchall()

    if index != None:
        value_list = []

        for i in db_list:
            value_list.append(i[index])

        return value_list
    return(db_list)


def add_value(conn, cursor, table, values):
    """
    Insert values into table, with the values inserted being arrays
    """

    SPACE_HOLDER = "%s,"
    sql = "INSERT INTO " + table + " VALUES(" + SPACE_HOLDER*(len(values) - 1 ) + "%s" + ")"

    cursor.execute(sql, values)
    conn.commit()

def delete_value(conn, cursor, table, column='', condition=''):
    """
    Delete Stuff
    :param conn:
    :param cursor:
    :param table:
    :param coloum:
    :param where:
    :return:
    """

    sql = "DELETE FROM " + table + " WHERE " + column + '="' + condition +'"'

    cursor.execute(sql)
    conn.commit()

if __name__ == '__main__':

    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'

    connection, curr = connect(user_host, user_login, password, schema)
    #
    #
    # sql = "INSERT INTO Tutor (TutorID, Email, Name) VALUES(" + SPACE_HOLDER * 2 +"%s" +")"
    # print(sql)
    # val = ('T5', "dsdf", "Yong wan")
    # curr.execute(sql, val)
    # connection.commit()
    #
    #
    # get_value_list(curr, "Tutor",  1)
    #
    # end_connection(connection)

    # add_value(connection, curr, "Tutor", values = ('T6', "dsdf", "Yong wan"))
    # print(get_value_list(curr, "Tutor"))
    # delete_value(connection, curr, "Tutor", "TutorID", "T6")
    # print(get_value_list(curr, "Tutor"))

    print(select_certain_value(curr, "AnswerTutor", "Answers", "Friday"))

    end_connection(connection)
