import os
import shutil

from utils import dom_utils

FROM = "D:\\Projects\\denva\\src"
TO = "\\ds-lpd-server\\denva\\src"
BACKUP = 'D:\\denva\\backup'

'''this script is used to copy project locally to my server'''


def backup():
    print('Performing backup..')
    dom_utils.get_timestamp_title()
    backup_path = BACKUP + dom_utils.get_date_as_folders()
    print(backup_path)
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    print('Coping files')
    result = shutil.copytree(TO, BACKUP)
    print('Backup complete. {}'.format(result))

def update():
    backup()
    """
        if os.path.exists(TO):

        shutil.rmtree(TO)
        result = shutil.copytree(FROM, TO)
        print(result)

    """

if __name__ == '__main__':
    update()