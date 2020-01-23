import random

names = [
    'getLogsAsSourceRecords()',
    'findElement()',
    'clickElement()',
    'waitUntilVisible()'
]


def get_random_method_name() -> str:
    return names[random.randint(0,len(names)-1)]
