import calendar
from datetime import datetime

from py2neo import Graph, Node, Relationship

from src.api.requests.user_request import UserRequest
from src.exceptions.user_define_execptions import NonAlphanumericError, UserNameTooLongError, UserNameAlreadyTaken, \
    UserNotFound, FollowingHimselfError


class UserService:
    def __init__(self):
        self.graph = Graph()

    def create_user(self, user: UserRequest):
        self.check_if_username_is_aphanumeric(user)
        self.check_if_length_is_lt_15(user)
        self.check_if_username_is_already_taken(user)

        node = Node('user', username=user.username, joined_date=datetime.now())
        self.graph.create(node)

    def check_if_username_is_already_taken(self, user):
        if self.graph.nodes.match('user', username=user.username).count() > 0:
            raise UserNameAlreadyTaken

    def check_if_length_is_lt_15(self, user):
        if len(user.username) > 14:
            raise UserNameTooLongError

    def check_if_username_is_aphanumeric(self, user):
        if not user.username.isalnum():
            raise NonAlphanumericError

    def find_user(self, username):
        node = self.get_user_from_database(username)
        response = dict(node)
        following = self.graph.relationships.match((node, None), r_type='follows').all()
        followers = self.graph.relationships.match((None, node), r_type='follows').all()
        posts = self.graph.nodes.match('post', username=username).count()
        response['following'] = len(following)
        response['followers'] = len(followers)
        response['posts'] = posts
        year, month, day = response['joined_date'].year_month_day
        response['joined_date'] = f'{calendar.month_name[month]} {day}, {year}'

        return response

    def list_follows(self, username):
        node = self.get_user_from_database(username)
        following = self.graph.relationships.match((node, None), r_type='follows').all()
        followers = self.graph.relationships.match((None, node), r_type='follows').all()
        response = {'following': [i.end_node['username'] for i in following],
                    'followers': [i.start_node['username'] for i in followers]}

        return response

    def get_user_from_database(self, username):
        node = self.graph.nodes.match('user', username=username).first()
        if node is None:
            raise UserNotFound
        return node

    def user_follows(self, own_username, friend_username):
        if own_username == friend_username:
            raise FollowingHimselfError
        own = self.get_user_from_database(own_username)
        friend = self.get_user_from_database(friend_username)
        if own is None or friend is None:
            raise UserNotFound
        self.graph.create(Relationship(own, 'follows', friend))

    def user_unfollows(self, own_username, friend_username):
        own = self.get_user_from_database(own_username)
        friend = self.get_user_from_database(friend_username)
        relation = self.graph.relationships.match((own, friend), r_type='follows').first()
        tx = self.graph.begin()
        tx.separate(relation)
        tx.commit()
