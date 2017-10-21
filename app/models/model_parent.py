from sqlalchemy import *
import sqlalchemy.sql
import sqlalchemy.orm
import sqlalchemy.ext.declarative
Base = sqlalchemy.ext.declarative.declarative_base()
url = 'sqlite:///db/db.db'
engine = sqlalchemy.create_engine(url)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


class User(Base):
    '''
    usersテーブルのカラム
    '''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    twitter_id = Column(Integer, unique=True, nullable=False)
    user_name = Column(Text, nullable=False)
    icon_url = Column(Text)
    token = Column(Text, nullable=False)
    secret = Column(Text, nullable=False)
    created_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    update_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    delete_at = Column(sqlalchemy.Text, default=None)

    def __repr__(self):
        return u"<twitter_id:{}, user_name:{})>".format(self.twitter_id, self.user_name)


class Restaurant(Base):
    '''
    restaurantsテーブルのカラム
    '''
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    store_id = Column(Text, nullable=False)
    lat = Column(REAL, nullable=False)
    lng = Column(REAL, nullable=False)
    genre = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    budget = Column(Text, nullable=False)
    open = Column(Text, nullable=False)
    parking = Column(Boolean, nullable=False)
    url = Column(Text, nullable=False)
    created_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    update_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    delete_at = Column(sqlalchemy.Text, default=None)

    def __repr__(self):
        return "<id:{}, name:{}, lat:{}, lng{}>".format(self.id, self.name, self.lat, self.lng)


class Favorites(Base):
    '''
    favoiteテーブルのカラム
    '''
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, nullable=False)
    id_restaurant = Column(Text, nullable=False)
    created_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    update_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    delete_at = Column(sqlalchemy.Text, default=None)

    def __repr__(self):
        return "<id:{}, id_user:{}, id_restaurant_id:{}>".format(self.id, self.id_user, self.id_restaurant)


def create_tables():
    '''
    テーブルデータの作成
    '''
    Base.metadata.create_all(engine)