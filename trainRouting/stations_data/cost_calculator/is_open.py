from ...utils.time import is_night_hours
from collections import defaultdict
import datetime

"""
This module maintains the various handler functions that encapsulate the logic of deciding whether a train line is operational.
"""


def default_is_open_function(current_time):
    return True


"""
Assume station is open at exactly 10pm.
"""


def closed_during_night_hours(current_time):
    if current_time == datetime.time(22, 0, 0, 0):
        return True
    if is_night_hours(current_time):
        return False
    return default_is_open_function(current_time)


train_line_to_is_open_mapping = defaultdict(lambda: default_is_open_function)

for line in ["DT", "CG" and "CE"]:
    train_line_to_is_open_mapping[line] = closed_during_night_hours


def is_open(line):
    """
       Returns a handler function that takes current time and checks if line is open at a given time.

               Parameters:
               line(str): train line

               Returns:
                      datetime.datetime -> bool: handler func that takes current time and returns True iff
                      line is operational.
       """
    return train_line_to_is_open_mapping[line]
