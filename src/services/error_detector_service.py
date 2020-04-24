from utils import dom_utils


def get_errors(data: dict) -> list:
    errors = []
    if dom_utils.get_int_number_from_text(data['system']['server']['Memory Available']) < 500:
        errors.append('Memory available on SERVER is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['denva']['Memory Available']) < 128:
        errors.append('Memory available ON DENVA is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['enviro']['Memory Available']) < 128:
        errors.append('Memory available ON ENVIRO is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['delight']['Memory Available']) < 128:
        errors.append('Memory available ON DELIGHT is VERY LOW.')

    if dom_utils.get_int_number_from_text(data['system']['server']['Disk Free']) < 128:
        errors.append('Free space on disk  ON SERVER is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['denva']['Free Space']) < 128:
        errors.append('Free space on disk  ON DENVA is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['enviro']['Free Space']) < 128:
        errors.append('Free space on disk  ON ENVIRO is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['delight']['Free Space']) < 128:
        errors.append('Free space on disk  ON DELIGHT is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['denva']['Data Free Space']) < 256:
        errors.append('Free space on data partition ON DENVA is VERY LOW.')
    if dom_utils.get_int_number_from_text(data['system']['enviro']['Data Free Space']) < 256:
        errors.append('Free space on data partition ON ENVIRO is VERY LOW.')

    return errors
