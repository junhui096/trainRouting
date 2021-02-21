from ..factory import CostCalculatorFactory
from datetime import datetime, timedelta

peak_hour_time = datetime(day=25, month=2, year=2021, hour=6, minute=0)
night_hour_time = datetime(day=25, month=2, year=2021, hour=22, minute=0)
non_peak_hour_time = datetime(day=20, month=2, year=2021, hour=6, minute=0)


def check_NS_and_NE_lines_take_twelve_minutes_per_station_at_peak_hours():
    assert CostCalculatorFactory.create("NS").get_travel_cost_per_station(peak_hour_time) == timedelta(minutes=12)
    assert CostCalculatorFactory.create("NE").get_travel_cost_per_station(peak_hour_time) == timedelta(minutes=12)


def check_all_other_lines_take_ten_minutes_per_station_at_peak_hours():
    assert CostCalculatorFactory.create("DT").get_travel_cost_per_station(peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("TE").get_travel_cost_per_station(peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("EW").get_travel_cost_per_station(peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("CE").get_travel_cost_per_station(peak_hour_time) == timedelta(minutes=10)


def check_train_line_change_takes_15_mins_per_stop_at_peak_hours():
    assert CostCalculatorFactory.create("NS").get_transfer_costs(peak_hour_time) == timedelta(minutes=15)
    assert CostCalculatorFactory.create("DT").get_transfer_costs(peak_hour_time) == timedelta(minutes=15)
    assert CostCalculatorFactory.create("TE").get_transfer_costs(peak_hour_time) == timedelta(minutes=15)


def check_DT_CG_CE_lines_not_operate_at_night_hours():
    for i in ["DT", "CG", "CE"]:
        assert not CostCalculatorFactory.create(i).is_open(night_hour_time)


def check_other_train_lines_open_at_all_times():
    assert CostCalculatorFactory.create("NS").is_open(night_hour_time)
    assert CostCalculatorFactory.create("DT").is_open(non_peak_hour_time)
    assert CostCalculatorFactory.create("CG").is_open(peak_hour_time)
    assert CostCalculatorFactory.create("EW").is_open(non_peak_hour_time)


def check_all_other_lines_take_ten_minutes_per_station_at_night_hours():
    assert CostCalculatorFactory.create("DT").get_travel_cost_per_station(night_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("TE").get_travel_cost_per_station(night_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("EW").get_travel_cost_per_station(night_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("CE").get_travel_cost_per_station(night_hour_time) == timedelta(minutes=10)


def check_train_line_change_takes_ten_mins_per_stop_at_night_hours():
    assert CostCalculatorFactory.create("NS").get_transfer_costs(night_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("DT").get_transfer_costs(night_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("TE").get_transfer_costs(night_hour_time) == timedelta(minutes=10)


def check_DT_and_TE_lines_take_eight_minutes_per_station_at_non_peak_hours():
    assert CostCalculatorFactory.create("DT").get_travel_cost_per_station(non_peak_hour_time) == timedelta(minutes=8)
    assert CostCalculatorFactory.create("TE").get_travel_cost_per_station(non_peak_hour_time) == timedelta(minutes=8)


def check_all_other_lines_take_ten_minutes_per_station_at_non_peak_hours():
    assert CostCalculatorFactory.create("DT").get_travel_cost_per_station(non_peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("TE").get_travel_cost_per_station(non_peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("EW").get_travel_cost_per_station(non_peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("CE").get_travel_cost_per_station(non_peak_hour_time) == timedelta(minutes=10)


def check_train_line_change_takes_ten_mins_per_stop_at_non_peak_hours():
    assert CostCalculatorFactory.create("NS").get_transfer_costs(non_peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("DT").get_transfer_costs(non_peak_hour_time) == timedelta(minutes=10)
    assert CostCalculatorFactory.create("TE").get_transfer_costs(non_peak_hour_time) == timedelta(minutes=10)
