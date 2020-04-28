import pyodbc
import sys
from PyQt5.QtWidgets import (QApplication)
from desktop.main_window import MainWindow


def main():
    server = 'DESKTOP-L10LTBT\SQLEXPRESS'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}',
                          server=server,
                          database='shopdb',
                          trusted_connection='yes',
                          autocommit=True)

    cursor = conn.cursor()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
