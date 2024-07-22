import databases
import sqlalchemy
from Seminar_6_Additional_opportunities_FastApi.HW.settings.settings import settings
from Seminar_6_Additional_opportunities_FastApi.HW.model.models_orders import Status

DATABASE_URL = settings.DATABASE_URL
# DATABASE_URL = 'postgresql://user:password@localhost/dbname'

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer,
                                           primary_key=True),
                         sqlalchemy.Column('first_name',
                                           sqlalchemy.String(32)),
                         sqlalchemy.Column('last_name',
                                           sqlalchemy.String(32)),
                         sqlalchemy.Column('email', sqlalchemy.String(128)),
                         sqlalchemy.Column('password', sqlalchemy.String(32))
                         )

products = sqlalchemy.Table('products',
                            metadata,
                            sqlalchemy.Column('id', sqlalchemy.Integer,
                                              primary_key=True),
                            sqlalchemy.Column('name',
                                              sqlalchemy.String(32)),
                            sqlalchemy.Column('description',
                                              sqlalchemy.String(32)),
                            sqlalchemy.Column('price', sqlalchemy.Integer),
                            )

orders = sqlalchemy.Table('orders',
                          metadata,
                          sqlalchemy.Column('id', sqlalchemy.Integer,
                                            primary_key=True),
                          sqlalchemy.Column('id_user',
                                            sqlalchemy.ForeignKey('users.id')),
                          sqlalchemy.Column('id_product',
                                            sqlalchemy.ForeignKey('products.id')),
                          sqlalchemy.Column('date_order',
                                            sqlalchemy.String(128)),
                          sqlalchemy.Column('status', sqlalchemy.Enum(Status)),
                          )

engine = sqlalchemy.create_engine(DATABASE_URL,
                                  connect_args={'check_same_thread': False})

metadata.create_all(engine)
