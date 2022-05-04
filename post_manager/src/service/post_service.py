import calendar

from py2neo import *
import requests
from datetime import datetime
from src.exceptions.user_define_execptions import UserNotFound, MessageTooLong, DailyPostLimitReached


class PostService:
    def __init__(self):
        self.graph = Graph()

    def create_post(self, username, message, ref=None):
        self.check_message_length(message)
        self.check_if_user_has_more_than_five_messages_today(username)
        node = self.get_user_from_database(username)
        self.graph.create(Node('post', username=node['username'], message=message, date=datetime.now(), ref=ref))

    def check_message_length(self, message):
        if len(message) > 777:
            raise MessageTooLong

    def get_user_from_database(self, username):
        node = self.graph.nodes.match('user', username=username).first()
        if node is None:
            raise UserNotFound
        return node

    def check_if_user_has_more_than_five_messages_today(self, username):
        today = datetime.now().date()
        dates = [i['date'].date() for i in self.graph.nodes.match('post', username=username).all()]
        if dates.count(today) >= 5:
            raise DailyPostLimitReached

    def get_posts(self, username):
        node = self.get_user_from_database(username)
        following = [i.end_node['username'] for i in
                     self.graph.relationships.match((node, None), r_type='follows').all()]

        messages = []
        for i in self.graph.nodes.match('post', username=(username, *following)).all():
            message = self.convert_node_post_to_response_post(i)
            messages.append(message)
        return messages

    def convert_node_post_to_response_post(self, i):
        message = {'id': i.identity, 'username': i['username'], 'message': i['message'],
                   'date': self.format_datetime(i['date'])}
        if i['ref'] is not None and int(i['ref']) >= 0:
            message['repost'] = self.get_post_by_id(i['ref'])
        return message

    def get_post_by_id(self, ref):
        post = self.graph.nodes.get(int(ref))
        return self.convert_node_post_to_response_post(post)

    def format_datetime(self, raw_datetime):
        hour, minute, sec = raw_datetime.hour_minute_second
        year, month, day = raw_datetime.year_month_day
        return f'{hour}:{minute} - {calendar.month_name[month]} {day}, {year}'
