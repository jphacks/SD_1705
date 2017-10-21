from models.model_parent import *


class UserModel():

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

    def get_user_by_token(self, token):
        '''
        tokenで指定したユーザ１人を返す
        :param id: string
        :return: [User]
        '''
        try:
            user_data = self.session.query(User).filter_by(token=token).one()
            return [user_data]
        except Exception as e:
            return e

    def create_user(self, twitter_id, user_name, icon_url, token, secret):
        '''
        新しいユーザを登録
        :param  twitter_id: int,
                user_name: string,
                icon_url: string,
                token: string,
                secret: string
        }
        :return: [User]
        '''
        new_user = User(
            twitter_id=twitter_id,
            user_name=user_name,
            icon_url=icon_url,
            token=token,
            secret=secret
        )
        self.session.add(new_user)
        self.session.flush()
        self.session.commit()
        return [new_user]

    def update_user_token(self, twitter_id, user_name, token):
        '''
        ユーザのtoken情報を更新
        twitter_idで更新ユーザを識別
        :param user_name:
        :return: [User]
        '''
        try:
            user = self.session.query(User).filter_by(twitter_id=twitter_id).one()
            user.user_name = user_name
            user.token = token
            self.session.flush()
            self.session.commit()
            return [user]
        except Exception as e:
            return e
