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
    try:
        connection = mysql.connector.connect(
            host=str(user_host),
            user=str(user_login),
            passwd=str(password),
            database=str(db)
        )
        curr = connection.cursor()
        return connection, curr

    except mysql.connector.Error as err:
        print("Stuff went south: {}".format(err))

def end_connection(connection):
    '''
    :param connection:
    :return:
    '''
    connection.close()

def get_value_list(cursor, table, index=None):
    '''
    This function collects a certain value in a specified table, returns it as a list.
    :param cursor:
    :param table:
    :param index:
    :return:
    '''
    try:
        cursor.execute("SELECT * FROM " + table)
        db_list = cursor.fetchall()
        length_list_index = len(db_list[0]) - 1
        if (db_list != [] and index != None) and length_list_index >= index:
            value_list = []
            for i in db_list:
                value_list.append(i[index])
            return value_list
        else:
            return (db_list)

    except mysql.connector.Error as err:
        print("Stuff went south: {}".format(err))


def add_value(conn, cursor, table, values):
    """
    Insert values into table, with the values inserted being arrays
    """
    SPACE_HOLDER = "%s,"
    sql = "INSERT INTO " + table + " VALUES(" + SPACE_HOLDER*(len(values) - 1 ) + "%s" + ")"
    try:
        cursor.execute(sql, values)
        conn.commit()
    except mysql.connector.Error as err:
        print("Stuff went south: {}".format(err))

def delete(conn, cursor, table, column=None, condition=None):
    """
    """
    if column != None:
        sql = "DELETE FROM " + table + " WHERE " + str(column) + '="' + str(condition) + '"'
    else:
        sql = "DELETE FROM " + table
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        print("Stuff went wrong:{}".format(err))

def convert(question_list):

    for question_index in range(len(question_list)):
        question_list[question_index] = list(question_list[question_index])
        if question_list[question_index][2] == 2:
            question_list[question_index][3] = question_list[question_index][3].split(",")
    return question_list

def combine(list, index):

    new_list = []
    for value in list:
        new_list.append(value[index])

    return(new_list)

if __name__ == '__main__':

    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'

    connection, curr = connect(user_host, user_login, password, schema)
    question_list = get_value_list(curr, "Questions Order By QuestionID")

    convert(question_list)

    end_connection(connection)
