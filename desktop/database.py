import pyodbc


class Database:
    def __init__(self):
        self.connection = None

    def connect_db(self, server: str, database: str, name: str, password: str, autocommit: bool = False,
                   timeout: int = 4) -> pyodbc.Connection:
        """
        This function connects to database and returns connection object
        """

        self.connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}", server=server, database=database,
                                         uid=name, pwd=password, autocommit=autocommit, timeout=timeout)

        return self.connection
