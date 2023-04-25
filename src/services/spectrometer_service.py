def check_warning(measurement: dict) -> list:
    warnings = []
    if float(measurement['red']) < 1 and float(measurement['orange']) < 1 and float(measurement['yellow']) < 1 and float(measurement['green']) < 1 and float(measurement['blue']) < 1 and float(measurement['violet']) < 1:
        warnings.append(
            f"Spectrometer returns zeros only Red:{measurement['red']} | Orange:{measurement['orange']} | Yellow:{measurement['yellow']} | Green:{measurement['green']} | Blue:{measurement['blue']} | Violet:{measurement['violet']}|")
    return warnings
