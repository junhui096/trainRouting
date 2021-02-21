"""
This module is responsible for rendering the routes received to proper html.
"""

header_template = "<br/>Travel from {} to {}<br/>"
num_station_info_template = "Stations travelled: {}<br/>"
time_taken_info_template = "Time: {} minutes<br/>"
unreachable_template = "<br/>There are no routes from {} to {}<br/>"



def build_response(source, dest, routes, use_time_costs):
    """
    Returns a HTML response string that can be rendered in the browser.

            Parameters:
            source (string): name of source station
            dest (string): name of dest station routes(Route[]): list of routes from trainRouting package to be rendered
            use_time_costs(bool): Decides which template to render depending on whether to describe
             routes by time costs or number of stations.

            Returns:
                    string: html string to be rendered.
    """
    if not routes:
        return unreachable_template.format(source, dest)
    if use_time_costs:
        info_template = time_taken_info_template
    else:
        info_template = num_station_info_template
    return "<br/>".join([header_template.format(source, dest) + info_template.format(str(route["Info"]))
                         + "<br/>".join(route["Route"].split("\n")) + "<br/>" for route in routes])
