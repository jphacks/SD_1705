import requests
from pprint import pprint

class GoogleMap_parsing():
    def __init__(self, origin: str, destination: str, waypoints: list):
        self.route_list = []
        self.origin = origin
        self.destination = destination
        self.waypoints = waypoints
        self.result_of_gm_api = requests.get(
            "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints={}&language=ja&key=AIzaSyCJb3c7Bd6oGo0mT9dmuBi_tCDzllc47rk".format(self.origin, self.destination, "|".join(self.waypoints))).json()

        self.input_locations = self.__get_input_locations()


    def __get_input_locations(self) -> list:
        """
        origin, destination, waypointsを一つの配列にまとめる
        :return: list(input_location: str)
        """
        input_locations = self.waypoints
        input_locations.insert(0,self.origin)
        input_locations.append(self.destination)
        return input_locations

    def get_route(self) -> list:
        """
        apiからの座標を出力
        :return: list({lat:value, lng:value})
        """
        route_steps = []
        for route in self.result_of_gm_api["routes"][0]["legs"]:
            for step in route['steps']:
                route_steps.append(step["start_location"])
                route_steps .append(step["end_location"])
        return [route for i, route in enumerate(route_steps) if i == 0 or (i-1 != -1 and route_steps[i-1] != route)]

    def get_input_location_status(self) -> tuple:
        """
        inputのlocationがどうかを調べる
        :return: (リクエストのステータス, frontに返すdict（{num: {is_exist: bool, location: str}, num:...}）)
        """
        result_dict = dict()
        assert len(self.result_of_gm_api['geocoded_waypoints']) == len(self.input_locations), "入ってきたlocationの数とapiを通して得られたpointの数が違う"
        for i, status_api in enumerate(self.result_of_gm_api["geocoded_waypoints"]):
            if i == 0:
                self.__get_result_dict(result_dict, status_api, self.input_locations[i], i)
            elif i == len(self.result_of_gm_api["geocoded_waypoints"]):
                self.__get_result_dict(result_dict, status_api, self.input_locations[i], i)
            else:
                self.__get_result_dict(result_dict, status_api, self.input_locations[i], i)

        return (self.result_of_gm_api["status"], result_dict)


    def __get_result_dict(self, result_dict: dict, status_api, location: str, i: int):
        """
        get_input_location_statusで繰り返す処理を関数化
        :param result_dict:
        :param status_api:
        :param location:
        :param i:
        :return:
        """
        if i == 0:
            key = "origin"
        elif i == len(self.result_of_gm_api)-1:
            key = "destination"
        else:
            key = "way{}".format(i-1)
            

        if status_api["geocoder_status"] == "OK":
            result_dict[key] = location
        else:
            result_dict[key] = None
