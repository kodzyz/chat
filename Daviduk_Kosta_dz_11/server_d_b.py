from sqlalchemy import __version__, create_engine, Table, Column, \
    Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker

database = create_engine('sqlite:///server.db3', echo=False, pool_recycle=7200)

metadata = MetaData()
client_table = Table('client', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('login', String, unique=True),
                     Column('info', String)
                     )

story_table = Table('story', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('data', DateTime),
                    Column('ip_address', String),
                    Column('client', ForeignKey('client.id'))
                    )

contacts_table = Table('contacts', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('owner_id', ForeignKey('client.id')),
                       Column('client_id', ForeignKey('client.id'))
                       )

metadata.create_all(database)


class Client:
    def __init__(self, login, info):
        self.id = None
        self.login = login
        self.info = info

    def __repr__(self):
        return f'<User({self.login}, {self.info})>'


class Story:
    def __init__(self, data, ip_address, client_id):
        self.id = None
        self.data = data
        self.ip_address = ip_address
        self.client = client_id

    def __repr__(self):
        return f'<User({self.data}, {self.ip_address})>'


class Contacts:
    def __init__(self, owner_id, client_id):
        self.id = None
        self.owner = owner_id
        self.client = client_id

    def __repr__(self):
        return f'<User({self.owner}, {self.client})>'


mapper(Client, client_table)
mapper(Story, story_table)
mapper(Contacts, contacts_table)

Session = sessionmaker(bind=database)
session = Session()


client = Client('kosty', 'KOSTYANTIN')
session.add(client)
session.commit()
print(client.id)  # 1



