from flask import Blueprint
from flask import Flask, render_template
# from hotpepper_utils import search_near_restaurants
#  from googlemaps_utils import *

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
        - 検索結果のお店の情報stores
            - 緯度経度lat, lng
            - 店名name
            - 住所address
            - 予算budget
            - 営業時間open
            - 駐車場の有無parking
            - ホットペッパーのページのURL url
            - その店がこのユーザにふぁぼられているかどうかis_stared
        - この2つを1つの辞書resultsにまとめて返す
    処理の実態はsearch_restaurantsとstar_restaurant, unstar_restaurantで
    エラー内容をセッションにぶち込む
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
                # 適当に数店舗省略してある
                {'lat': '38.2545477359', 'lng': '140.8759171692', 'name': 'marie lulu マリールゥルゥ', 'budget': {'average': '昼1000円／夜2000円', 'name': '1501～2000円', 'code': 'B001'}, 'open': '火～土、祝前日: 11:00～16:00 （料理L.O. 15:00）', 'parking': 'あり ：店前の有料コインパーキング', 'url': 'https://www.hotpepper.jp/strJ001101188/?vos=nhppalsa000016'}, {'lat': '38.2543225131', 'lng': '140.8769107048', 'name': '武屋食堂 北目町店', 'budget': {'average': '1500円/宴会時3500円', 'name': '1501～2000円', 'code': 'B001'}, 'open': '月～土、祝前日: 11:30～14:30 （料理L.O. 14:30 ドリンクL.O. 14:30）17:30～23:30 （料理L.O. 23:00 ドリンクL.O. 23:00）日、祝日: 17:30～22:30 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'あり ：運転される方の飲酒はお断りします。', 'url': 'https://www.hotpepper.jp/strJ000974391/?vos=nhppalsa000016'}, 
                {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '伊達の牛たん本舗 牛たん通り店', 'budget': {'average': '1,500円（通常平均）\u30001,500円（ランチ平均）', 'name': '1501～2000円', 'code': 'B001'}, 'open': '月～日、祝日、祝前日: 11:00～22:00 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'なし', 'url': 'https://www.hotpepper.jp/strJ000302316/?vos=nhppalsa000016'}, {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': '松島 仙台', 'budget': {'average': '3000円', 'name': '2001～3000円', 'code': 'B002'}, 'open': '月～土: 11:00～22:30 （料理L.O. 22:30 ドリンクL.O. 22:30）日、祝日: 10:00～22:30 （料理L.O. 22:30 ドリンクL.O. 22:30）', 'parking': 'あり ：契約駐車場', 'url': 'https://www.hotpepper.jp/strJ000718475/?vos=nhppalsa000016'}, 
                {'lat': '38.2602889240', 'lng': '140.8822469063', 'name': 'シャルール ホテルメトロポリタン仙台', 'budget': {'average': '1200円', 'name': '1501～2000円', 'code': 'B001'}, 'open': '月～日、祝日、祝前日: 09:00～19:00 （料理L.O. 18:30 ドリンクL.O. 18:30）', 'parking': 'あり ：レストラン2000円以上利用で2時間無料', 'url': 'https://www.hotpepper.jp/strJ000797021/?vos=nhppalsa000016'}, 
                {'lat': '38.2601694902', 'lng': '140.8821385879', 'name': 'Order cafe dining 仙台', 'budget': {'average': '1500円', 'name': '2001～3000円', 'code': 'B002'}, 'open': '月～日、祝日、祝前日: 07:00～22:00 （料理L.O. 22:00 ドリンクL.O. 22:00）', 'parking': 'なし', 'url': 'https://www.hotpepper.jp/strJ000054592/?vos=nhppalsa000016'}
            ]  
    }
    results = {}
    #TODO : とりあえずコメントアウト
    # results['points'] = mock_results['points']
    # points = [results['points']['origin']] + results['points']['waypoints'] + [results['points']['destination']]
    # results['stores'] = search_near_restaurants(points)
    return render_template('search_result.html', results=mock_results) # resultsが完成したらresults=resultsに変える

# search_result()