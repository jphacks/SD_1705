"""
緯度経度からなる点ごとに近い飲食店を探す
"""

import requests
import json

def search_near_restaurants(points):
    """
    入力: 緯度と経度のiterableを受け取る
    出力:
        - 近い飲食店の情報リスト
            - 各店舗について
                - 緯度経度
                - 店名
                - 住所
                - 予算
                - 営業時間
                - 駐車場の有無
                - ホットペッパーのページのURL
    """
    ret = []
    attrs = ['id', 'lat', 'lng', 'name', 'address', 'open', 'parking']
    for point in points:
        lat = point['lat']
        lng = point['lng']
        near_restaurants = get_restaurants(lat, lng)
        for restaurant in near_restaurants:
            restaurant_dict = { attr: restaurant[attr] for attr in attrs }
            restaurant_dict['budget'] = restaurant['budget']['name']
            restaurant_dict['url'] = restaurant['urls']['pc'] # 仮にPC用のURLのみ取得
            restaurant_dict['parking'] = restaurant_dict['parking'].split('：')[0]
            if restaurant_dict not in ret:
                ret.append(restaurant_dict)
    return ret


def get_restaurants(lat, lng):
    """
    Hotpper APIにクエリを投げる
    """
    base_url = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    api_key = 'b61f3d3d92bbc454'
    params = {
        'key': api_key,
        'lat': lat,
        'lng': lng,
        'range': 1, # 与えられた地点から300m以内のお店を探す
        'format': 'json'
    }
    request = requests.get(base_url, params=params)
    results = json.loads(request.text)['results']
    if 'shop' in results.keys():
        return results['shop']
    else:
        return []


if __name__ == '__main__':
    # とりあえず片平キャンパスと仙台駅でテスト
    restaurants = search_near_restaurants([{'lat': 38.253834, 'lng': 140.87407400000006}, {'lat': 38.2601316, 'lng': 140.88243750000004}])
    print(restaurants)
    # レストランがない場合
    restaurants = search_near_restaurants([{'lat': 0, 'lng': 0}])
    print(restaurants)