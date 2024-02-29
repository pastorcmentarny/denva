import random

stopping_pattern = ['all stations', 'semi-fast', 'fast']
destination = ['Amersham', 'Chesham', 'Watford', 'Uxbridge', 'Baker Street', 'Aldgate']
next_station = ['Aldgate', 'Amersham', 'Baker Street', 'Barbican', 'Chalfont & Latimer', 'Chesham', 'Chorleywood',
                'Croxley', 'Eastcote', 'Euston Square', 'Farringdon', 'Great Portland Street', 'Harrow-on-the-Hill',
                'Hillingdon', 'Ickenham', 'King\'s Cross St. Pancras', 'Liverpool Street', 'Moor Park', 'North Harrow',
                'Northwick Park', 'Northwood', 'Northwood Hills', 'Pinner', 'Preston Road', 'Rayners Lane',
                'Rickmansworth', 'Ruislip', 'Ruislip Manor', 'Uxbridge', 'Watford', 'Wembley Park', 'West Harrow']


def get_stopping_pattern_type():
    return stopping_pattern[random.randint(0, len(stopping_pattern) - 1)]


def get_destination():
    return destination[random.randint(0, len(destination) - 1)]


def get_random_station():
    return next_station[random.randint(0, len(next_station) - 1)]


def add_randomly_mind_the_gap():
    if bool(random.getrandbits(1)):
        return 'Mind the gap between the train and the platform.'
    return ''


def add_rear_door_not_open_this(selected_station):
    if selected_station in ['Barbican', 'Great Portland Street']:
        return 'The rear door will not open here.Please use other doors'
    return ''


def add_rear_door_not_open_next(selected_station):
    if selected_station in ['Barbican', 'Great Portland Street']:
        return 'The rear door will not open at the next station.Please use other doors'
    return ''


def generate() -> str:
    selected_stopping_pattern = get_stopping_pattern_type()
    selected_destination = get_destination()
    selected_station = get_random_station()
    return f'This is {selected_stopping_pattern} Metropolitan line service to {selected_destination}. The next station is {selected_station}.{add_rear_door_not_open_next(destination)}.{add_randomly_mind_the_gap()}'


if __name__ == '__main__':
    print(generate())

#     return Platform 6 , for the 12:00 service to Aylesbury Vale Parkway. Calling at: Rickmansworth, Chorleywood, Amersham , Great Missenden, Wendover, Stoke Mandeville, Aylesbury and Aylesbury Vale Parkway.This train si formed of 6 carriages.
# MESSAGE = "This is a semi-fast Metropolitan line service to Amersham.The next station is Rickmansworth.The service is from Aldgate. Calling at: Rickmansworth, Chorleywood, Chalfont & Latimer and Amersham."
# MESSAGE = "This is a semi-fast Metropolitan line service to Amersham.The next station is Rickmansworth.The service is from Aldgate. Calling at: Liverpool Street, Moorgate, Barbican, Farringdon, King's Cross St. Pancras, Euston Square, Great Portland Street, Baker Street, Finchley Road, Wembley Park, Preston Road, Northwick Park, Harrow-on-the-Hill, North Harrow, Pinner, Northwood Hills, Northwood, Moor Park, Rickmansworth, Chorleywood, Chalfont & Latimer and Amersham."
# MESSAGE = "Platform 6 , for the 12:00 service to Aylesbury Vale Parkway. Calling at: Rickmansworth, Chorleywood, Amersham , Great Missenden, Wendover, Stoke Mandeville, Aylesbury and Aylesbury Vale Parkway.This train si formed of 6 carriages."
