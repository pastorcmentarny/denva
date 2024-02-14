import sqlite3
from contextlib import closing
from datetime import datetime

default_hc = {
    "denva_app": "20201212201221",
    "denva_ui": "20201212201221",
    "denva_device": 'OFF',
    "denva2_ui": "20201212201221",
    "denva2_motion": "20201212201221",
    "denva2_gps": "20201212201221",
    "denva2_barometric": "20201212201221",
    "denva2_spectrometer": "20201212201221",
    "denva2_sound": "20201212201221",
    "denva2_device": 'OFF',
    "server_app": "20201212201221",
    "server_ui": "20201212201221",
    "server_device": 'OFF',
    "cctv": "20201212201221",
    "knyszogar_hc": "20201212201221",
    "knyszogar_radar": "20201212201221",
    "knyszogar_digest": "20201212201221",
    "knyszogar_app": "20201212201221",
    "knyszogar_email": "20201212201221",
    "knyszogar_config": "20201212201221",
}
DB_NAME = "/home/pi/knyszogar/db/denva.db"

def count_size():
    connection = sqlite3.connect(DB_NAME)
    table_name = 'service_status'
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    print(f"ROW COUNT: {row_count}")
    cursor.close()
    connection.close()


def setup():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='service_status'")
    cursor.execute("CREATE TABLE service_status (service TEXT, last_updated TEXT)")

    for key in default_hc.keys():
        if key.endswith('_device'):
            params_data = [key, 'OFF']
            cursor.execute("INSERT INTO service_status VALUES (?, ?)", params_data)
        else:
            params_data = [key, '20201212201221']
            cursor.execute("INSERT INTO service_status VALUES (?, ?)", params_data)

    test1 = 'denva_app'
    rows1 = cursor.execute("SELECT service, last_updated FROM service_status WHERE service = ?",
                           (test1,), ).fetchall()
    test2 = 'denva_device'
    rows2 = cursor.execute("SELECT service, last_updated FROM service_status WHERE service = ?",
                           (test2,), ).fetchall()

    test3 = 'denva_app'
    now = datetime.now()
    current_data = str('2021{:02d}{:02d}{:02d}{:02d}{:02d}'
                       .format(now.month, now.day, now.hour, now.minute, now.second))
    cursor.execute("UPDATE service_status SET last_updated = ? WHERE service = ?",
                   (current_data, 'denva_app'))
    rows3 = cursor.execute("SELECT service, last_updated FROM service_status WHERE service = ?",
                           (test1,), ).fetchall()

    test4 = 'denva_device'
    current_state = 'ON'
    cursor.execute("UPDATE service_status SET last_updated = ? WHERE service = ?",
                   (current_state, 'denva_device'))
    rows4 = cursor.execute("SELECT service, last_updated FROM service_status WHERE service = ?",
                           (test2,), ).fetchall()
    print(rows1)
    print(rows2)
    print(rows3)
    print(rows4)
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    print(f"ROW COUNT: {row_count}")
    cursor.execute('SELECT SQLITE_VERSION()')
    data = cursor.fetchone()
    print('SQLite version:', data)
    connection.commit()
    cursor.close()
    connection.close()


def add_row(key: str):
    try:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                if key.endswith('_device'):
                    params_data = [key, 'OFF']
                    cursor.execute("INSERT INTO service_status VALUES (?, ?)", params_data)
                else:
                    params_data = [key, '20201212201221']
                cursor.execute("INSERT INTO service_status VALUES (?, ?)", params_data)
                print(f'Total changes :{connection.total_changes}')
                connection.commit()
    except sqlite3.Error as error:
        print(f"Unable to add row for {key} due to database error {error}")
    except Exception as exception:
        print(f"Unable to add row for {key} due to database error {exception}")


if __name__ == '__main__':
    add_row('knyszogar_config')

