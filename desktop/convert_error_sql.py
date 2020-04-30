import re

ERRORS_SQL = {
    18456: "Попытка соединения отклонена в результате сбоя проверки подлинности из-за неправильного имени или пароля."
}


def convert_error_sql(error: str) -> tuple:
    """
    This function convert error returned by ODBC and returns processed error
    """
    result = re.search(r"\([\d]+\)", error)
    error_number = int(re.sub(r'[()]', r'', result.group(0)))
    error_msg = ERRORS_SQL.get(error_number, None)

    return error_number, error_msg
