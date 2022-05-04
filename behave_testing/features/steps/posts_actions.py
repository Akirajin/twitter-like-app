from behave import *
import requests, json
from py2neo import *


@when("post creation api is called with the following username {username} and the following message")
@given("post creation api is called with the following username {username} and the following message")
def step_impl(context, username):
    context.response = requests.post(f"http://localhost:9000/users/{username}/posts", json=json.loads(context.text))


@then('the database should have {message_qty:d} message with the following message from username {username}')
def step_impl(context, message_qty, username):
    g = Graph()
    assert g.nodes.match('post', username=username).count() == message_qty


@given("post creation api is called with username {username} and the message {message} passing the reference of {friend} last message")
def step_impl(context, username, message, friend):
    g = Graph()
    post = g.nodes.match('post', username = friend).first()
    request = {"message": message, "ref":  post.identity}
    context.response = requests.post(f"http://localhost:9000/users/{username}/posts", json=request)
