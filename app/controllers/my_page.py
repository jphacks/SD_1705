from flask import Blueprint, render_template, session, redirect, url_for, request
import json

from controllers.hotpepper_utils import check_open

from models.users import UserModel
from models.favorites import FavoriteModel
from models.restaurants import RestaurantModel

app = Blueprint('my_page', __name__)


@app.route('/my_page', methods=['GET'])
def my_page():
    if session.get('twitter_id') is None:
        session['is_login'] = False
        return redirect(url_for('login.login'))

    budget = request.args.get('budget')
    genre = request.args.get('genre')

    print(budget)
    user_id = session['twitter_id']

    with UserModel() as User:
        user_info =User.get_user_by_twitter_id(twitter_id=user_id)[0]
        user = {
            'id': user_info.twitter_id,
            'name': user_info.user_name,
            'icon_url': user_info.icon_url
        }

    with FavoriteModel() as Favorite:
        favorites = Favorite.get_restaurants_by_id_user(session['twitter_id'])

    restaurants = []
    with RestaurantModel() as Restaurant:
        for favorite in favorites:
            data = Restaurant.get_restaurant_by_store_id(favorite.id_restaurant, budget=budget, genre=genre)[0]
            try:
                if check_open(data.open):
                    open_status = "営業中: "
                else:
                    open_status = "準備中: "
            except:
                open_status = ""
            
            if data is not None:
                restaurants.append({
                    'id': data.store_id,
                    'lat': data.lat,
                    'lng': data.lng,
                    'genre': data.genre,
                    'name': data.name,
                    'address': data.address,
                    'budget': data.budget,
                    'open': open_status+data.open,
                    'parking': data.parking,
                    'url': data.url,
                    'img_url': data.img_url
                })

    return render_template(
                'my_page.html',
                user=user,
                restaurants=restaurants
            )
