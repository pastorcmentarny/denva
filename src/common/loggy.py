import logging
logger = logging.getLogger('app')

def log_error_count(errors):
    number_of_errors = len(errors)
    if number_of_errors >= 2:
        logger.error('Found {} error(s).'.format(len(errors)))
    elif number_of_errors > 0:
        logger.warning('Found {} error(s).'.format(len(errors)))
    else:
        logger.debug('No errors found.')


def log_time(what:str,start_time,end_time):
    logger.info('{} took {} ms.'.format(what, int((end_time - start_time) * 1000)))