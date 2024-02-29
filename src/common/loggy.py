import logging

logger = logging.getLogger('app')


def log_error_count(errors):
    number_of_errors = len(errors)
    if number_of_errors >= 2:
        logger.warning(f'Found {len(errors)} errors. Errors: {str(errors)}')
    elif number_of_errors > 0:
        logger.info(f'Found {len(errors)} error. Errors: {str(errors)}')
    else:
        logger.debug('No errors found.')


def log_time(what: str, start_time, end_time):
    logger.info(f'{what} took {int((end_time - start_time) * 1000)} ms.')


def log_with_print(msg: str, warning: bool = False):
    if warning:
        logger.warning(msg)
    else:
        logger.info(msg)
    print(msg)
