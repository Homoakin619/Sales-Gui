from mysql.connector import connect
def db_connect():
    connection = connect(
            host = "localhost",
            username = "root",
            password = "",
            database = "Mystore"
        )
    return connection
    
