import os
import shutil

from common import dom_utils

FROM = "D:\\GitHub\\denva\\src\\"
TO = '\\\\DS-LPD-SERVER\\denva\\src\\'
BACKUP = '\\\\DS-LPD-SERVER\\denva\\backup\\project\\'


def update_server():
    print('Performing backup..')
    dom_utils.get_timestamp_title()
    backup_path = BACKUP + dom_utils.get_date_as_folders()
    print(backup_path)
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)


    # copy logs ,reports to
    source = '\\\\DS-LPD-SERVER\\denva\\data\\'
    destination = 'D:\\denva\\backup\\test\\'
    for folderName, subFolders, filenames in os.walk(source):
        print('The current folder is ' + folderName)

        for subFolder in subFolders:
            print('SUBFOLDER OF ' + folderName + ': ' + subFolder)
        for filename in filenames:
            print('FILE INSIDE ' + folderName + ': ' + filename)
            result = shutil.copy(folderName +  "\\" + filename, destination)
            print(result)
        print('')


if __name__ == '__main__':
    update_server()