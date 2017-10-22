import requests
from pprint import pprint
from copy import deepcopy

DIFFERENCE = 0.005

class GoogleMap_parsing():
    def __init__(self, origin: str, destination: str, waypoints: list, mode="driving"):
        self.route_list = []
        self.origin = origin
        self.destination = destination
        self.waypoints = waypoints
        self.mode = mode
        self.result_of_gm_api = requests.get(
            "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints={}&mode={}&language=ja&key=AIzaSyCJb3c7Bd6oGo0mT9dmuBi_tCDzllc47rk".format(self.origin, self.destination, "|".join(self.waypoints), self.mode)).json()

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
        route_path = [route for i, route in enumerate(route_steps) if i == 0 or (i-1 != -1 and route_steps[i-1] != route)]
        return self.__completion_route(route_path)

    def __completion_route(self, route: list) -> list:
        """
        DIFFERENCEより，差が大きい位置を補完
        :param route: google apiから取れる座標のリスト
        :return: 補完をしたリスト
        """
        copy_list = deepcopy(route)
        for i in range(0,len(route)-1):
            if abs(route[i]["lat"] - route[i+1]["lat"]) > DIFFERENCE or abs(route[i]["lng"] - route[i+1]["lng"]) > DIFFERENCE:
                lat_difference = (route[i + 1]["lat"] - route[i]["lat"]) / 10
                lng_difference = (route[i + 1]["lng"] - route[i]["lng"]) / 10
                index = copy_list.index(route[i])
                insert_val = route[i]
                for j in range(1,10):
                    insert_val["lat"] = insert_val["lat"] + lat_difference
                    insert_val["lng"] = insert_val["lng"] + lng_difference
                    copy_list.insert(index + j, deepcopy(insert_val))
        pprint(copy_list)
        return copy_list

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
