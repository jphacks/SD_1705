from flask import Blueprint, render_template, session, redirect, url_for
import json

from models.users import UserModel
from models.favorites import FavoriteModel
from models.restaurants import RestaurantModel

app = Blueprint('my_page', __name__)


@app.route('/my_page', methods=['GET'])
def my_page():
    if session.get('twitter_id') is None:
        session['is_login'] = False
        return redirect(url_for('login.login'))

    user_id = session['twitter_id']

    user = {}
    with UserModel() as User:
        user_info =User.get_user_by_twitter_id(twitter_id=user_id)[0]
        user = {
            'id': user_info.twitter_id,
            'name': user_info.user_name,
            'icon_url': user_info.icon_url
        }
    # print(user['id'])
    with FavoriteModel() as Favorite:
        favorites = Favorite.get_restaurants_by_id_user(session['twitter_id'])

    print(favorites)
    restaurants = []
    with RestaurantModel() as Restaurant:
        for favorite in favorites:
            data = Restaurant.get_restaurant_by_store_id(favorite.id_restaurant)[0]
            restaurants.append({
                'id': data.store_id,
                'lat': data.lat,
                'lng': data.lng,
                'genre':data.genre,
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
