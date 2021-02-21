from .. import storage


def test_load_csv_returns_station_maps():
    interchange_station_name_to_station_map, station_index_to_station_map = storage.load_csv("TestStations.csv")
    assert len(station_index_to_station_map) == 3
    assert len(interchange_station_name_to_station_map) == 2
    assert set(station_index_to_station_map.keys()) == {0, 1, 2}
    assert set(interchange_station_name_to_station_map.keys()) == {"Station 1", "Station 2"}
    assert interchange_station_name_to_station_map["Station 1"].stations[0] is station_index_to_station_map[0]
    assert interchange_station_name_to_station_map["Station 1"].stations[1] is station_index_to_station_map[1]


def test_load_csv_with_invalid_file_path_returns_empty_maps():
    interchange_station_name_to_station_map, station_index_to_station_map = storage.load_csv("Invalid.csv")
    assert len(interchange_station_name_to_station_map) == 0
    assert len(station_index_to_station_map) == 0
