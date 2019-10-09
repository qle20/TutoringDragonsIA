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

    except mysql.connector.Error as err:
        print("Stuff went south: {}".format(err))

    if index != None:
        value_list = []
        for i in db_list:
            value_list.append(i[index])
        return value_list

    return (db_list)

def add_value(conn, cursor, table, values):
    """
    Insert values into table, with the values inserted being arrays
    """
    SPACE_HOLDER = "%s,"
    sql = "INSERT INTO " + table + " VALUES(" + SPACE_HOLDER*(len(values) - 1 ) + "%s" + ")"
    cursor.execute(sql, values)
    conn.commit()

def delete(conn, cursor, table, column=None, condition=None):
    """
    Delete Stuff
    :param conn:
    :param cursor:
    :param table:
    :param coloum:
    :param where:
    :return:
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

if __name__ == '__main__':

    user_host = 'localhost'
    user_login = 'root'
    password = 'razzmatazz'
    schema = 'Test_schema'

    connection, curr = connect(user_host, user_login, password, schema)

    get_value_list(curr, "Tutor", 5)
    end_connection(connection)
