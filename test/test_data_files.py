import unittest

from common import data_files


#TODO finish this test
class DataFilesTestCases(unittest.TestCase):
    def test_save_report_at_server(self):
        data = {
            "now": {
                "denva": {
                    "aqi": "n/a",
                    "ax": "-0.01",
                    "ay": "0.02",
                    "az": "-0.01",
                    "colour": "#ffa9c5",
                    "cpu_temp": "49.0",
                    "eco2": "642",
                    "gas_resistance": "12946860.59",
                    "gx": "0.44",
                    "gy": "1.79",
                    "gz": "-0.22",
                    "humidity": "37.687",
                    "motion": "16.46875",
                    "mx": "-85.35",
                    "my": "54.00",
                    "mz": "-57.30",
                    "pressure": "997.87",
                    "temp": "25.1",
                    "timestamp": "2020-04-29 10:00:04.011122",
                    "tvoc": "132",
                    "uva_index": "0.12",
                    "uvb_index": "0.16"
                },
                "enviro": {
                    "cpu_temp": "44.5'C",
                    "light": "1815.3",
                    "measurement_time": "190",
                    "nh3": "96.48",
                    "oxidised": "65.74",
                    "pm1": "1.0",
                    "pm10": "1.0",
                    "pm25": "1.0",
                    "reduced": "191.39",
                    "temperature": "13.0",
                    "timestamp": "2020-04-29 10:00:09.324039"
                }
            },
            "report": {
                "denva": {
                    "avg": {
                        "cpu_temperature": "47.63",
                        "execution_time": "744447870 ns.",
                        "gas_resistance": "12946860.59",
                        "humidity": "40.58",
                        "measurement_time": "901.66",
                        "motion": "4.95",
                        "pressure": "999.77",
                        "temperature": "23.25",
                        "uva": "0.02",
                        "uvb": "0.04"
                    },
                    "measurement_counter": 15917,
                    "records": {
                        "biggest_motion": "22",
                        "cpu_temperature": {
                            "max": "52.0",
                            "min": "43.0"
                        },
                        "execution_time": "1602894888 ns.",
                        "highest_eco2": "2867",
                        "highest_tvoc": "732",
                        "humidity": {
                            "max": "44.704",
                            "min": "33.519"
                        },
                        "log entries counter": 15917,
                        "max_uv_index": {
                            "uva": 0.08,
                            "uvb": 0.13
                        },
                        "pressure": {
                            "max": "1002.05",
                            "min": "998.91"
                        },
                        "temperature": {
                            "max": "27.24",
                            "min": "19.87"
                        }
                    },
                    "report_date": "28.4'2020",
                    "tube": {
                        "delays": {
                            "BakerlooFS": 0,
                            "BakerlooMD": 0,
                            "BakerlooPS": 0,
                            "BakerlooSD": 0,
                            "BakerlooTotalTime": "0 seconds.",
                            "CentralFS": 0,
                            "CentralMD": 0,
                            "CentralPS": 0,
                            "CentralSD": 0,
                            "CentralTotalTime": "0 seconds.",
                            "CircleFS": 0,
                            "CircleMD": 0,
                            "CirclePS": 0,
                            "CircleSD": 0,
                            "CircleTotalTime": "0 seconds.",
                            "DistrictFS": 0,
                            "DistrictMD": 0,
                            "DistrictPS": 0,
                            "DistrictSD": 0,
                            "DistrictTotalTime": "0 seconds.",
                            "HammersmithFS": 0,
                            "HammersmithMD": 0,
                            "HammersmithPS": 0,
                            "HammersmithSD": 0,
                            "HammersmithTotalTime": "0 seconds.",
                            "JubileeFS": 0,
                            "JubileeMD": 0,
                            "JubileePS": 0,
                            "JubileeSD": 0,
                            "JubileeTotalTime": "0 seconds.",
                            "MetropolitanFS": 0,
                            "MetropolitanMD": 0,
                            "MetropolitanPS": 0,
                            "MetropolitanSD": 0,
                            "MetropolitanTotalTime": "0 seconds.",
                            "NorthernFS": 0,
                            "NorthernMD": 0,
                            "NorthernPS": 0,
                            "NorthernSD": 0,
                            "NorthernTotalTime": "0 seconds.",
                            "PiccadillyFS": 0,
                            "PiccadillyMD": 0,
                            "PiccadillyPS": 0,
                            "PiccadillySD": 0,
                            "PiccadillyTotalTime": "0 seconds.",
                            "VictoriaFS": 0,
                            "VictoriaMD": 0,
                            "VictoriaPS": 0,
                            "VictoriaSD": 0,
                            "VictoriaTotalTime": "0 seconds.",
                            "WaterlooFS": 0,
                            "WaterlooMD": 0,
                            "WaterlooPS": 0,
                            "WaterlooSD": 0,
                            "WaterlooTotalTime": "0 seconds."
                        }
                    },
                    "warning_counter": 5,
                    "warnings": {
                        "cow": 0,
                        "cthe": 0,
                        "cthf": 0,
                        "cthw": 0,
                        "dfsl": 0,
                        "dsl": 0,
                        "fsl": 0,
                        "hhe": 0,
                        "hhw": 0,
                        "hle": 0,
                        "hlw": 0,
                        "iqe": 0,
                        "iqw": 0,
                        "the": 0,
                        "thw": 0,
                        "tle": 0,
                        "tlw": 0,
                        "uvaw": 0,
                        "uvbw": 0
                    }
                },
                "enviro": {
                    "avg": {
                        "execution_time": "0.19955573200013532 ns.",
                        "light": "160.15",
                        "measurement_time": "191.90",
                        "nh3": "98.25",
                        "oxidised": "65.48",
                        "pm1": "4.16",
                        "pm10": "5.91",
                        "pm25": "5.67",
                        "reduced": "188.79",
                        "temperature": "13.60"
                    },
                    "measurement_counter": 17174,
                    "records": {
                        "execution_time": "426073247 ns.",
                        "highest_light": "900.8",
                        "highest_oxidised": "76.76",
                        "highest_pm1": "12.0",
                        "highest_pm10": "16.0",
                        "highest_pm25": "16.0",
                        "highest_reduced": "203.92",
                        "log entries counter": 17174,
                        "measurement_time": {
                            "max": "10887",
                            "min": "162"
                        },
                        "temperature": {
                            "max": "20.4",
                            "min": "9.9"
                        }
                    },
                    "report_date": "28.4'2020",
                    "warning_counter": 2149
                },
                "rickmansworth": {
                    "crimes": "Crime data N/A",
                    "floods": "Flooding. 0 severe flooding warnings that are danger to life, 0 flooding warnings that require immediate action, 0 flooding alerts that flooding is possible.",
                    "o2": "None of the cell sites close to your location currently has any reported outages.",
                    "weather": [
                        "Max temp.: 13 \u00b0C",
                        "Min temp.: 6 \u00b0C",
                        "Sunny intervals changing to heavy rain by lunchtime",
                        "Sunrise: 05:36",
                        "Sunset: 20:23",
                        "UV: Moderate",
                        "Pollution: Low",
                        "Pollen: Low",
                        "2020-4-29-9-59-59"
                    ]
                }
            }
        }

        # when
        data_files.save_report_at_server(data)

        # then
        # check file exists
