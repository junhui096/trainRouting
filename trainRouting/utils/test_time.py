from .time import is_night_hours, is_peak_hours
from datetime import datetime


def test_is_peak_hours_returns_False_on_weekends():
    assert not is_peak_hours(datetime(day=27, year=2021, month=2, hour=7))


def test_is_peak_hours_returns_True_on_weekdays_at_6am_or_6pm_but_not_9am_or_9pm():
    assert not is_peak_hours(datetime(day=26, year=2021, month=2, hour=9))
    assert not is_peak_hours(datetime(day=26, year=2021, month=2, hour=21))
    assert is_peak_hours(datetime(day=26, year=2021, month=2, hour=6))
    assert is_peak_hours(datetime(day=26, year=2021, month=2, hour=18))


def test_is_night_hours_returns_True_at_times_from_10pm_to_6am():
    assert is_night_hours(datetime(day=27, year=2021, month=2, hour=22))
    assert is_night_hours(datetime(day=27, year=2021, month=2, hour=5))


def test_is_night_hours_returns_False_outside_10pm_to_6am():
    assert not is_night_hours(datetime(day=26, year=2021, month=2, hour=9))
    assert not is_night_hours(datetime(day=26, year=2021, month=2, hour=21))
