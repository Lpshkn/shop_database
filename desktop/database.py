import pyodbc


class Database:
    def __init__(self):
        self._connection = None
        # This is the default schema for the database, and if it's necessary to change it, you must change this value
        self._schema = 'dbo'
        # The list contains all query which must be executed
        self._queries = []

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
        db_object._connection = pyodbc.connect(driver, server=server, database=database,
                                              uid=name, pwd=password, trusted_connection=trusted_connection, autocommit=autocommit, timeout=timeout)

        return db_object

    def get_columns(self, table_name: str) -> list:
        """
        This method gets columns names of the table. It takes columns names from the database using the table name.

        :param table_name: take the columns' names from this table
        :return: list of the columns' names
        """
        query = f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                """

        self.add_query(query)
        executed_query = self.execute_query()
        columns = executed_query.fetchall()
        columns = [column[0] for column in columns]

        return columns

    def get_rows(self, table_name: str) -> list:
        """
        This method gets rows values of the table. It takes rows values from the database using the table name.

        :param table_name: take the rows values from this table
        :return: list of rows of this table
        """

        self.add_query(f"SELECT * FROM {table_name}")
        rows = self.execute_query().fetchall()
        return rows

    def delete_tuple(self, table_name: str, rows: list, columns: list = None, force_delete: bool = True):
        """
        This method deletes appropriate rows from the database.

        :param table_name: the name of the table
        :param rows: the rows that will be deleted from the database
        :param columns: the names of columns
        :param force_delete: the flag which specifies that it's important to execute the delete query at the moment
        """
        if columns is None:
            columns = self.get_columns(table_name)

        for row in rows:
            # Make a delete query
            conditions = []
            query = f"DELETE FROM {table_name} WHERE "

            # Iterate through the columns and append the conditions to delete the appropriate tuple
            for column, item in zip(columns, row):
                if item:
                    condition = f"{column} = '{item}'"
                else:
                    condition = f"{column} IS NULL"
                conditions.append(condition)

            # Concatenate whole list of conditions into the one query
            query += ' AND '.join(conditions)
            self.add_query(query)

            if force_delete:
                self.execute_query()

    def get_tables(self):
        """
        Get all names of the tables containing in the database, except of the diagrams system table
        """
        cursor = self._connection.cursor()
        tables = cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME <> 'sysdiagrams' AND TABLE_NAME <> 'systranschemas'
                AND TABLE_SCHEMA = '{0}'
                """.format(self._schema)).fetchall()
        tables = [table[0] for table in tables]
        return tables

    def add_query(self, query: str):
        """
        This method adds the query to the query list. Note, this method doesn't execute the query.
        But this method must be used before executing the query.

        :param query: this query will be added into the query list
        """
        self._queries.append(query)

    def execute_query(self, all_queries: bool = False):
        """
        This method executes the first query containing in the query list. If it executes only one query,
        it will return a result of executed query. Nevertheless, if the flag "all_queries" is True,
        then the method will execute all queries starts from the first and doesn't return anything.

        :param all_queries: specify that if it's necessary to execute all queries in the list
        """
        cursor = self._connection.cursor()

        if all_queries:
            for query in self._queries:
                cursor.execute(query).commit()

        else:
            query = self._queries.pop(0)
            executed_query = cursor.execute(query)
            return executed_query

    def reject_query(self, all_queries: bool = False):
        """
        This method rejects the last query containing in the query list and returns it. If the flag "all_queries"
        is True, then the method will reject all queries in the query list and won't return any.

        :param all_queries: specify that if it's necessary to reject all queries in the list
        """
        if all_queries:
            self._queries.clear()
        else:
            return self._queries.pop()
