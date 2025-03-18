from sqlalchemy import create_engine, MetaData, Table, Column, Double, String, insert, select, update

db_engine = create_engine('sqlite+pysqlite:///where-this.sqlite')
metadata = MetaData()

photos_table = Table('photos', metadata,
    Column('provider_id', String, primary_key=True),
    Column('daily_challenge_date', String, nullable=True, unique=True, index=True),
    Column('photo_url', String, nullable=True),
    Column('author_url', String, nullable=True),
    Column('author_name', String, nullable=True),
    Column('location_name', String, nullable=True),
    Column('location_country', String, nullable=True), # iso code
    Column('location_lat', Double, nullable=True),
    Column('location_lng', Double, nullable=True),
)

metadata.create_all(db_engine)

def create_photo(provider_id):
    query = insert(photos_table).values(provider_id = provider_id)
    with db_engine.connect() as connection:
        connection.execute(query)
        connection.commit()

def set_photo_data(provider_id, data):
    query = update(photos_table).where(photos_table.c.provider_id == provider_id).values(
        daily_challenge_date = data['daily_challenge_date'],
        photo_url = data['photo_url'],
        author_url = data['author_url'],
        author_name = data['author_name'],
        location_name = data['location_name'],
        location_country = data['location_country'],
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
        'location_country': row[6],
        'location_lat': row[7],
        'location_lng': row[8]
    }