import os
from sqlalchemy import create_engine, MetaData, Table, Column, Double, String, insert, select, update

db_path = os.path.join(os.path.dirname(__file__), './where-this.sqlite')
db_engine = create_engine(f'sqlite+pysqlite:///{db_path}')
metadata = MetaData()

photos_table = Table('photos', metadata,
    Column('provider_id', String, primary_key=True),
    Column('daily_challenge_date', String, nullable=True, unique=True, index=True),
    Column('photo_url', String, nullable=True),
    Column('author_url', String, nullable=True),
    Column('author_name', String, nullable=True),
    Column('location_name', String, nullable=True),
    Column('country_name', String, nullable=True),
    Column('country_code', String, nullable=True),
    Column('location_lat', Double, nullable=True),
    Column('location_lng', Double, nullable=True),
)

metadata.create_all(db_engine)

def create_photo(provider_id):
    query = insert(photos_table).values(provider_id = provider_id)
    with db_engine.connect() as connection:
        connection.execute(query)
        connection.commit()
    
    return {
        'provider_id': provider_id,
        'daily_challenge_date': None,
        'photo_url': None,
        'author_url': None,
        'author_name': None,
        'location_name': None,
        'country_name': None,
        'country_code': None,
        'location_lat': None,
        'location_lng': None
    }

def set_photo_data(provider_id, data):
    query = update(photos_table).where(photos_table.c.provider_id == provider_id).values(
        daily_challenge_date = data['daily_challenge_date'],
        photo_url = data['photo_url'],
        author_url = data['author_url'],
        author_name = data['author_name'],
        location_name = data['location_name'],
        country_name = data['country_name'],
        country_code = data['country_code'],
        location_lat = data['location_lat'],
        location_lng = data['location_lng']
    )
    with db_engine.connect() as connection:
        connection.execute(query)
        connection.commit()


def get_all():
    query = select(photos_table)
    result = []
    with db_engine.connect() as connection:
        result = connection.execute(query).all()
    return [map_row(row) for row in result]

def get_eligible():
    query = select(photos_table) \
        .where(photos_table.c.daily_challenge_date == None) \
        .where(photos_table.c.photo_url != None)
    result = []
    with db_engine.connect() as connection:
        result = connection.execute(query).all()
    return [map_row(row) for row in result]

def get_by_id(provider_id):
    query = select(photos_table).where(photos_table.c.provider_id == provider_id)
    result = None
    with db_engine.connect() as connection:
        result = connection.execute(query).first()
    return map_row(result)

def map_row(row):
    return {
        'provider_id': row[0],
        'daily_challenge_date': row[1],
        'photo_url': row[2],
        'author_url': row[3],
        'author_name': row[4],
        'location_name': row[5],
        'country_name': row[6],
        'country_code': row[7],
        'location_lat': row[8],
        'location_lng': row[9]
    }