from .. import app


def test_travel_between_stations_ignoring_time_costs():
    with app.test_client() as c:
        expected = "<br/>Travel from Dover to Bukit Batok<br/>" + \
                   "Stations travelled: 4<br/>Route: (EW22, EW23, EW24, NS1, NS2)<br/>" + \
                   "Take EW line from Dover to Clementi<br/>Take EW line from Clementi to Jurong East<br/>" + \
                   "Change from EW line to NS line<br/>Take NS line from Jurong East to Bukit Batok<br/>"

        response = c.get("/api/v1/get_routes?start=Dover&end=Bukit Batok")
        assert response.data.decode('utf-8') == expected
        assert response.status_code == 200


def test_travel_between_station_with_time_costs():
    expected = "<br/>Travel from Boon Lay to Little India<br/>Time: 150 minutes<br/>" + \
               "Route: (EW27, EW26, EW25, EW24, EW23, EW22, EW21, CC22, CC21, CC20, CC19, DT9, DT10, DT11, DT12)<br/>" + \
               "Take EW line from Boon Lay to Lakeside<br/>Take EW line from Lakeside to Chinese Garden<br/>" + \
               "Take EW line from Chinese Garden to Jurong East<br/>Take EW line from Jurong East to Clementi<br/>" + \
               "Take EW line from Clementi to Dover<br/>" + \
               "Take EW line from Dover to Buona Vista<br/>" + \
               "Change from EW line to CC line<br/>Take CC line from Buona Vista to Holland Village<br/>" + \
               "Take CC line from Holland Village to Farrer Road<br/>" + \
               "Take CC line from Farrer Road to Botanic Gardens<br/>" + "Change from CC line to DT line<br/>" + \
               "Take DT line from Botanic Gardens to Stevens<br/>" + \
               "Take DT line from Stevens to Newton<br/>" + \
               "Take DT line from Newton to Little India<br/><br/><br/>" + \
               "Travel from Boon Lay to Little India<br/>Time: 165 minutes<br/>" + \
               "Route: (EW27, EW26, EW25, EW24, EW23, EW22, EW21, CC22, CC21, CC20, CC19, DT9, DT10, DT11, DT12, NE7)<br/>" + \
               "Take EW line from Boon Lay to Lakeside<br/>Take EW line from Lakeside to Chinese Garden<br/>" + \
               "Take EW line from Chinese Garden to Jurong East<br/>Take EW line from Jurong East to Clementi<br/>" + \
               "Take EW line from Clementi to Dover<br/>Take EW line from Dover to Buona Vista<br/>" + \
               "Change from EW line to CC line<br/>Take CC line from Buona Vista to Holland Village<br/>" + \
               "Take CC line from Holland Village to Farrer Road<br/>" + \
               "Take CC line from Farrer Road to Botanic Gardens<br/>" + \
               "Change from CC line to DT line<br/>Take DT line from Botanic Gardens to Stevens<br/>" + \
               "Take DT line from Stevens to Newton<br/>Take DT line from Newton to Little India<br/>" + \
               "Change from DT line to NE line<br/>"

    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=Boon Lay&end=Little India&start_time=2021-01-05T06:00")
        assert response.data.decode('utf-8') == expected


def test_travel_between_stations_with_start_station_closed():
    expected = "<br/>There are no routes from Hillview to Jurong East<br/>"
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=Hillview&end=Jurong East&start_time=2020-01-05T22:30")
        assert response.data.decode('utf-8') == expected


def test_travel_between_stations_with_end_station_closed_at_end():
    expected = "<br/>There are no routes from Jurong East to Hillview<br/>"
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=Jurong East&end=Hillview&start_time=2020-01-05T20:30")
        assert response.data.decode('utf-8') == expected


def test_travel_between_stations_with_intermediate_stations_closed():
    expected = "<br/>There are no routes from Geylang Bahru to Hillview<br/>"
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=Geylang Bahru&end=Hillview&start_time=2020-01-05T20:45")
        assert response.data.decode('utf-8') == expected
