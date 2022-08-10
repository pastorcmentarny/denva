from datetime import datetime as dt

"""
Service to write down all events that happen
"""
ENCODING = 'utf-8'


def add(new_entry):
    path = f"diary-{dt.year}-{dt.month:02d}-{dt.day:02d}.txt"
    with open(path, "w", encoding=ENCODING) as diary_file:
        diary_file.write(new_entry)
