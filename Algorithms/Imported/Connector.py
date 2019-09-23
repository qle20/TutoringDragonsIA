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

def get_data(cursor, select):

    cursor.execute("SELECT " + select)
    data = curr.fetchall()

    return data

def get_value_list(cursor, table, index):
    '''
    This function collects a certain value in a specified table, in wchi returns it as a list.
    :param cursor:
    :param table:
    :param index:
    :return:
    '''
    cursor.execute("SELECT * FROM " + table)
    db_list = cursor.fetchall()

    value_list = []

    for i in db_list:
        value_list.append(i[index])

    return value_list

def add_value(cursor, ):
    ""

if __name__ == '__main__':

    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'

    connection, curr = connect(user_host, user_login, password, schema)

    get_value_list(curr, "Tutor",  1)

    end_connection(connection)
