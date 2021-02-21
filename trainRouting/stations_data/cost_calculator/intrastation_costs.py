from ...utils.time import is_peak_hours
from datetime import timedelta
from collections import defaultdict

"""
This module maintains the various handler functions that encapsulate the logic for calculating cost of line transfer.
(ie. within the same station)
"""

def default_cost_function(current_time):
    if is_peak_hours(current_time):
        return timedelta(minutes=15)
    else:
        return timedelta(minutes=10)


train_line_to_cost_function_mapping = defaultdict(lambda: default_cost_function)


def get_intrastation_travel_costs(line):
    """
       Get handler function to initialize cost calculator by train line.

               Parameters:
               line(str): train line

               Returns:
                      datetime.datetime -> timedelta: handler func that takes current time and returns time for transfer
                      within the same physical interchange.
       """
    return train_line_to_cost_function_mapping[line]
