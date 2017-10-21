from flask import Blueprint, render_template, session, redirect, url_for
import json

from models.users import UserModel
from models.favorites import FavoriteModel
from models.restaurants import RestaurantModel

app = Blueprint('my_page', __name__)


@app.route('/my_page', methods=['GET'])
def my_page():
    if session.get('twitter_token') is None:
        session['is_login'] = False
        return redirect(url_for('login.login'))

    token = session['twitter_token']

    user = {}
    with UserModel() as User:
        user_info = User.get_user_by_token(token=token)[0]
        user = {
            'id': user_info.twitter_id,
            'name': user_info.user_name,
            'icon_url': user_info.icon_url
        }
    # print(user['id'])
    with FavoriteModel() as Favorite:
        favorites = Favorite.get_restaurants_by_id_user(user['id'])

    # print(user['id'])
    # print(favorites)
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
    #print(len(favorites))

    return render_template(
            'my_page.html',
            user=user,
            restaurants=restaurants
            )
