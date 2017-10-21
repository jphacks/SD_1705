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

    def create_restaurant(self, lat, lng, name, address, budget, open, parking, url):
       '''
       新しいお店を登録
       :param lat: 緯度
       :param lng: 軽度
       :param name: 名前
       :param address: 住所
       :param budget: 予算
       :param open: 営業時間
       :param parking: 駐車場
       :param url: ホットペッパーのurl
       :return: [Restaurant]
       '''
       new_restaurant = Restaurant(
           lat=lat,
           lng=lng,
           name=name,
           address=address,
           budget=budget,
           open=open,
           parking=parking,
           url=url
       )
       self.session.add(new_restaurant)
       self.session.flush()
       self.session.commit()
       return [new_restaurant]

    def get_restaurant_by_id(self, id):
        '''
        お店をidで引っ張ってくる
        :param id: お店のid
        :return: [Restaurant]
        '''
        restaurant_data = self.session.query(Restaurant).filter_by(id=id).one()
        return [restaurant_data]