from .templates import build_response

mock_routes = [{"Info": 5, "Route": "test route1"}, {"Info": 10, "Route": "test route2"}]


def test_build_response_with_no_routes():
    expected = "<br/>There are no routes from A to B<br/>"
    assert build_response("A", "B", [], False) == expected


def test_build_response_with_use_time_costs_as_False():
    expected = "<br/>Travel from A to B<br/>Stations travelled: 5<br/>test route1<br/><br/><br/>Travel from A to B<br/>Stations travelled: 10<br/>test route2<br/>"
    assert build_response("A", "B", mock_routes, False) == expected


def test_build_response_with_use_time_costs_as_True():
    expected = "<br/>Travel from A to B<br/>Time: 5 minutes<br/>test route1<br/><br/><br/>Travel from A to B<br/>Time: 10 minutes<br/>test route2<br/>"
    assert build_response("A", "B", mock_routes, True) == expected
