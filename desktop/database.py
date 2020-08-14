import pyodbc


class Database:
    def __init__(self):
        self.connection = None

    @staticmethod
    def connect_db(server: str, database: str, name: str, password: str, autocommit: bool = False,
                   timeout: int = 4, driver: str = "DRIVER={ODBC Driver 17 for SQL Server}",
                   trusted_connection='no'):
        """
        This method connects to the database and returns the connection object.

        :param server: the name of the server to connect
        :param database: the name of the database contained on the server and which you want to connect
        :param name: the name of the user which will be connected to the database
        :param password: the password of the user
        :param autocommit: the flag which specifies that each query will be committed immediately
        :param timeout: time what the server will wait while connecting
        :param driver: the driver of the ODBC to connect to the database using this driver
        """

        db_object = Database()
        db_object.connection = pyodbc.connect(driver, server=server, database=database,
                                              uid=name, pwd=password, trusted_connection=trusted_connection, autocommit=autocommit, timeout=timeout)

        return db_object
