from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import sqlite3


class ClientBase:
    Base = declarative_base()

    class Message(Base):
        __tablename__ = 'message'
        id = Column(Integer, primary_key=True)
        sender = Column(String)
        recipient = Column(String)
        data = Column(DateTime)
        message = Column(String)

        def __init__(self, sender, recipient, data, message):
            self.sender = sender
            self.recipient = recipient
            self.data = data
            self.message = message

        def __repr__(self):
            return f'<Message({self.sender}, {self.recipient}, {self.data}, {self.message})>'

    def __init__(self):
        self.engine = create_engine('sqlite:///client.db3', echo=False, pool_recycle=7200,
                                    connect_args={"check_same_thread": False})
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.commit()

    def save_message(self, sender, recipient, message):
        """
        :param sender:
        :param recipient:
        :param message:
        :return: client.db3
        """
        message = self.Message(sender=sender, recipient=recipient, data=datetime.datetime.now(), message=message)
        self.session.add(message)
        self.session.commit()

    def see_messages(self, sender, recipient):
        """
        :param sender: отправитель
        :param recipient: получатель
        :return: переписка: отправил/принял
        [(('sender', 'recipient', 'data', 'message'), ('recipient', 'sender', 'data', 'message')),
        """
        list_message_sender = []
        list_message_recipient = []
        for message in self.session.query(self.Message).filter_by(sender=sender, recipient=recipient):
            list_message_sender.append((message.sender, message.recipient,
                                        str(datetime.datetime.strptime(str(message.data), '%Y-%m-%d %H:%M:%S.%f')),
                                        message.message))

        for message in self.session.query(self.Message).filter_by(sender=recipient, recipient=sender):
            list_message_recipient.append((message.sender, message.recipient,
                                           str(datetime.datetime.strptime(str(message.data), '%Y-%m-%d %H:%M:%S.%f')),
                                           message.message))

        zipped_values = zip(list_message_sender, list_message_recipient)
        zipped_list = list(zipped_values)

        return zipped_list


client = ClientBase()
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
