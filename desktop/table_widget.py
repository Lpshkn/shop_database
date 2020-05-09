import datetime
import decimal
from functools import reduce
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDateTime


class TableWidget(QTableWidget):
    def __init__(self, parent, connection, table_name):
        super().__init__(parent)

        self.setObjectName(table_name)

        self.connection = connection
        self.table_name = table_name

        self.update_table()
        self.update_configurations()

    def update_configurations(self, section_size=250):
        """
        This method updates dimensions of columns, sets configurations to both headers etc.
        """
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setDefaultSectionSize(section_size)

    def update_table(self, columns=None, rows=None, flags: list = (Qt.ItemIsSelectable, Qt.ItemIsEnabled)):
        """
        This method provides updating the table. Depending on the passed values methods takes data
        from the database or from the passed data.

        :param columns: it's a list of columns name, which will be set into the table.
                        If it's none, the columns will be taken from the database
        :param rows: it's a list of rows values, which will be set into the table.
                    If it's none, the rows will be taken from the database
        :param flags: a list of flags, which will be applied when setting the cells
        """

        # Clear the previous values of the table
        self.clear()
        self.setColumnCount(0)
        self.setRowCount(0)

        if columns:
            self.set_columns(columns)
        else:
            self.set_columns_from_database(self.table_name)

        if rows:
            self.set_rows(rows, flags)
        else:
            self.set_rows_from_database(self.table_name, flags)

    def set_columns_from_database(self, table_name: str):
        """
        This method sets columns names of the table. It takes columns names from the database using the table name.

        :param table_name: take the columns names from this table
        """

        cursor = self.connection.cursor()
        columns = cursor.execute(
            f"""
            SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """).fetchall()
        columns = [column[0] for column in columns]

        self.set_columns(columns)

    def set_columns(self, columns: list):
        """
        This method sets columns names of the table. It takes columns names from the passed list.

        :param columns: take the columns names from this list
        """

        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

    def set_rows_from_database(self, table_name: str, flags: list):
        """
        This method sets rows values of the table. It takes rows values from the database using the table name.

        :param table_name: take the rows values from this table
        :param flags: a list of flags, which will be applied when setting the cells
        """

        cursor = self.connection.cursor()
        rows = cursor.execute(
            f"""
            SELECT *
                FROM {table_name}
            """).fetchall()

        self.set_rows(rows, flags)

    def set_rows(self, rows: list, flags: list):
        """
        This method sets rows values of the table. It takes rows values from the passed list.

        :param rows: take the rows values from this list
        :param flags: a list of flags, which will be applied when setting the cells
        """

        # Create empty rows to fill them later
        self.setRowCount(len(rows))

        # Set all values from the columns
        for index_row, row in enumerate(rows):
            for index_column in range(self.columnCount()):
                # Get a value from the column
                value = row[index_column]

                # Check that values is instance of Datetime SQL type
                # It's necessary to convert that value to a type that the table understands
                if isinstance(value, datetime.date):
                    date_str = str(value)
                    # If the date string has a space, then there is also time in the date string
                    if ' ' in date_str:
                        value = QDateTime().fromString(date_str, 'yyyy-MM-dd HH:mm:ss')
                    else:
                        value = QDateTime().fromString(date_str, 'yyyy-MM-dd')
                # Convert the "MONEY" type from SQL type to the float type
                elif isinstance(value, decimal.Decimal):
                    value = float(value)

                # Set the value into the cell
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, value)
                # Set flags to disable editing any cell
                item.setFlags(reduce(lambda x, y: x | y, flags))
                self.setItem(index_row, index_column, item)

    def get_columns(self, selected: bool = False) -> list:
        """
        This method returns the list of column names

        :param selected: it's a flag which specify that only selected columns will be taken, else all columns will be taken
        :return: list of column names
        """
        if selected:
            selected_items = self.selectedItems()
            columns_indexes = set(item.col() for item in selected_items)
            columns = [self.horizontalHeaderItem(i).text() for i in columns_indexes]
        else:
            columns = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]

        return columns

    def get_rows(self, selected: bool = False) -> list:
        """
        This method returns the list of rows values

        :param selected: it's a flag which specify that only selected rows will be taken, else all rows will be taken
        :return: list of rows values
        """
        rows = []
        if selected:
            selected_items = self.selectedItems()
            rows_indexes = set(item.row() for item in selected_items)
            for row_index in rows_indexes:
                rows.append([self.item(row_index, col_index).text() for col_index in range(self.columnCount())])
        else:
            for row_index in range(self.rowCount()):
                rows.append([self.item(row_index, col_index).text() for col_index in range(self.columnCount())])

        return rows

    def delete_tuple(self):
        """
        This is a slot, which will be called when user will select any cells and will click the delete button.
        This method deletes appropriate rows from the database.
        """

        cursor = self.connection.cursor()
        # Get numbers of selected cells rows
        selected_items = self.selectedItems()
        rows_to_delete = set(item.row() for item in selected_items)

        for row in self.get_rows(selected=True):
            # Make a delete query
            conditions = []
            delete_query = f"DELETE FROM {self.table_name} WHERE "

            # Iterate through the columns and append the conditions to delete the appropriate tuple
            for column, item in zip(self.get_columns(), row):
                if item:
                    condition = f"{column} = '{item}'"
                else:
                    condition = f"{column} IS NULL"
                conditions.append(condition)

            # Concatenate whole list of conditions into the one query
            delete_query += ' AND '.join(conditions)
            cursor.execute(delete_query).commit()
