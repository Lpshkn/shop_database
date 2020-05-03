from PyQt5.QtWidgets import QTableWidget


class TableWidget(QTableWidget):
    def __init__(self, parent, connection, table_name):
        super().__init__(parent)

        self.connection = connection
        self.table_name = table_name

        self.set_columns(table_name)
        self.update_configurations()

    def update_configurations(self, section_size=250):
        """
        This method updates dimensions of columns, sets configurations to both headers etc.
        """
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
