import sqlite3
import logging
from datetime import datetime
from contextlib import closing

logger = logging.getLogger('app')

# constants
DB_NAME = "/home/pi/knyszogar/db/denva.db"
STATUS_ROWS = 19
SERVICE_TABLE = 'service_status'


def update_for(what: str):
    try:
        if what.endswith('_device'):
            logger.warning(f'Unable to update for {what}')
            return
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                now = datetime.now()
                current_data = str(
                    f'{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}')

                cursor.execute("UPDATE service_status SET last_updated = ? WHERE service = ?", (current_data, what))
            logger.debug(f'Total changes :{connection.total_changes}')
            connection.commit()
            logger.debug(f'{what} updated to {current_data}')
    except sqlite3.Error as error:
        logger.error(f"Didn't get status for {what}  due to database error {error}", exc_info=True)
    except Exception as exception:
        logger.error(f"Didn't get update status for {what} due to exception {exception}", exc_info=True)


def get_status_for(what: str):
    logger.debug(f'Getting status (last updated) for {what}')
    try:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                logger.debug(f'Total changes before:{connection.total_changes}')
                result = cursor.execute("SELECT service, last_updated FROM service_status WHERE service = ?",
                                        (what,)).fetchall()
                logger.warning(f'Status for {what} is {result}')
                return result[1]
            logger.debug(f'Total changes after:{connection.total_changes}')
    except sqlite3.Error as error:
        logger.error(f"Didn't get status for {what}  due to database error {error}",
                     exc_info=True)
    except Exception as exception:
        logger.error(f"Didn't get update status for {what} due to exception {exception}",
                     exc_info=True)


def set_device_on(device_name: str):
    if device_name.endswith("_device"):
        set_device_status_to(device_name, "OK")
    else:
        print(f'Unable to update for {device_name}')


def set_device_off(device_name: str):
    if device_name.endswith("_device"):
        set_device_status_to(device_name, "OFF")
    else:
        print(f'Unable to update for {device_name}')


def set_device_status_to(device_name: str, device_state: str):
    try:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("UPDATE service_status SET last_updated = ? WHERE service = ?",
                               (device_state, device_name))
                print(connection.total_changes)
            print(f'Total changes :{connection.total_changes}')
            connection.commit()
    except sqlite3.Error as error:
        logger.error(f"Didn't update status for {device_name} to {device_state} due to database error {error}",
                     exc_info=True)
    except Exception as exception:
        logger.error(f"Didn't update status for {device_name} to {device_state} due to exception {exception}",
                     exc_info=True)


def self_test():
    try:
        print('TEST started')
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                rows = cursor.execute("SELECT 1").fetchall()
                print(f'Test result: {rows}')
                table_name = 'service_status'
                query = f"SELECT COUNT(*) FROM {table_name}"
                cursor.execute(query)
                result = cursor.fetchone()
                row_count = result[0]
                if int(row_count) == STATUS_ROWS:
                    logger.info(f'Row count is correct {row_count}')
                else:
                    logger.warning(f'It should be {STATUS_ROWS} rows but there are {row_count}')
        print('TEST stopped')
    except sqlite3.Error as error:
        logger.error(f"During test connection database attacked with error {error}", exc_info=True)
    except Exception as exception:
        logger.error(f"During test connection application blew up with exception {exception}", exc_info=True)


if __name__ == '__main__':
    self_test()
