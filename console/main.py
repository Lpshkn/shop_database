import psycopg2
import stdiomask
from terminaltables import SingleTable

stop = {
    'stop'
}


def main():
    host = 'localhost'
    port = 49678
    dbname = 'shopdb'
    user = input('[ db user ] ')
    password = stdiomask.getpass(prompt='[ db password ] ', mask='*')

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    while True:
        request = input('[ SQL ] ')
        if request in stop:
            break

        cur = conn.cursor()
        cur.execute(request)
        if not cur.description:
            conn.commit()
            print('<<< OK')
            continue

        headers = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        table = SingleTable([headers, *rows])
        print(table.table)


if __name__ == '__main__':
    main()