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
    lat = Column(Numeric, nullable=False)
    lng = Column(Numeric, nullable=False)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    budget = Column(Text, nullable=False)
    open = Column(Text, nullable=False)
    parking = Column(Boolean, nullable=False)
    url = Column(Text, nullable=False)
    created_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    update_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    delete_at = Column(sqlalchemy.Text, default=None)


class Favorites(Base):
    '''
    favoiteテーブルのカラム
    '''
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, nullable=False)
    id_restaurant = Column(Integer, nullable=False)
    created_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    update_at = Column(Date, server_default=sqlalchemy.sql.func.now(), nullable=False)
    delete_at = Column(sqlalchemy.Text, default=None)


def create_tables():
    '''
    テーブルデータの作成
    '''
    Base.metadata.create_all(engine)