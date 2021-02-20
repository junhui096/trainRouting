from . import storage
import datetime


def test_get_station_by_index():
    sample_station = storage.get_station_by_index(6)
    assert sample_station.name == "Marsiling"
    assert sample_station.code == "NS8"
    assert sample_station.opening_date == datetime.date(year=1996, month=2, day=10)


def test_get_station_by_index_with_invalid_index_gives_none():
    sample_station = storage.get_station_by_index(500)
    assert sample_station is None


def test_get_station_by_name():
    sample_interchange_station = storage.get_station_by_name("Buona Vista")
    sample_stations = sample_interchange_station.get_stations()
    assert len(sample_stations) == 2
    assert storage.get_station_by_index(sample_stations[0]).name == "Buona Vista"
    assert storage.get_station_by_index(sample_stations[0]).code == "EW21"

    assert storage.get_station_by_index(sample_stations[1]).name == "Buona Vista"
    assert storage.get_station_by_index(sample_stations[1]).code == "CC22"


def test_get_station_by_name_with_invalid_name_gives_none():
    sample_station = storage.get_station_by_name("abc")
    assert sample_station is None



