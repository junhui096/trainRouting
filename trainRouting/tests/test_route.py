from ..route import Route
from datetime import datetime, timedelta
from .. import route
import pytest
from .mocks import mock_get_station_name_by_index, mock_get_station_code_by_index, mock_get_train_line_by_index

start_time = datetime.now()
end_time = datetime.now() + timedelta(minutes=30)
test_route_1 = Route(route=[0, 5, 4, 3], start_time=start_time, end_time=end_time)
test_route_2 = Route(route=[0, 5, 4, 3], start_time=datetime(day=2, month=3, year=1990),
                     end_time=datetime(day=2, month=3, year=1990))


@pytest.fixture(autouse=True)
def mock_data_access_calls(mocker):
    mocker.patch.object(route, "get_station_code_by_index", side_effect=mock_get_station_code_by_index)
    mocker.patch.object(route, "get_train_line_by_index", side_effect=mock_get_train_line_by_index)
    mocker.patch.object(route, "get_station_name_by_index", side_effect=mock_get_station_name_by_index)


def test_route_to_string_gives_directions():
    expected = "Route: (EW0, NS5, NS4, NS3)\nChange from EW line to NS line\nTake NS line from Station 0 to Station " \
               "4\nTake NS line from Station 4 to Station 1"
    assert str(test_route_1) == expected


def test_route_equality_between_routes_with_same_id_seq():
    assert test_route_1 == test_route_2


def test_route_hashing_equality():
    s = set()
    s.add(test_route_1)
    s.add(test_route_2)
    assert len(s) == 1


def test_num_stations_returns_num_physical_stations():
    assert test_route_1.num_stations() == 3


def test_num_steps_returns_length_of_route():
    assert test_route_1.num_steps() == 4


def test_get_travel_time_returns_num_minutes_of_travel():
    assert test_route_1.get_travel_time() == 30
