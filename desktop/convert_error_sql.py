import re

ERRORS_SQL = {
    18456: "Попытка соединения отклонена в результате сбоя проверки подлинности из-за неправильного имени или пароля.",
    4060: "Невозможно получить доступ к этой базе данных. Ошибка входа. Проверьте корректность названия базы данных."
}


def convert_error_sql(error: str) -> str:
    """
    This function convert error returned by ODBC and returns processed error
    """
    split_error = error[1].split(';')[-1]

    error_number = re.search(r"\([\d-]+\)", split_error)
    error_number = int(re.sub(r'[()]', r'', error_number.group(0)))

    error_msg = ERRORS_SQL.get(error_number, None)
    if error_msg:
        error_msg = "Ошибка " + str(error_number) + ": " + error_msg
    else:
        error_msg = re.sub(r"(\[[\w\s-]+\])|(\([\w\s-]+\))", r"", split_error)
        error_msg = "Ошибка: " + error_msg.strip()

    return error_msg
