from mysql.connector import connect
def db_connect():
    connection = connect(
            host = "localhost",
            username = "root",
            password = "homoakin619",
            database = "Mystore"
        )
    return connection
    
