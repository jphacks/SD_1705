from flask import Blueprint, session, render_template, redirect, url_for, request

from models.favorites import FavoriteModel
from models.users import UserModel
from models.restaurants import RestaurantModel

app = Blueprint('fav', __name__)

@app.route('/fav', methods=['POST'])
def fav():
    '''
    お店をお気に入り登録する
    '''
    # ユーザIDを求める
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

    store_id = request.form('store_id')
    print(store_id, user_id)
    with FavoriteModel() as Favorite:
        print(Favorite.is_exist(user_id, store_id))
        if not Favorite.is_exist(user_id, store_id):
            # レストラン追加
            with RestaurantModel() as Retaurant:
                Retaurant.create_restaurant(
                    store_id=store_id, 
                    lat=request.form['lat'],
                    lng=request.form['lng'],
                    genre=request.form['genre'],
                    name=request.form['name'],
                    address=request.form['address'],
                    budget=request.form['budget'],
                    open=request.form['open'],
                    parking=request.form['parking'],
                    url=request.form['url']
                )
        return Favorite.create_fav(id_user=user_id, id_restaurant=store_id)

    return None