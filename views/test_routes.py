import pytest
from .. import app
from . import routes
import datetime


def mock_get_all_routes(source, dest, current_time, use_time_costs):
    if source == "Invalid":
        raise Exception()
    return [{"Info": 5, "Route": "test route"}]


@pytest.fixture
def mock_train_routing_client(mocker):
    mock = mocker.patch.object(routes, "get_all_routes", side_effect=mock_get_all_routes)
    return mock


def test_missing_start_param_gives_400():
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes")
        assert response.data.decode('utf-8') == "Missing start query parameter"
        assert response.status_code == 400


def test_missing_end_param_gives_400():
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=A")
        assert response.data.decode('utf-8') == "Missing end query parameter"
        assert response.status_code == 400


def test_invalid_start_time_gives_400():
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=A&end=B&start_time=1111")
        expected = "Invalid start time time data '1111' does not match format '%Y-%m-%dT%H:%M'"
        assert response.data.decode('utf-8') == expected
        assert response.status_code == 400


def test_successful_rendering_without_current_time(mock_train_routing_client):
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=A&end=B")
        assert response.data.decode('utf-8') == "<br/>Travel from A to B<br/>Stations travelled: 5<br/>test route<br/>"
        mock_train_routing_client.assert_called_with("A", "B", datetime.datetime.min, False)
        assert response.status_code == 200


def test_successful_rendering_with_current_time(mock_train_routing_client):
    expected_date = datetime.datetime(year=2020, month=1, day=5, hour=12, minute=30)
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=A&end=B&start_time=2020-01-05T12:30")
        assert response.data.decode('utf-8') == "<br/>Travel from A to B<br/>Time: 5 minutes<br/>test route<br/>"
        mock_train_routing_client.assert_called_with("A", "B", expected_date, True)


def test_routes_with_invalid_start_name_gives_404():
    expected = "Error finding routes. Ensure the name of start and end stations are valid."
    with app.test_client() as c:
        response = c.get("/api/v1/get_routes?start=Invalid&end=B")
        assert response.data.decode('utf-8') == expected
        assert response.status_code == 404
