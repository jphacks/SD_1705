import requests

class GoogleMao_parsing():
    def __init__(self, origin: str, destination: str, waypoints: list):
        self.route_list = []
        self.origin = origin
        self.destination = destination
        self.waypoints = waypoints
        self.result_of_gmapi = requests.get(
            "https://maps.googleapis.com/maps/api/directions/json?\
            origin={}&destination={}&waypoints={}&language=ja&key=AIzaSyCJb3c7Bd6oGo0mT9dmuBi_tCDzllc47rk".format(origin, destination, "|".join(waypoints)))


    def get_route(self) -> list:
        route_steps = []
        for route in self.result_of_gmapi.json()["routes"][0]["legs"]:
            for step in route['steps']:
                route_steps.append(step["start_location"])
                route_steps .append(step["end_location"])
        return [route for i, route in enumerate(route_steps) if i == 0 or (i-1 != -1 and route_steps[i-1] != route)]

