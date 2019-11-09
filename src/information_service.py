import web_data

information = {
    "crimes": "unknown",
    "floods": "unknown",
    "weather": "unknown",
}


def get_data_about_rickmansworth() -> dict:
    information['crimes'] = web_data.get_crime()
    information['floods'] = web_data.get_flood()
    information['weather'] = web_data.get_weather()
    information['o2'] = web_data.get_o2_status()
    return information
