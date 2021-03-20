import sys
from pathlib import Path

from common import data_files

if __name__ == '__main__':
    data_files.setup_logging('overseer_mode')
    status_filepath = Path(r"D:\overseer_mode.txt")
    with open(status_filepath, 'w') as status_file:
        if len(sys.argv) == 2:
            print(f'Updating {sys.argv[0]} with {sys.argv[1]}')
            status_file.write(str(sys.argv[1]))
        else:
            print(f'Setting back to auto mode')
            status_file.write("")
