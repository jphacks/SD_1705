"""
緯度経度からなる点ごとに近い飲食店を探す
"""

import requests

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
    near_restaurants = set()
    for lat, lng in points:
        near_restaurants.update(get_restaurants(lat, lng))
    
    return list(near_restaurants)

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
    print(request.text['result'])
    return []

#とりあえず片平キャンパスと仙台駅
print(search_near_restaurants([(38.253834, 140.87407400000006), (38.2601316, 140.88243750000004)]))