from datetime import datetime
from deepdiff import DeepDiff
import requests, json
from behave import given, when, then
from py2neo import Graph, Node, Relationship


@given('we have a empty database')
def step_delete(context):
    g = Graph()
    g.delete_all()


@when('users creation api is called with the following username {username}')
def step_call(context, username):
    request = {'username': username}
    response = requests.post('http://localhost:8000/users', json=request)
    context.response = response


@then('the request will return httpStatus {http_status:d}')
def step_http_status(context, http_status):
    assert http_status == context.response.status_code, f'expected: {http_status}, current:{context.response.status_code}'


@then('the username {username} should appear {times:d} time(s) in the users base')
def step_check_database(context, username, times):
    g = Graph()
    assert g.nodes.match('user', username=username).count() == times


@then('the payload must return the following message {text}')
def step_http_status(context, text):
    current = context.response.json()['description']
    assert text == current, f"expected: {text}, current: {current}"


@given("there's user {username} in the database")
def step_username_already_there(context, username):
    g = Graph()
    g.create(Node('user', username=username, joined_date=datetime.now()))


@given('user {user_origin} is following username {user_dest}')
def step_create_following_number(context, user_origin, user_dest):
    g = Graph()
    origin = g.nodes.match('user', username=user_origin).first()
    dest = g.nodes.match('user', username=user_dest).first()
    g.create(Relationship(origin, 'follows', dest))


@when('the {path} is called using GET')
def step_calling_get(context, path):
    response = requests.get(path)
    context.response = response


@then("the payload will have the following json")
def step_compare_body(context):
    expected = json.loads(context.text)
    current = context.response.json()
    if 'joined_date' in expected.keys():
        expected['joined_date'] = current['joined_date']  # can't compare dates
    assert len(DeepDiff(expected, current, ignore_order=True)) == 0, f'expected: {expected}, current: {current}'


@then("the payload will have the following lists")
def step_compare_body(context):
    expected = json.loads(context.text)
    current = context.response.json()

    assert len(DeepDiff(expected, current, exclude_regex_paths=["\['id'\]", "\['date'\]"],
                        ignore_order=True)) == 0, f'expected: {expected}, current: {current}'


@when('the {path} is called using {verb} with payload')
def step_follow_someone(context, path, verb):
    if verb == 'POST':
        context.response = requests.post(path, json=json.loads(context.text))
    elif verb == 'DELETE':
        context.response = requests.delete(path, json=json.loads(context.text))
