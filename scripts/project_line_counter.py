import os.path
import pathlib

line_count = 0
file_count = 0

for path, _, files in os.walk("D:\\GitHub\\denva\\src\\"):
    for name in files:
        file_path = pathlib.PurePath(path, name)
        if str(file_path).endswith(".py"):
            with open(str(file_path), encoding="utf-8") as f:
                file_count += 1
                for line in f:
                    line_count += 1

print("There is a {} files in the project and total count of lines in the project is: {}".format(file_count,line_count))
