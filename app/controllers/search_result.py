from flask import Blueprint, session, render_template, redirect, url_for, request

from controllers.hotpepper_utils import search_near_restaurants
from controllers.googlemap_utils import GoogleMap_parsing

from models.favorites import FavoriteModel
from models.users import UserModel
from models.restaurants import RestaurantModel


app = Blueprint('search_result', __name__)


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
        - ルート表示route
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
            {'id': 'J001101188', 'lat': '38.2545477359', 'lng': '140.8759171692', 'name': 'marie lulu マリールゥルゥ', 'address': '宮城県仙台市青葉区北目町４－７\u3000HSGビル5F', 'open': '火～土、祝前日: 11:00～16:00 （料理L.O. 15:00）', 'parking': 'あり ：店前の有料コインパーキング', 'budget': '1501～2000円', 'url': 'https://www.hotpepper.jp/strJ001101188/?vos=nhppalsa000016', 'fav': False}, 
            {'id': 'J000974391', 'lat': '38.2543225131', 'lng': '140.8769107048', 'name': '武屋食堂 北目町店', 'address': '宮城県仙台市青葉区北目町2-28', 'open': '月～土、祝前日: 11:30～14:30 （料理L.O. 14:30 ドリンクL.O. 14:30）17:30～23:30 （料理L.O. 23:00 ドリンクL.O. 23:00）日、祝日: 17:30～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'あり ：運転される方の飲酒はお断りします。', 'budget': '1501～2000円', 'url': 'https://www.hotpepper.jp/strJ000974391/?vos=nhppalsa000016', 'fav': True}, 
            {'id': 'J000710330', 'lat': '38.2539089584', 'lng': '140.8772059764', 'name': '中国めしや 竹竹', 'address': '宮城県仙台市青葉区北目町２－２２', 'open': '月～土、祝前日: 11:00～14:3017:30～22:00', 'parking': 'あり', 'budget': '1501～2000円', 'url': 'https://www.hotpepper.jp/strJ000710330/?vos=nhppalsa000016', 'fav': False},
            {'id': 'J000683774', 'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '郷土料理 みやぎ乃 エスパル店', 'address': '宮城県仙台市青葉区中央１－１－１\u3000エスパルB１', 'open': '月～日、祝日、祝前日: 11:00～23:00', 'parking': 'なし ：お近くのパーキングエリアをご利用くださいませ。', 'budget': '3001～4000円', 'url': 'https://www.hotpepper.jp/strJ000683774/?vos=nhppalsa000016', 'fav': True}, 
            {'id': 'J000797021', 'lat': '38.2602889240', 'lng': '140.8822469063', 'name': 'シャルール ホテルメトロポリタン仙台', 'address': '宮城県仙台市青葉区中央１-1-1\u3000ホテルメトロポリタン仙台１階', 'open': '月～日、祝日、祝前日: 09:00～19:00 （料理L.O. 18:30 ドリンクL.O. 18:30）', 'parking': 'あり ：レストラン2000円以上利用で2時間無料', 'budget': '1501～2000円', 'url': 'https://www.hotpepper.jp/strJ000797021/?vos=nhppalsa000016', 'fav': False}, 
            {'id': 'J000054592', 'lat': '38.2601694902', 'lng': '140.8821385879', 'name': 'Order cafe dining 仙台', 'address': '宮城県仙台市青葉区中央１-1-1\u3000仙台駅2階', 'open': '月～日、祝日、祝前日: 07:00～22:00 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'なし', 'budget': '2001～3000円', 'url': 'https://www.hotpepper.jp/strJ000054592/?vos=nhppalsa000016', 'fav': True}
        ]  
    }
    mock_points = {
        'origin': "東北大学片平キャンパス",
        'destination': "仙台駅",
        'waypoints':[
            "e-Beans"
        ]
    }
    #とりあえずコメントアウト
    # googlemap = GoogleMap_parsing(mock_points['origin'], mock_points['destination'], mock_points['waypoints'])
    # results = {}
    # results['points'] = mock_points
    # results['stores'] = search_near_restaurants(googlemap.get_route())
    #とりあえずコメントアウト

 
    # print(results)
    
    # ユーザid取得
    # token = session['twitter_token']
    
    with UserModel() as User:
        # User.create_user('noisy_noimin', 'Noimin', icon_url="", token="token", secret="secret")
        try:
            user = User.get_user_by_token(token='token')
        except:
            return redirect(url_for('login')) # ログアウトされてたらloginページにリダイレクト
    
    if user:
        user_id = user[0].id
    else:
        return redirect(url_for('login'))


    with FavoriteModel() as Favorite, RestaurantModel() as Restaurant:
        # Restaurant.create_restaurant('J000054592', 38.2601694902, 140.8821385879, 'Order cafe dining 仙台', '宮城県仙台市青葉区中央１-1-1\u3000仙台駅2階', '月～日、祝日、祝前日: 07:00～22:00 （料理L.O. 22:00 ドリンクL.O. 22:00）', '2001～3000円', 'なし', 'https://www.hotpepper.jp/strJ000054592/?vos=nhppalsa000016')
        # Favorite.create_fav(1, 1)
        # Restaurant.create_restaurant('J001177343', 38.2603907956, 140.8801562494, '天ぷら寿司 えびす', '宮城県仙台市青葉区中央１-10-25\u3000EDEN仙台', '月～日、祝日、祝前日: 11:30～14:00 （料理L.O. 14:00 ドリンクL.O. 14:00）17:00～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）', '3001～4000円', 'あり ：近くにコインパーキングございます。', 'https://www.hotpepper.jp/strJ001177343/?vos=nhppalsa000016')
        # Favorite.create_fav(2, 2)
        try:
            favorites = Favorite.get_restaurants_by_id_user(user_id)
            favorite_restaurants = [Restaurant.get_restaurant_by_id(favorite_restaurant.id)[0] for favorite_restaurant in favorites]
        except:
            return redirect(url_for('login')) # ログアウトされてたらloginページにリダイレクト
    
    for idx, restaurant in enumerate(results['stores']):
<<<<<<< HEAD
        results['stores'][idx]['fav'] = restaurant in favorite_restaurants
    print(results)
    """

    return render_template('search_result.html', results=mock_results)# resultsが完成したらresults=resultsに変える



# search_result()
=======
        results['stores'][idx]['fav'] = False
        for favorite_restaurant in favorite_restaurants:
            if restaurant['id'] == favorite_restaurant.store_id:
                results['stores'][idx]['fav'] = True

    return render_template('search_result.html', results=results) # resultsが完成したらresults=resultsに変える
>>>>>>> develop
