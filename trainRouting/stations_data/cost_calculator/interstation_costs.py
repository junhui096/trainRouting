from ...utils.time import is_peak_hours
from datetime import timedelta
from collections import defaultdict

"""
This module maintains the various handler functions that encapsulate the logic for calculating cost of travel between 
stations of same line.(ie. between two physical stations)
"""


def twelve_min_during_peak(current_time):
    if is_peak_hours(current_time):
        return timedelta(minutes=12)
    else:
        return default_cost_function(current_time)


def eight_minutes_during_non_peak(current_time):
    if not is_peak_hours(current_time):
        return timedelta(minutes=8)
    else:
        return default_cost_function(current_time)


def default_cost_function(current_time):
    return timedelta(minutes=10)


train_line_to_cost_function_mapping = defaultdict(lambda: default_cost_function)

train_line_to_cost_function_mapping["NS"] = twelve_min_during_peak
train_line_to_cost_function_mapping["NE"] = twelve_min_during_peak
train_line_to_cost_function_mapping["DT"] = eight_minutes_during_non_peak
train_line_to_cost_function_mapping["TE"] = eight_minutes_during_non_peak


def get_interstation_travel_costs(line):
    """
    Get handler function to initialize cost calculator by train line.

            Parameters:
            line(str): train line

            Returns:
                   datetime.datetime -> timedelta: handler func that takes current time and returns time for travel
                   on same line.
    """
    return train_line_to_cost_function_mapping[line]
