from ..stations import InterchangeStation, Station
from datetime import datetime, date, timedelta

test_interchange = InterchangeStation(name="Test Interchange")
test_station_1 = Station(name="Test Interchange", station_id=1, code="EW1",
                         opening_date=date(day=1, month=1, year=2000))
test_station_2 = Station(name="Test Interchange", station_id=2, code="NS1",
                         opening_date=date(day=1, month=1, year=2050))
test_interchange.stations = [test_station_1, test_station_2]


def test_is_open_returns_True_is_open_and_False_otherwise():
    assert test_station_1.is_open(current_time=datetime(day=1, month=1, year=2000))
    assert not test_station_1.is_open(current_time=datetime(day=1, month=1, year=1999))


def test_get_code_returns_station_code():
    assert test_station_1.get_code() == "EW1"


def test_get_name_returns_station_name():
    assert test_station_1.get_name() == "Test Interchange"


def test_get_train_line_returns_train_line_of_station():
    assert test_station_1.get_train_line() == "EW"


def test_get_travel_time_returns_time_between_two_stations():
    assert test_station_1.get_travel_time(test_station_2,
                                          current_time=datetime(hour=10, minute=20, day=1, month=5,
                                                                year=2020)) == timedelta(minutes=10)


def test_add_station_increases_num_of_stations_in_interchange():
    sample_interchange = InterchangeStation(name="Sample Interchange")
    assert len(sample_interchange.stations) == 0
    sample_interchange.add_station(station_id=3, code="CC10", opening_date=date.today())
    assert len(sample_interchange.stations) == 1


def test_get_stations_with_current_time_as_None_returns_all_stations():
    assert test_interchange.get_stations(None) == [1, 2]


def test_get_stations_with_current_time_returns_open_stations():
    assert test_interchange.get_stations(current_time=datetime(day=10, month=10, year=2010)) == [1]
