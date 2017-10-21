"""
緯度経度からなる点ごとに近い飲食店を探す
"""

import requests
import json
import re

pattern_days = re.compile(r"([月火水木金土日][:：])")

budget_dict = {"〜500円":"B009","501〜1000円":"B010","1001〜1500円":"B011","1501〜2000円":"B001","2001〜3000円":"B002","3001〜4000円":"B003","4001〜5000円":"B008","5001〜7000円":"B004","7001〜10000円":"B005","10001〜15000円":"B006","15001〜20000円":"B012","20001〜30000円":"B013","30001円〜":"B014"}
genre_dict = {'居酒屋': 'G001','ダイニングバー': 'G002','創作料理': 'G003','和食': 'G004','洋食': 'G005','イタリアン・フレンチ': 'G006','中華': 'G007','焼肉・韓国料理': 'G008','アジアン': 'G009','各国料理': 'G010','カラオケ・パーティ': 'G011','バー・カクテル': 'G012','ラーメン': 'G013','お好み焼き・もんじゃ・鉄板焼き': 'G016','カフェ・スイーツ': 'G014','その他グルメ': 'G015'}

def search_near_restaurants(points, budget, genre):
    """
    入力: 緯度と経度のiterableを受け取る
    出力:
        - 近い飲食店の情報リスト
            - 各店舗について
                - 緯度経度
                - ジャンル
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
        near_restaurants = get_restaurants(lat, lng, budget, genre)
        for restaurant in near_restaurants:
            restaurant_dict = { attr: restaurant[attr] for attr in attrs }
            restaurant_dict['genre'] = restaurant['genre']['name']
            restaurant_dict['budget'] = restaurant['budget']['name']
            restaurant_dict['url'] = restaurant['urls']['pc'] # 仮にPC用のURLのみ取得

            restaurant_dict['open'] = restaurant_dict['open'].replace('（', '<br />（').replace('）', "）<br />")
            pattern_days.sub(r"\1<br />", restaurant_dict['open'])
            restaurant_dict['parking'] = restaurant_dict['parking'].split('：')[0]
            
            if restaurant_dict not in ret:
                ret.append(restaurant_dict)
    return ret


def get_restaurants(lat, lng, budget, genre):
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
    if budget:
        params['budget'] = budget_dict[budget]
    if genre:
        params['genre'] = genre_dict[genre]
        print(params['genre'])
    request = requests.get(base_url, params=params)
    results = json.loads(request.text)['results']
    if 'shop' in results.keys():
        return results['shop']
    else:
        return []


if __name__ == '__main__':
    # とりあえず片平キャンパスと仙台駅でテスト
    restaurants = search_near_restaurants([{'lat': 38.253834, 'lng': 140.87407400000006,'lat': 38.2601316, 'lng': 140.88243750000004}])
    print(restaurants)
    # レストランがない場合
    restaurants = search_near_restaurants([{'lat': 0, 'lng': 0}])
    print(restaurants)