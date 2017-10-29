from models.model_parent import *


class RestaurantModel():

    def __init__(self):
        self.closed = False
        self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        if self.closed:
            return
        self.session.closed = True
        self.session.close()

    def create_restaurant(self, store_id, lat, lng, genre, name, address, budget, open, parking, url, img_url):
       '''
       新しいお店を登録
       :param lat: 緯度
       :param lng: 軽度
       :param genre: ジャンル名
       :param name: 名前
       :param address: 住所
       :param budget: 予算
       :param open: 営業時間
       :param parking: 駐車場
       :param url: ホットペッパーのurl
       :param img_url: ShopListの横に表示するようの画像url
       :return: [Restaurant]
       '''
       new_restaurant = Restaurant(
           store_id=store_id,
           lat=lat,
           lng=lng,
           genre=genre,
           name=name,
           address=address,
           budget=budget,
           open=open,
           parking=parking,
           url=url,
           img_url=img_url
       )
       self.session.add(new_restaurant)
       self.session.flush()
       self.session.commit()
       return [new_restaurant]

    def get_restaurant_by_store_id(self, store_id, budget=None, genre=None):
        '''
        お店をstore_idで引っ張ってくる
        :param id: お店のid
        :return: [Restaurant]
        '''
        restaurant_data = self.session.query(Restaurant).filter_by(store_id=store_id)
        restaurant_data = restaurant_data.filter_by(budget=budget) if budget else restaurant_data
        restaurant_data = restaurant_data.filter_by(genre=genre) if genre else restaurant_data
        restaurant_data = restaurant_data.first()

        return [restaurant_data]