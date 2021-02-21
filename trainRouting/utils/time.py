import datetime


def is_peak_hours(time):
    """
    Returns True if time falls between 6am(inclusive) to 9am(exclusive) or 6pm(incl) to 9pm(excl) on any weekday.
            Parameters:
                    time(datetime): time to test
            Returns:
                    bool:
    """
    if not 1 <= time.isoweekday() <= 5:
        return False
    if time.hour in [6, 7, 8, 18, 19, 20]:
        return True

    return False


def is_night_hours(time):
    """
    Returns True if time falls between 10pm(inclusive) to 6am(exclusive) on any day.
            Parameters:
                    time(datetime): time to test
            Returns:
                    bool:
    """
    if time == datetime.time(22, 0, 0, 0):
        return True
    return time.hour in [22, 23, 0, 1, 2, 3, 4, 5]