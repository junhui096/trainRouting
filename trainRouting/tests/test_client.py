from .. import client, route
import pytest
from datetime import datetime, timedelta
from .mocks import mock_get_station_ids_by_name, mock_is_valid_station_name


@pytest.fixture(autouse=True)
def mock_functions(mocker):
    mocker.patch.object(client, "get_station_ids_by_name", side_effect=mock_get_station_ids_by_name)
    mocker.patch.object(client, "is_valid_station_name", side_effect=mock_is_valid_station_name)


@pytest.fixture(autouse=True)
def mock_network(mocker):
    start_time = datetime.now()
    route_1 = route.Route(route=[1, 3, 4], start_time=start_time, end_time=start_time + timedelta(minutes=45))
    route_2 = route.Route(route=[0, 4], start_time=start_time, end_time=start_time + timedelta(minutes=20))

    class MockNetwork:
        @staticmethod
        def get_routes(source, dest, current_time, use_time_costs):
            return [route_1, route_2]

    mock = mocker.patch.object(client, "MRTNetwork", MockNetwork)
    return mock


def test_empty_routes_if_source_and_dest_are_the_same():
    assert client.get_all_routes("Station 1", "Station 1", datetime.now(), False) == []


def test_get_all_routes_with_invalid_source_raises_exception():
    with pytest.raises(Exception):
        client.get_all_routes("Invalid", "Station 1", datetime.now(), False)


def test_get_all_routes_with_invalid_dest_raises_exception():
    with pytest.raises(Exception):
        client.get_all_routes("Station 1", "Invalid", datetime.now(), False)


def test_get_all_routes_with_use_current_costs_as_True_returns_routes_sorted_by_travel_time(mock_network):
    result = client.get_all_routes("Station 1", "Station 4", datetime.now(), True)
    assert [rt["Info"] for rt in result] == ["20", "45"]


def test_get_all_routes_with_use_current_costs_as_False_returns_routes_sorted_by_num_stations(mock_network):
    result = client.get_all_routes("Station 1", "Station 4", datetime.now(), False)
    assert [rt["Info"] for rt in result] == ["2", "3"]
