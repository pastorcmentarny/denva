def get_records_as_dict(measurements_list):
    measurements_data = {
        'lowest_ax': 16777216,
        'highest_ax': -16777216,
        'lowest_ay': 16777216,
        'highest_ay': -16777216,
        'lowest_az': 16777216,
        'highest_az': -16777216,
        'lowest_gx': 16777216,
        'highest_gx': -16777216,
        'lowest_gy': 16777216,
        'highest_gy': -16777216,
        'lowest_gz': 16777216,
        'highest_gz': -16777216,
        'lowest_mx': 16777216,
        'highest_mx': -16777216,
        'lowest_my': 16777216,
        'highest_my': -16777216,
        'lowest_mz': 16777216,
        'highest_mz': -16777216,
        'fastest_measurement_time': 16777216,
        'slowest_measurement_time': 0
    }

    for entry in measurements_list:
        for field_key in measurements_data.keys():
            a_key = field_key.replace("slowest_", "").replace("highest_", "").replace("fastest_", "").replace("lowest_","")

            print(
                f'D. field {field_key} with data {measurements_data[field_key]} :: key {a_key} with data {entry[a_key]}')
            if field_key.startswith("fastest_"):
                print(f"fastest {entry[a_key]} = {measurements_data[field_key]}")
                if measurements_data[field_key] > entry[a_key]:
                    measurements_data[field_key] = entry[a_key]
                    print(f'update fastest {field_key} with {measurements_data[field_key]}')
            elif field_key.startswith("slowest_"):
                print(f"slowest {entry[a_key]} = {measurements_data[field_key]}")
                if measurements_data[field_key] < entry[a_key]:
                    measurements_data[field_key] = entry[a_key]
                    print(f'update slowest {field_key} with {measurements_data[field_key]}')
            elif field_key.startswith("highest_"):
                print(f"{a_key} {entry[a_key]} = {field_key} {measurements_data[field_key]}")
                if entry[a_key] > measurements_data[field_key]:
                    measurements_data[field_key] = entry[a_key]
                    print(f'update higest {field_key} with {measurements_data[field_key]}')
            elif field_key.startswith("lowest_"):
                if entry[a_key] < measurements_data[field_key]:
                    measurements_data[field_key] = entry[a_key]
            else:
                print(
                    f'Interesting. field {field_key} with data {measurements_data[field_key]} :: key {a_key} with data {entry[a_key]}')
    return measurements_data
