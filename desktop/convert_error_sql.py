import re
import desktop.database as db


def process_error_sql(error: str) -> str:
    """
    This function processes error returned by ODBC and returns processed error
    """
    error_msg = re.sub(r"\[[\w\s-]+\]", r"", error[1])
    msgs = []
    for msg in re.split(r'\.[\b]', error_msg):
        msg = msg.strip()
        msg = msg[0].upper() + msg[1:]
        msgs.append(msg)

    # Translate the table names
    error_msg = '. '.join(msgs)
    for table_name in db.TABLES.keys():
        if table_name in error_msg:
            error_msg = re.sub(r'"[\w]+\.[\w]+\.{0}"'.format(table_name), '"{0}"'.format(db.TABLES.get(table_name, table_name)), error_msg)
            break

    # Translate the column names
    for column_name in db.COLUMNS.keys():
        if column_name in error_msg:
            error_msg = re.sub(r'"{0}"'.format(column_name), '"{0}"'.format(db.COLUMNS.get(column_name, column_name)), error_msg)
            break

    return error_msg
