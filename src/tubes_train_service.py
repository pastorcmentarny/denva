import data_files
import utils


def get_stats_file_for(year: str, month: str, day: str) -> list:
    date = utils.get_filename_for_stats(year, month, day)
    return data_files.load_stats('/home/pi/stats/' + date)


def get_stats_file_for_today() -> list:
    return data_files.load_stats('/home/pi/stats/stats.log')


def count_tube_color_today() -> dict:
    return count_tube_color(get_stats_file_for_today())


def count_tube_color(stats_list) -> dict:
    stats_counter = {
        'Bakerloo': 0,
        'Central': 0,
        'Circle': 0,
        'District': 0,
        'Hammersmith': 0,
        'Jubilee': 0,
        'Metropolitan': 0,
        'Piccadilly': 0,
        'Victoria': 0,
        'Waterloo': 0
    }

    for stat in stats_list:
        if 'Bakerloo line' in stat:
            stats_counter['Bakerloo'] += 1
        elif 'Central line' in stat:
            stats_counter['Central'] += 1
        elif 'Circle line' in stat:
            stats_counter['Circle'] += 1
        elif 'District line' in stat:
            stats_counter['District'] += 1
        elif 'Hammersmith & City line' in stat:
            stats_counter['Hammersmith'] += 1
        elif 'Jubilee line' in stat:
            stats_counter['Jubilee'] += 1
        elif 'Metropolitan line' in stat:
            stats_counter['Metropolitan'] += 1
        elif 'Piccadilly line' in stat:
            stats_counter['Piccadilly'] += 1
        elif 'Victoria line' in stat:
            stats_counter['Victoria'] += 1
        elif 'Waterloo & City line' in stat:
            stats_counter['Waterloo'] += 1

    return stats_counter
