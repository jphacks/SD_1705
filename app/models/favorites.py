from models.model_parent import *


class FavoriteModel():

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

    def create_fav(self, id_user, id_restaurant):
        '''
        新しいお気に入りを登録
        :param id_user: ユーザid
        :param id_restaurant: レストランid
        :return: [fav]
        '''
        new_fav = Favorites(
            id_user=id_user,
            id_restaurant=id_restaurant
        )
        self.session.add(new_fav)
        self.session.flush()
        self.session.commit()
        return [new_fav]

    def delete_fav(self, id_user, id_restaurant):
        del_fav = self.session.query(Favorites).filter_by(id_user=id_user, id_restaurant=id_restaurant).first()
        self.session.delete(del_fav)
        self.session.flush()
        self.session.commit()
        return []

    def get_restaurants_by_id_user(self, id_user):
        '''
        あるユーザがファボった複数のお店を返す
        :param id_user:
        :return: [Restaurant1, Restaurant2, ... ]
        '''
        restaurants_data = self.session.query(Favorites).filter_by(id_user=id_user).all()
        return restaurants_data

    def get_restaurants_by_id_restaurant(self, id_restaurant):
        '''
        あるお店をファボっているユーザを複数返す
        :param id_user:
        :return: [Restaurant1, Restaurant2, ... ]
        '''
        restaurants_data = self.session.query(Favorites).filter_by(id_restaurant=id_restaurant).all()
        return restaurants_data

    def is_exist(self, id_user, id_restaurant):
        '''
        ファボがすでに存在するかどうか
        '''
        restaurants_data = self.session.query(Favorites).filter_by(id_user=id_user, id_restaurant=id_restaurant).all()
        return bool(restaurants_data)