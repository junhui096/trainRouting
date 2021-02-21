from .is_open import is_open
from .interstation_costs import get_interstation_travel_costs
from .intrastation_costs import get_intrastation_travel_costs

"""
Factory class responsible for creating travel time cost calculator by station_line.
"""


class CostCalculatorFactory:
    """
    Retrieves the cost handler functions based on train line, and initialises cost calculator accordingly.
    """

    @staticmethod
    def create(station_line):
        return CostCalculatorFactory.CostCalculator(is_open=is_open(station_line),
                                                    interstation_costs=get_interstation_travel_costs(station_line),
                                                    intrastation_costs=get_intrastation_travel_costs(station_line))

    """
    Encapsulates the logic of calculating the travel costs for a given train line, the transfer costs between train lines, 
    and the logic to determine if a train line is operational. Station objects delegate such logic to the cost calculator.
    A cost calculator is composed of three functions that help to calculate the cost in each instance respectively.
    """
    class CostCalculator:

        def __init__(self, is_open, interstation_costs, intrastation_costs):
            self.is_open = is_open
            self.interstation_costs = interstation_costs
            self.intrastation_costs = intrastation_costs

        def is_open(self, current_time):
            """
            Delegates the logic to the is_open handler to check if station should be open. True if station is to be open
            at current_time and False otherwise.
            """
            return self.is_open(current_time)

        def get_transfer_costs(self, current_time):
            """
            Delegates the logic to the intrastation_costs handler to calculate cost of line transfers. Returns timedelta
            object for transfer cost.
            """
            return self.intrastation_costs(current_time)

        def get_travel_cost_per_station(self, current_time):
            """
            Delegates logic to interstation_cost_handler to calculate time needed for one stop on the train line
            at time current_time.
            """
            return self.interstation_costs(current_time)
