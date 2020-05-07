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

        self.set_columns(table_name)
        self.set_values(table_name)
        self.update_configurations()

    def update_configurations(self, section_size=250):
        """
        This method updates dimensions of columns, sets configurations to both headers etc.
        """
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setDefaultSectionSize(section_size)

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
                condition = f"{column_name} = '{item_text}'"
                conditions.append(condition)

            # Concatenate whole list of conditions into the one query
            delete_query += ' AND '.join(conditions)
            cursor.execute(delete_query)
