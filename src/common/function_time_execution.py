import datetime


# TODO use it
def execution_time(func):
    def wrapper():
        start_time = datetime.datetime.now()

        val = func()

        end_time = datetime.datetime.now()

        time_diff = (end_time - start_time)
        result = time_diff.total_seconds() * 1000
        print(f'It took {result} ms.')

        return val

    return wrapper
