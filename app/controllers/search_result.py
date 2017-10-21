from flask import Blueprint, session, render_template, redirect, url_for, request

from hotpepper_utils import search_near_restaurants
#  from googlemaps_utils import *

import sys; sys.path.append('/Users/yoshinari/work/SD_1705/app') # いらなくなるかも
from models.favorites import FavoriteModel
from models.users import UserModel


app = Blueprint('search_result', __name__, template_folder='templates')


@app.route('/search_result', method=['GET'])
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
        'stores': 
            [
                {'lat': '38.2545477359', 'lng': '140.8759171692', 'name': 'marie lulu マリールゥルゥ', 'address': '宮城県仙台市青葉区北目町４－７\u3000HSGビル5F', 'budget': {'average': '昼1000円／夜2000円', 'name': '1501～2000円', 'code': 'B001'}, 'open': '火～土、祝前日: 11:00～16:00 （料理L.O. 15:00）', 'parking': 'あり ：店前の有料コインパーキング', 'url': 'https://www.hotpepper.jp/strJ001101188/?vos=nhppalsa000016'}, {'lat': '38.2543225131', 'lng': '140.8769107048', 'name': '武屋食堂 北目町店', 'address': '宮城県仙台市青葉区北目町2-28', 'budget': {'average': '1500円/宴会時3500円', 'name': '1501～2000円', 'code': 'B001'}, 'open': '月～土、祝前日: 11:30～14:30 （料理L.O. 14:30 ドリンクL.O. 14:30）17:30～23:30 （料理L.O. 23:00 ドリンクL.O. 23:00）日、祝日: 17:30～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'あり ：運転される方の飲酒はお断りします。', 'url': 'https://www.hotpepper.jp/strJ000974391/?vos=nhppalsa000016', 'fav': True}, 
                {'lat': '38.2539089584', 'lng': '140.8772059764', 'name': '中国めしや 竹竹', 'address': '宮城県仙台市青葉区北目町２－２２', 'budget': {'average': '昼750円／夜1000円', 'name': '1501～2000円', 'code': 'B001'}, 'open': '月～土、祝前日: 11:00～14:3017:30～22:00', 'parking': 'あり', 'url': 'https://www.hotpepper.jp/strJ000710330/?vos=nhppalsa000016', 'fav': False}, 
                {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '郷土料理 みやぎ乃 エスパル店', 'address': '宮城県仙台市青葉区中央１－１－１\u3000エスパルB１', 'budget': {'average': '1500円（通常平均）\u30002500円（宴会平均）\u30001250円（ランチ平均）', 'name': '3001～4000円', 'code': 'B003'}, 'open': '月～日、祝日、祝前日: 11:00～23:00', 'parking': 'なし ：お近くのパーキングエリアをご利用くださいませ。', 'url': 'https://www.hotpepper.jp/strJ000683774/?vos=nhppalsa000016', 'fav': True}, 
                {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '寿司田 仙台駅ビル店', 'address': '宮城県仙台市青葉区中央１‐１‐１ 仙台エスパルＢ１', 'budget': {'average': '3000円', 'name': '3001～4000円', 'code': 'B003'}, 'open': '月～日、祝日、祝前日: 11:00～23:00 （料理L.O. 22:30 ドリンクL.O. 22:30）', 'parking': 'なし', 'url': 'https://www.hotpepper.jp/strJ000279012/?vos=nhppalsa000016', 'fav': False}
            ]  
    }
    results = {}
    results['points'] = mock_results['points']
    points = [results['points']['origin']] + results['points']['waypoints'] + [results['points']['destination']]
    results['stores'] = search_near_restaurants(points)
    # ユーザid取得
    with UserModel() as user:
        try:
            user_data = user.get_user_by_token(session.pop('twitter_token', None))[0]
            user_id = user_data.twitter_id
            print(user_data)
        except:
            redirect(url_for('login')) # ログアウトされてたらloginページにリダイレクト
    # ふぁぼられてるかどうかチェック
    with FavoriteModel() as favorite:
        for restaurant in results['stores']:
            pass
    return render_template('search_result.html', results=mock_results) # resultsが完成したらresults=resultsに変える

search_result()