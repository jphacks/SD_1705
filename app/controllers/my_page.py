from flask import Blueprint, render_template, session, redirect, url_for
import json

from models.users import UserModel
from models.favorites import FavoriteModel
from models.restaurants import RestaurantModel

app = Blueprint('my_page', __name__)


@app.route('/my_page', methods=['GET'])
def my_page():

    # ログインしていなかった時
    # if 'twitter_token' not in session:
    #     session['is_login'] = False
    #     redirect(url_for('login'))
    #
    # token = session['twitter_token']

    token = 'token'
    with UserModel() as User:
        user = User.get_user_by_token(token=token)

    with FavoriteModel() as Favorite:
        favorites = Favorite.get_restaurants_by_id_user(user[0].id)

    restaurants = []
    with RestaurantModel() as Restaurant:
        for favorite in favorites:
            data = Restaurant.get_restaurant_by_id(favorite.id)[0]
            restaurants.append({
                'id': data.id,
                'lat': data.lat,
                'lng': data.lng,
                'name': data.name,
                'address': data.address,
                'budget': data.budget,
                'open': data.open,
                'parking': data.parking,
                'url': data.url
            })

    return render_template(
            'my_page.html',
            restaurants=restaurants
            )
