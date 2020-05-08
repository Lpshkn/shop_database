import datetime
import decimal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDateTime


class TableWidget(QTableWidget):
    def __init__(self, parent, connection, table_name):
        super().__init__(parent)

        self.setObjectName(table_name)

        self.connection = connection
        self.table_name = table_name

        self.update_table(table_name)
        self.update_configurations()

    def update_configurations(self, section_size=250):
        """
        This method updates dimensions of columns, sets configurations to both headers etc.
        """
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setDefaultSectionSize(section_size)

    def update_table(self, table_name):
        self.clear()
        self.setColumnCount(0)
        self.setRowCount(0)

        self.set_columns(table_name)
        self.set_values(table_name)

    def set_columns(self, table_name):
        """
        This method gets all names of columns and configures the columns into the table
        """
        cursor = self.connection.cursor()
        columns = cursor.execute(
            f"""
            SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """).fetchall()
        columns = [column[0] for column in columns]

        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

    def set_values(self, table_name):
        """
        This method gets all values for columns and set rows into the table
        """
        cursor = self.connection.cursor()
        rows = cursor.execute(
            f"""
            SELECT *
                FROM {table_name}
            """).fetchall()

        # Create empty rows to fill them later
        self.setRowCount(len(rows))

        # Set all values from the columns
        for index, row in enumerate(rows):
            for column in range(self.columnCount()):
                # Get a value from the column
                value = row[column]

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
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.setItem(index, column, item)

    def get_columns(self, selected: bool = False) -> list:
        """
        This method returns the list of column names

        :param selected: it's a flag which specify that only selected columns will be taken, else all columns will be taken
        :return: list of column names
        """
        if selected:
            selected_items = self.selectedItems()
            columns_indexes = set(item.col() for item in selected_items)
            columns = [self.horizontalHeaderItem(i) for i in columns_indexes]
        else:
            columns = [self.horizontalHeaderItem(i) for i in range(self.columnCount())]

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

        for index_row in rows_to_delete:
            # Make a delete query
            conditions = []
            delete_query = f"DELETE FROM {self.table_name} WHERE "

            # Iterate through the columns and append the conditions to delete the appropriate tuple
            for index_col in range(self.columnCount()):
                item_text = self.item(index_row, index_col).text()
                column_name = self.horizontalHeaderItem(index_col).text()
                if item_text:
                    condition = f"{column_name} = '{item_text}'"
                else:
                    condition = f"{column_name} IS NULL"
                conditions.append(condition)

            # Concatenate whole list of conditions into the one query
            delete_query += ' AND '.join(conditions)
            cursor.execute(delete_query).commit()
