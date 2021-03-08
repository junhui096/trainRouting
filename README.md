# Train Routing Zendesk Coding Challenge 

## Assumptions:

* If no start time is given, assume that the trip starts from the current wall clock time.
* The trainRouting package assumes that two routes are different if the sequence of station codes traversed are different, 
even if consecutive station codes refer to the same physical station, and only involve a change in train lines.
Hence, the trainRouting package may produce multiple routes that differ only in their starting or ending station code when the source or destination station is an interchange station 
with multiple station codes.
* If travel times are considered in routing, the routing package assumes that there are no additional wait times at stations, apart from travel & transfer times.
* Assume that the travel time from any source station A to neighbouring station B, is entirely determined by time at which the passenger visits station A.
For example, the travel time between DT12 and DT13 on a weekday at 5.53am is assumed to be 8 minutes, rather than 10 minutes, 
in line with travel times in the non-peak band, even though the traveller will only arrive at DT13 in the peak hour time band.
* In calculating travel times between stations, the routing package assumes that peak hours begin from 6am on weekdays, inclusive, and end at 9am on weekdays exclusive.
* In calculating travel times between stations, the routing package assumes night hours begin from 10pm, inclusive, and end at 6am exclusive.
* The routing package assumes that the DT, CG and CE are open both at exactly 10pm and exactly 6am, the beginning and end of night hours respectively.


## How to run with Docker:

```
cd trainRouting
docker build . --tag train_routing:1.0  
docker run -d -p 5000:5000 --name train train_routing:1.0
```
## Run tests with docker:

```
docker exec -it train /bin/bash
cd trainRouting/
pytest
```

## Requirements:
* Python 2.7 (installed by default in Ubuntu 16.04) Otherwise:
```
sudo apt update && sudo apt install python-minimal
```

## How to run:

```
cd trainRouting
sudo apt update && sudo apt install python-pip
sudo pip install -r requirements.txt
```
Run the flask web server as follows:
```
export FLASK_APP=main.py
flask run
``` 
To get a list of routes between a named source station to a named destination station, issue a GET http request to the following url:

> http://localhost:5000/api/v1/get_routes

The html response can be rendered in a browser. 

The url requires these two query parameters: 

* start: the name of the source station 
* end: the name of the destination station

For example:

> http://localhost:5000/api/v1/get_routes?start=Lavender&end=Buona%20Vista

It can further include this optional parameter:
* current_time: The start time of the route expressed as: "YYYY-MM-DDThh:mm" format

For example:

> http://localhost:5000/api/v1/get_routes?start=Lavender&end=Newton&start_time=2020-01-05T12:30

If current time is not specified travel costs between stations and transfer costs within stations are ignored. Furthermore,
all stations are assumed to be open including stations that have an opening date in the future.\
By default, the routes are returned in ascending order of the number of stations traversed in the route.\
If the optional current_time parameter is included by the user, routes are ordered in ascending order of their end_time.

## Tests
```
pytest
```
The pytest runner collects all test files and runs them in turn.

   