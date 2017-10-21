from flask import Blueprint, session, render_template, redirect, url_for, request

from hotpepper_utils import search_near_restaurants
from googlemap_utils import GoogleMap_parsing

import sys; sys.path.append('/Users/yoshinari/work/SD_1705/app') # いらなくなるかも
from models.favorites import FavoriteModel
from models.users import UserModel
from models.restaurants import RestaurantModel


app = Blueprint('search_result', __name__, template_folder='templates')


@app.route('/search_result', methods=['GET'])
def search_result():
    """
    GET元: top
    render先: search_result.html?
    入力: 
        出発地origin，到着地destination，(あれば)経由地の地点名waypoints
        または
        starかunstarか(is_stared), star/unstarされたお店の一通りの情報(store: 辞書の中身は出力に倣う)
        入力がどちらなのかによって処理を変える
    出力: 
        - 出発地・到着地・(あれば)経由地の緯度経度points
            {
                origin: {lat:0, lng:0}, 
                destination: {lat:0, lng:0}, 
                waypoints:[
                    {lat:0, lng:0}, {lat:1, lng:1}, ...
                ]
            }
        - ルート表示root
            - placeIdのリスト
        - 検索結果のお店の情報stores
            - 緯度経度lat, lng
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
    mock_results = {
        'points': {
            'origin': {'lat': 38.253834, 'lng': 140.87407400000006}, # 片平キャンパス
            'destination': {'lat': 38.2601316, 'lng': 140.88243750000004}, # 仙台駅
            'waypoints':[
                {'lat': 38.258623, 'lng': 140.879684} # e-Beans
            ]
        },
        'route': [
            {'lat': 38.2550648, 'lng': 140.8733472}, {'lat': 38.2549348, 'lng': 140.8729901}, {'lat': 38.2561386, 'lng': 140.8723537}, {'lat': 38.2560644, 'lng': 140.8720585}, {'lat': 38.2593788, 'lng': 140.8709787}, {'lat': 38.2607307, 'lng': 140.8778758}, {'lat': 38.2584622, 'lng': 140.8792068}, {'lat': 38.25769409999999, 'lng': 140.8796827}, {'lat': 38.2579533, 'lng': 140.8809551}, {'lat': 38.2597031, 'lng': 140.8799099}, {'lat': 38.2601316, 'lng': 140.8810914}
        ],
        'stores': [
            {'lat': '38.2545477359', 'lng': '140.8759171692', 'name': 'marie lulu マリールゥルゥ', 'address': '宮城県仙台市青葉区北目町４－７\u3000HSGビル5F', 'budget': '1501～2000円', 'open': '火～土、祝前日: 11:00～16:00 （料理L.O. 15:00）', 'parking': 'あり ：店前の有料コインパーキング', 'url': 'https://www.hotpepper.jp/strJ001101188/?vos=nhppalsa000016'}, {'lat': '38.2543225131', 'lng': '140.8769107048', 'name': '武屋食堂 北目町店', 'address': '宮城県仙台市青葉区北目町2-28', 'budget': '1501～2000円', 'open': '月～土、祝前日: 11:30～14:30 （料理L.O. 14:30 ドリンクL.O. 14:30）17:30～23:30 （料理L.O. 23:00 ドリンクL.O. 23:00）日、祝日: 17:30～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'あり ：運転される方の飲酒はお断りします。', 'url': 'https://www.hotpepper.jp/strJ000974391/?vos=nhppalsa000016', 'fav': True}, 
            {'lat': '38.2539089584', 'lng': '140.8772059764', 'name': '中国めしや 竹竹', 'address': '宮城県仙台市青葉区北目町２－２２', 'budget': '1501～2000円', 'open': '月～土、祝前日: 11:00～14:3017:30～22:00', 'parking': 'あり', 'url': 'https://www.hotpepper.jp/strJ000710330/?vos=nhppalsa000016', 'fav': False}, 
            {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '郷土料理 みやぎ乃 エスパル店', 'address': '宮城県仙台市青葉区中央１－１－１\u3000エスパルB１', 'budget': '3001～4000円', 'open': '月～日、祝日、祝前日: 11:00～23:00', 'parking': 'なし ：お近くのパーキングエリアをご利用くださいませ。', 'url': 'https://www.hotpepper.jp/strJ000683774/?vos=nhppalsa000016', 'fav': True}, 
            {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '寿司田 仙台駅ビル店', 'address': '宮城県仙台市青葉区中央１‐１‐１ 仙台エスパルＢ１', 'budget': '3001～4000円', 'open': '月～日、祝日、祝前日: 11:00～23:00 （料理L.O. 22:30 ドリンクL.O. 22:30）', 'parking': 'なし', 'url': 'https://www.hotpepper.jp/strJ000279012/?vos=nhppalsa000016', 'fav': False}
        ]  
    }
    mock_points = {
        'origin': "東北大学片平キャンパス",
        'destination': "仙台駅",
        'waypoints':[
            "e-Beans"
        ]
    }
    
    googlemap = GoogleMap_parsing(mock_points['origin'], mock_points['destination'], mock_points['waypoints'])
    results = {}
    results['points'] = mock_points
    results['stores'] = search_near_restaurants(googlemap.get_route())
    # print(results)
    
    # ユーザid取得
    # token = session['twitter_token']
    
    with UserModel() as User:
        # User.create_user('noisy_noimin', 'Noimin', icon_url="", token="token", secret="secret")
        try:
            user = User.get_user_by_token(token='token')
            user_id = user[0].id
        except:
            return redirect(url_for('login')) # ログアウトされてたらloginページにリダイレクト
    
    with FavoriteModel() as Favorite, RestaurantModel() as Restaurant:
        # Favorite.create_fav(user_id, 1145141919810)
        # Restaurant.create_restaurant(lat=0, lng=0, name="野獣レストラン", address="日本", budget="810円", open="8時から10時まで", parking="無", url="")
        # Restaurant.create_restaurant('38.2603907956', '140.8801562494', '天ぷら寿司 えびす', '宮城県仙台市青葉区中央１-10-25\u3000EDEN仙台', '3001～4000円', '月～日、祝日、祝前日: 11:30～14:00 （料理L.O. 14:00 ドリンクL.O. 14:00）17:00～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'あり ：近くにコインパーキングございます。', 'https://www.hotpepper.jp/strJ001177343/?vos=nhppalsa000016')
        # Favorite.create_fav(user_id, 3)
        try:
            favorites = Favorite.get_restaurants_by_id_user(user_id)
            favorite_restaurants = [Restaurant.get_restaurant_by_id(favorite_restaurant.id)[0] for favorite_restaurant in favorites]
        except:
            return redirect(url_for('login')) # ログアウトされてたらloginページにリダイレクト
    
    for idx, restaurant in enumerate(results['stores']):
        results['stores'][idx]['fav'] = False
        for favorite_restaurant in favorite_restaurants:
            

    return render_template('search_result.html', results=mock_results) # resultsが完成したらresults=resultsに変える



search_result()