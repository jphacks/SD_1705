from flask import Blueprint, session, render_template, redirect, url_for, request

from models.favorites import FavoriteModel
from models.users import UserModel
from models.restaurants import RestaurantModel

app = Blueprint('fav', __name__)

@app.route('/fav', methods=['POST'])
def fav():
    '''
    お店をお気に入り登録する/お気に入りから削除する
    '''
    # ユーザIDを求める
    if session.get('twitter_id') is not None:
        twitter_id = session['twitter_id']
    else:
        session['is_login'] = False
        return redirect(url_for('login.login'))
    
    store_id = request.form['id']
    
    with FavoriteModel() as Favorite:
        if not Favorite.is_exist(twitter_id, store_id):
            # ふぁぼする
            # レストラン追加
            with RestaurantModel() as Restaurant:
                if not Restaurant.get_restaurant_by_store_id(store_id)[0]:
                    Restaurant.create_restaurant(
                        store_id=store_id, 
                        lat=request.form['lat'],
                        lng=request.form['lng'],
                        genre=request.form['genre'],
                        name=request.form['name'],
                        address=request.form['address'],
                        budget=request.form['budget'],
                        open=request.form['open'],
                        parking=request.form['parking'],
                        url=request.form['url'],
                        img_url=(request.form['img_url'] if request.form['img_url'] else None)
                    )
            ret = Favorite.create_fav(id_user=twitter_id, id_restaurant=store_id)
            print(ret)
        else:
            #ふぁぼ解除する
            with FavoriteModel() as Favorite:
                ret = Favorite.delete_fav(id_user=twitter_id, id_restaurant=store_id)
                print(ret)
                

    return ""