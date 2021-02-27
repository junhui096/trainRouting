from .. import mrt_network
from datetime import datetime, timedelta
from .. import route
import pytest
from .mocks import mock_get_station_ids_by_name, mock_get_train_line_by_index, mock_get_station_name_by_index, \
    mock_get_travel_time


@pytest.fixture(autouse=True)
def mock_data_access_calls(mocker):
    mocker.patch.object(mrt_network, "get_station_ids_by_name", side_effect=mock_get_station_ids_by_name)
    mocker.patch.object(mrt_network, "get_train_line_by_index", side_effect=mock_get_train_line_by_index)
    mocker.patch.object(mrt_network, "get_station_name_by_index", side_effect=mock_get_station_name_by_index)
    mocker.patch.object(mrt_network, "get_travel_time", side_effect=mock_get_travel_time)


def test_get_neighbours_returns_all_adj_stations_on_same_line_or_within_same_interchange_with_use_time_costs_False():
    mock_node = mrt_network.MRTNetwork.Node(station_id=0, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == {1, 5}
    mock_node = mrt_network.MRTNetwork.Node(station_id=1, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == {0, 2, 3}
    mock_node = mrt_network.MRTNetwork.Node(station_id=2, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == {1}
    mock_node = mrt_network.MRTNetwork.Node(station_id=3, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == {1, 4}
    mock_node = mrt_network.MRTNetwork.Node(station_id=4, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == {3, 5}
    mock_node = mrt_network.MRTNetwork.Node(station_id=5, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == {0, 4}
    mock_node = mrt_network.MRTNetwork.Node(station_id=6, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(False)} == set()


def test_get_neighbours_with_use_time_costs_True_does_not_return_closed_stations():
    mock_node = mrt_network.MRTNetwork.Node(station_id=1, current_time=datetime.now())
    assert {neigh.get_id() for neigh in mock_node.get_neighbours(True)} == {0, 3}


def test_neighbouring_nodes_have_time_values_higher_than_source_node_when_use_time_costs_is_True():
    current_time = datetime(day=1, year=2000, month=1, hour=1, minute=10)
    expected_time = current_time + timedelta(minutes=10)
    mock_node = mrt_network.MRTNetwork.Node(station_id=5, current_time=current_time)
    assert all(n.get_current_time() == expected_time for n in mock_node.get_neighbours(use_time_costs=True))


def test_get_routes_with_source_and_dest_id_same_returns_no_routes():
    assert mrt_network.MRTNetwork.get_routes(1, 1, datetime.now(), False) == []


def test_get_routes_from_source_to_dest_without_time_costs_returns_shortest_route_by_num_steps():
    assert mrt_network.MRTNetwork.get_routes(0, 3, datetime.now(), False) == \
           [route.Route(route=[0, 1, 3], start_time=datetime.now(), end_time=datetime.now())]


def test_get_routes_from_source_to_dest_with_time_costs_returns_shortest_route_by_travel_time():
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=30)
    assert mrt_network.MRTNetwork.get_routes(0, 3, start_time, True) == \
           [route.Route([0, 5, 4, 3], start_time, end_time)]


def test_get_routes_with_time_costs_True_returns_correct_end_time_of_route():
    start_time = datetime.now()
    expected_end_time = start_time + timedelta(minutes=30)
    assert mrt_network.MRTNetwork.get_routes(0, 3, start_time, True)[0].end_time == expected_end_time


def test_get_routes_with_unreachable_dest_from_source():
    assert mrt_network.MRTNetwork.get_routes(0, 6, datetime(day=1, month=1, year=2000), False) == []
