from flask import Blueprint, session, render_template, redirect, url_for, request
from pprint import pprint

from controllers.hotpepper_utils import search_near_restaurants
from controllers.googlemap_utils import GoogleMap_parsing

from models.favorites import FavoriteModel
from models.users import UserModel
from models.restaurants import RestaurantModel


MAX = 1  #unknown_errorが起きた際の最大やり直し回数
app = Blueprint('search_result', __name__)
way_dict = {'車': 'driving', '徒歩': 'walking', '自転車': 'bicycling', '公共交通機関': 'transit'}

@app.route('/search_result', methods=['GET', 'POST'])
def search_result():
    """
    GET元: top
    render先: search_result.html?
    入力: 
        出発地origin，到着地destination，(あれば)経由地の地点名waypoints
        または
        star/unstarされたお店のstore_id
        入力がどちらなのかによって処理を変える
    出力: 
        - 出発地・到着地・(あれば)経由地の緯度経度points
            {
                origin: {name: hoge, lat:0, lng:0}, 
                destination: {name: fuga, lat:0, lng:0}, 
                waypoints:[
                    {name: ago, lat:0, lng:0}, {name: kubi, lat:1, lng:1}, ...
                ]
            }
        - ルート表示route
        - 検索結果のお店の情報stores
            - 緯度経度lat, lng
            - hotpepperのID store_id
            - 店名name
            - 住所address
            - 予算budget
            - 営業時間open
            - 駐車場の有無parking
            - ホットペッパーのページのURL url
            - その店がこのユーザにふぁぼられているかどうかfav
        - この2つを1つの辞書resultsにまとめて返す
    処理の実態はsearch_restaurantsとstar_restaurant, unstar_restaurantで
    エラー内容をセッションにぶち込む(UNKNOWN_ERRORならもう一回呼び出す)
    """
    input_from_front = {
        'fav': True,
        'store_id': 'J001101188'
    }

    # ユーザID求める
    if session.get('twitter_token') is not None:
        token = session['twitter_token']
    else:
        session['is_login'] = False
        return redirect(url_for('login.login'))
    with UserModel() as User:
        try:
            user = User.get_user_by_token(token=token)
        except:
            return redirect(url_for('login.login')) # ログアウトされてたらloginページにリダイレクト
    if user:
        user_id = user[0].id
    else:
        return redirect(url_for('login.login'))
    
    origin = request.args.get('origin')
    destination = request.args.get('dest')
    waypoints = []
    i = 0
    while True:
        waypoint = request.args.get('way{}'.format(i))
        if not waypoint:
            break
        waypoints.append(waypoint)
        i += 1
    budget = request.form['budget']
    genre = request.form['genre']
    range_ = request.form['range']
    if not range_:
        range_ = '300m'
    way = request.form['way']
    if way:
        mode = way_dict[way]
    else:
        mode = 'driving'

    googlemap = GoogleMap_parsing(origin, destination, waypoints, mode=mode)

    status = googlemap.get_input_location_status()
    errors = {
        'NOT_FOUND': status[1],
        'ZERO_RESULTS': (status[0] == 'ZERO_RESULTS'),
        'UNKNOWN_ERROR': (status[0] == 'UNKNOWN_ERROR')
    }

    for _ in range(MAX):
        if status[0] == 'OK':
            results = {}

            latlngs = []
            routes = googlemap.result_of_gm_api['routes'][0]['legs']
            latlngs.append(routes[0]['start_location'])
            for route in routes:
                latlngs.append(route['end_location'])
            results['points'] = {
                'origin': {'name': origin, 'lat': latlngs[0]['lat'], 'lng': latlngs[0]['lng']}, 
                'destination': {'name': destination, 'lat': latlngs[-1]['lat'], 'lng': latlngs[-1]['lng']}, 
                'waypoints': []
            }
            for idx,latlng in enumerate(latlngs):
                results['points']['waypoints'].append({'name': waypoints[idx], 'lat': latlng['lat'], 'lng': latlng['lng']})
                
            results['stores'] = search_near_restaurants(googlemap.get_route(), budget=budget, genre=genre, range_=range_)

            with FavoriteModel() as Favorite, RestaurantModel() as Restaurant:
                try:
                    favorites = Favorite.get_restaurants_by_id_user(user_id)
                    favorite_restaurants = [Restaurant.get_restaurant_by_id(favorite_restaurant.id)[0] for favorite_restaurant in favorites]
                except:
                    return redirect(url_for('login.login')) # ログアウトされてたらloginページにリダイレクト
            
            for idx, restaurant in enumerate(results['stores']):
                results['stores'][idx]['fav'] = False
                for favorite_restaurant in favorite_restaurants:
                    if restaurant['id'] == favorite_restaurant.store_id:
                        results['stores'][idx]['fav'] = True

            return render_template('search_result.html', results=results)

        else:
            session['NOT_FOUND'] = errors['NOT_FOUND']
            session['ZERO_RESULTS'] = errors['ZERO_RESULTS']
            session['UNKNOWN_ERROR'] = errors['UNKNOWN_ERROR']
            return redirect(url_for('top.top_page'))

    else:
        session['NOT_FOUND'] = errors['NOT_FOUND']
        session['ZERO_RESULTS'] = errors['ZERO_RESULTS']
        session['UNKNOWN_ERROR'] = errors['UNKNOWN_ERROR']
        return redirect(url_for('top.top_page'))

def fav(user_id, store_id):
    with FavoriteModel() as Favorite:
        Favorite.create_fav(user_id, store_id)
    return # 返り値どうする

def unfav(user_id, store_id):
    with FavoriteModel() as Favorite:
        Favorite.create_fav(user_id, store_id)
    return# 返り値どうするの