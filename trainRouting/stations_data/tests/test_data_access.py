import pytest

from .. import data_access
from .. import stations
from datetime import date, datetime, timedelta


def mock_is_open(self, current_time):
    if self.station_id == 2:
        return False
    return True


def mock_get_travel_time(self, dest, current_time):
    if dest.station_id != 3:
        raise AssertionError
    if not current_time:
        raise AssertionError
    return timedelta(minutes=3)


@pytest.fixture(autouse=True)
def mock_storage(mocker):
    mocker.patch.object(stations.Station, "is_open", mock_is_open)
    mocker.patch.object(stations.Station, "get_travel_time", mock_get_travel_time)

    mock_station_1 = stations.Station(name="Station 1", code="ST1", station_id=1,
                                      opening_date=date(day=10, month=5, year=1990))
    mock_station_2 = stations.Station(name="Station 1", code="CT1", station_id=2,
                                      opening_date=date(day=10, month=5, year=1995))
    mock_station_3 = stations.Station(name="Station 2", code="ST2", station_id=3,
                                      opening_date=date(day=10, month=5, year=1990))

    mock_interchange_station = stations.InterchangeStation(name="Station 1")

    mock_interchange_station.stations = [mock_station_1, mock_station_2]

    mock_station_index_to_station_map = {1: mock_station_1, 2: mock_station_2, 3: mock_station_3}

    mock_station_name_to_station_map = {"Station 1": mock_interchange_station,
                                        "Station 2": stations.InterchangeStation(name="Station 2")}

    mocker.patch.object(data_access.storage, "station_index_to_station_map",
                        mock_station_index_to_station_map)
    mocker.patch.object(data_access.storage, "interchange_station_name_to_station_map",
                        mock_station_name_to_station_map)


def test_is_valid_station_name():
    assert not data_access.is_valid_station_name("Invalid")
    assert data_access.is_valid_station_name("Station 1")


def test_get_all_station_ids_by_name__with_time_None_returns_all_station_ids():
    assert data_access.get_station_ids_by_name("Station 1", None) == [1, 2]


def test_get_station_ids_by_name_with_invalid_name_returns_empty_list():
    assert data_access.get_station_ids_by_name("Invalid", current_time=None) == []


def test_get_station_ids_by_name_returns_only_open_stations():
    assert data_access.get_station_ids_by_name("Station 1", current_time=datetime.now()) == [1]


def test_get_station_line_by_index_with_time_None_returns_line():
    assert data_access.get_train_line_by_index(1, None) == "ST"


def test_get_station_line_with_invalid_index_returns_None():
    assert data_access.get_train_line_by_index(-1, None) is None


def test_get_station_line_by_index_returns_None_if_station_is_closed():
    assert data_access.get_train_line_by_index(2, current_time=datetime(day=9, month=5, year=1995)) is None


def test_get_station_code_by_index():
    assert data_access.get_station_code_by_index(1, current_time=datetime(day=10, month=5, year=1995)) is "ST1"


def test_get_station_code_by_index_with_invalid_index_returns_None():
    assert data_access.get_station_code_by_index(-1, current_time=datetime(day=10, month=5, year=1995)) is None


def test_get_station_code_by_index_returns_None_if_station_is_closed():
    assert data_access.get_station_code_by_index(2, current_time=datetime(day=10, month=5, year=1993)) is None


def test_get_station_name_by_index():
    assert data_access.get_station_name_by_index(1, current_time=datetime(day=10, month=5, year=1993)) == "Station 1"


def test_get_station_name_by_index_with_invalid_index_returns_None():
    assert data_access.get_station_name_by_index(-1, current_time=datetime(day=10, month=5, year=1995)) is None


def test_get_station_name_by_index_returns_None_if_station_is_closed():
    assert data_access.get_station_name_by_index(2, current_time=datetime(day=10, month=5, year=1993)) is None


def test_get_travel_time_raises_exception_with_invalid_source_or_dest_id():
    with pytest.raises(Exception):
        data_access.get_travel_time(-1, 1, current_time=datetime.now())
    with pytest.raises(Exception):
        data_access.get_travel_time(1, -1, current_time=datetime.now())


def test_get_travel_time_raises_exception_if_source_or_dest_is_closed():
    with pytest.raises(Exception):
        data_access.get_travel_time(1, 2, current_time=datetime.now())
    with pytest.raises(Exception):
        data_access.get_travel_time(2, 1, current_time=datetime.now())


def test_get_travel_time_returns_zero_minutes_if_station_ids_are_same():
    assert data_access.get_travel_time(1, 1, current_time=datetime.now()).total_seconds() == 0


def test_get_travel_time_returns_travel_time_between_source_and_dest_id():
    assert data_access.get_travel_time(1, 3, current_time=datetime.now()).total_seconds() == 3 * 60
