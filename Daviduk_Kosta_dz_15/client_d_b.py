from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import sqlite3


class ClientBase:
    '''
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется декларативный стиль.
    '''
    Base = declarative_base()

    class Message(Base):
        '''
        Класс - отображение для таблицы статистики переданных сообщений.
        '''
        __tablename__ = 'message'
        id = Column(Integer, primary_key=True)
        contact = Column(String)
        direction = Column(String)
        message = Column(String)
        data = Column(DateTime)

        def __init__(self, contact, direction, message):
            self.contact = contact
            self.direction = direction
            self.message = message
            self.data = datetime.datetime.now()

        def __repr__(self):
            return f'<Message({self.contact}, {self.direction}, {self.message}, {self.data})>'

    def __init__(self):
        self.engine = create_engine('sqlite:///client.db3', echo=False, pool_recycle=7200,
                                    connect_args={"check_same_thread": False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.commit()

    def save_message(self, contact, direction, message):
        '''Метод сохраняющий сообщение в базе данных.'''
        message = self.Message(contact, direction, message)
        self.session.add(message)
        self.session.commit()

    def get_history(self, contact):
        '''Метод возвращающий историю сообщений с определённым пользователем.'''
        query = self.session.query(self.Message).filter_by(contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.data) for history_row in query.all()]

#
# client = ClientBase()
# history_list = sorted(client.get_history('ko'), key=lambda item: item[3])
# print(history_list)

# a = client.save_message("ko", "pa", 'Hello my friend')
# b = client.save_message("pa", "ko", 'Hello, how are you?')
# с = client.see_messages("ko", "pa")
# for i in с:
#     print(i)
# print(client.see_messages("pa", "ko"))
# (('ko', 'pa', '2022-12-17 16:11:18.678346', 'Hello my friend'),
# ('pa', 'ko', '2022-12-17 16:11:18.688312', 'Hello, how are you?'))
# (('ko', 'pa', '2022-12-17 16:32:42.593164', 'my name is "ko"'),
# ('pa', 'ko', '2022-12-17 16:32:42.603421', 'my name is "pa"'))
# [(('pa', 'ko', '2022-12-17 16:11:18.688312', 'Hello, how are you?'),
# ('ko', 'pa', '2022-12-17 16:11:18.678346', 'Hello my friend')),
# (('pa', 'ko', '2022-12-17 16:32:42.603421', 'my name is "pa"'),
# ('ko', 'pa', '2022-12-17 16:32:42.593164', 'my name is "ko"'))]
