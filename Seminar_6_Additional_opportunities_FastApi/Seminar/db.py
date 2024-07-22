import databases
import sqlalchemy
from settings import settings

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
                         sqlalchemy.Column('address', sqlalchemy.String(128)),
                         sqlalchemy.Column('password', sqlalchemy.String(32))
                         )

engine = sqlalchemy.create_engine(DATABASE_URL,
                                  connect_args={'check_same_thread': False})

metadata.create_all(engine)
