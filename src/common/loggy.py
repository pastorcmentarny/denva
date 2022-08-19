import logging

logger = logging.getLogger('app')


def log_error_count(errors):
    number_of_errors = len(errors)
    if number_of_errors >= 2:
        logger.error('Found {} errors. Errors: {}'.format(len(errors), str(errors)))
    elif number_of_errors > 0:
        logger.warning('Found {} error. Errors: {}'.format(len(errors), str(errors)))
    else:
        logger.debug('No errors found.')


def log_time(what: str, start_time, end_time):
    logger.info('{} took {} ms.'.format(what, int((end_time - start_time) * 1000)))


def log_with_print(msg: str, warning: bool = False):
    if warning:
        logger.warning(msg)
    else:
        logger.info(msg)
    print(msg)
