"""
Mock train network:

0 - - - 1 - 2 (EW)
|       |
5 - 4 - 3 (NS)   6(DT)
"""
from datetime import timedelta


def mock_get_station_ids_by_name(name, current_time):
    if name == "Station 0":
        return [0, 5]
    elif name == "Station 1":
        return [1, 3]
    elif name == "Station 2":
        return [2]
    elif name == "Station 4":
        return [4]
    elif name == "Unreachable":
        return [6]


def mock_get_train_line_by_index(index, current_time):
    if index in [0, 1, 2]:
        return "EW"
    elif index in [3, 4, 5]:
        return "NS"
    elif index in [6]:
        return "DT"


def mock_get_station_code_by_index(index, current_time):
    mapping = {0: "EW0", 1: "EW1", 2: "EW2", 3: "NS3", 4: "NS4", 5: "NS5", 6: "DT6"}
    return mapping[index]


def mock_get_station_name_by_index(index, current_time):
    if index in [0, 5]:
        return "Station 0"
    elif index in [1, 3]:
        return "Station 1"
    elif index == 2:
        return "Station 2"
    elif index == 4:
        return "Station 4"
    else:
        return "Unreachable"


def mock_get_travel_time(source_id, dest_id, current_time):
    if source_id == 0 and dest_id == 1:
        return timedelta(minutes=1000)
    if source_id == 1 and dest_id == 0:
        return timedelta(minutes=1000)
    return timedelta(minutes=10)


def mock_is_valid_station_name(name):
    if name in ["Station 0", "Station 1", "Station 2", "Station 4"]:
        return True
    else:
        return False
