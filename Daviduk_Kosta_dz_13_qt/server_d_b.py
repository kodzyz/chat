from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime


class ServerBase:
    Base = declarative_base()

    class Client(Base):
        __tablename__ = 'client'
        id = Column(Integer, primary_key=True)
        login = Column(String)
        info = Column(String)

        def __init__(self, login, info):
            self.login = login
            self.info = info

        def __repr__(self):
            return f'<Client({self.login}, {self.info})>'

    class Story(Base):
        __tablename__ = 'story'
        id = Column(Integer, primary_key=True)
        data = Column(DateTime)
        ip_address = Column(String)
        client_id = Column(ForeignKey('client.id'))

        def __init__(self, data, ip_address, client_id):
            self.data = data
            self.ip_address = ip_address
            self.client_id = client_id

        def __repr__(self):
            return f'<Story({self.data}, {self.ip_address}, {self.client_id})>'

    class Contacts(Base):
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        owner_id = Column(ForeignKey('client.id'))
        client_id = Column(ForeignKey('client.id'))

        def __init__(self, owner_id, client_id):
            self.owner_id = owner_id
            self.client_id = client_id

        def __repr__(self):
            return f'<Contacts({self.owner_id}, {self.client_id})>'

    def __init__(self):
        self.engine = create_engine('sqlite:///server.db3', echo=False, pool_recycle=7200, connect_args={"check_same_thread": False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.commit()

    def save_log(self, login, info):
        """ если log есть в Client заполняем только Story
             ('ip_address', 'client_id' берем из Client)
            если нет - добавляем log в Client и заполняем Story
        """
        query = self.session.query(self.Client.login)
        if [True for i in query.all() if i[0] == login]:  # if login in в bd => X
            for id_ in self.session.query(self.Client.id).filter_by(login=login):
                login_id = id_[0]  # id <---- login
                for info_ in self.session.query(self.Client.info).filter_by(login=login):
                    login_info = info_[0]  # info <---- login
                    story = self.Story(data=datetime.datetime.now(), ip_address=login_info,
                                       client_id=login_id)  # новая только дата
                    self.session.add(story)
                    self.session.commit()
        else:
            client = self.Client(login=login, info=info)
            self.session.add(client)
            self.session.commit()
            story = self.Story(data=datetime.datetime.now(), ip_address=info, client_id=client.id)
            self.session.add(story)
            self.session.commit()

    def messages_db(self, client1, client2):
        """ если client1 пишет client2 или наоборот то
        они добавляют друг друга в свои списки контактов
        """
        for id_ in self.session.query(self.Client.id).filter_by(login=client1):
            login_id_1 = id_[0]  # находим id по имени client1
            for id__ in self.session.query(self.Client.id).filter_by(login=client2):
                login_id_2 = id__[0]  # находим id по имени client2
                query1 = self.session.query(self.Contacts.owner_id)
                query2 = self.session.query(self.Contacts.client_id)
                if ([True for i in query1.all() if i[0] == login_id_1] and [True for i in query2.all() if
                                                                            i[0] == login_id_2]) \
                        or ([True for i in query1.all() if i[0] == login_id_2] and [True for i in query2.all() if
                                                                                    i[0] == login_id_1]):
                    return
                contacts1 = self.Contacts(owner_id=login_id_1, client_id=login_id_2)
                contacts2 = self.Contacts(owner_id=login_id_2, client_id=login_id_1)
                self.session.add(contacts1)
                self.session.add(contacts2)
                self.session.commit()

    def get_contacts(self, log):
        """
        :param log: логин
        :return: список его контактов
        """
        list_contact_client_id = []
        for id_ in self.session.query(self.Client.id).filter_by(login=log):
            login_id_ = id_[0]
            query = self.session.query(self.Contacts.owner_id)
            # if client.id in в owner_id => list(Contacts.client_id)
            if [True for owner_id in query.all() if owner_id[0] == login_id_]:
                for contacts in self.session.query(self.Contacts.client_id).filter(self.Contacts.owner_id == login_id_):
                    list_contact_client_id.append(contacts[0])
        list_client_login = []
        for client_id in list_contact_client_id:
            client_login_query = self.session.query(self.Client.login).filter(self.Client.id == client_id)
            for clear_log in client_login_query:
                list_client_login.append(clear_log[0])
        if not list_client_login:
            return 400
        return list_client_login

    def add_contact(self, owner, add_contact):
        """
        :param owner:
        :param add_contact:
        :return:
        """
        for id_ in self.session.query(self.Client.id).filter_by(login=owner):
            contact_owner_id = id_[0]  # находим id по имени owner (табл.Client)
            for id__ in self.session.query(self.Client.id).filter_by(login=add_contact):
                add_contact_id = id__[0]  # находим id по имени add_contact (табл.Client)
                owner_id = self.session.query(self.Contacts.owner_id)
                client_id = self.session.query(self.Contacts.client_id)
                # если "add_contact_id" уже есть у "contact_owner_id"(табл.Contacts) => return
                if ([True for i in owner_id.all() if i[0] == contact_owner_id] and
                        [True for i in client_id.all() if i[0] == add_contact_id]):
                    return
                contacts = self.Contacts(owner_id=contact_owner_id, client_id=add_contact_id)

                self.session.add(contacts)
                self.session.commit()

    def del_contact(self, owner, del_contact):
        """
        :param owner:
        :param del_contact:
        :return:
        """
        for id_ in self.session.query(self.Client.id).filter_by(login=owner):
            contact_owner_id = id_[0]  # находим id по имени owner (табл.Client)
            for id__ in self.session.query(self.Client.id).filter_by(login=del_contact):
                del_contact_id = id__[0]  # находим id по имени add_contact (табл.Client)
                owner_id_ = self.session.query(self.Contacts.owner_id)
                client_id_ = self.session.query(self.Contacts.client_id)
                # если "add_contact_id" уже есть у "contact_owner_id"(табл.Contacts) => del
                if ([True for i in owner_id_.all() if i[0] == contact_owner_id] and [True for i in client_id_.all() if
                                                                                     i[0] == del_contact_id]):
                    self.session.query(self.Contacts).filter(self.Contacts.owner_id == contact_owner_id,
                                                             self.Contacts.client_id == del_contact_id).delete()
                    self.session.commit()
                return

    def get_users(self):
        return [user[0] for user in self.session.query(self.Client.login).all()]


client = ServerBase()
#
#a = client.get_users()
# print(a)
# client.del_contact("ko", "pa")
# b = client.get_contacts("ko")
# print(b)

# print(client.__dict__)
# client.save_log('koss1', 'dakope@tut.by1')
# client.save_log(login='koss', info='dakope@tut.by')


# for item in session.query(Client):
#     print(item.login, ' ', item.info)
