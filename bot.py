__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "25.03.2018"
__app__ = "rest_bot"
__status__ = "Development"

import json
import random
import time
from functools import partial

import click
import requests
from faker import Faker
from termcolor import cprint

faker_factory = Faker("uk_UA")

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
with open('test_data.json') as json_data_file:
    test_data = json.load(json_data_file)

api_url = config.get("api_url_address")


@click.group()
def cli():
    pass


@click.command()
@click.option('--number_of_users', default=None, help='Number of test Users to create.')
@click.option('--max_posts_per_user', default=None, help='Max number of post created by users.')
@click.option('--max_likes_per_user', default=None, help='Max number of post created by users.')
def create_activity(number_of_users, max_posts_per_user, max_likes_per_user):
    if number_of_users:
        config['number_of_users'] = number_of_users
    if max_posts_per_user:
        config['max_posts_per_user'] = max_posts_per_user
    if max_likes_per_user:
        config['max_likes_per_user'] = max_likes_per_user

    users_list = []
    users_dict_tokens = {}
    posts_list = []

    # Step 1: Creating accounts
    cprint('Step 1: Creating accounts.\n', 'blue')
    time.sleep(2)
    if config.get('only_deliverable_emails'):
        cprint('Email hunter checking is enabled, use only deliverable email addresses.', 'magenta')
        deliverable_emails = test_data.get('deliverable_emails')
        if config.get('number_of_users') > len(deliverable_emails):
            emails = deliverable_emails
            cprint(
                'Number of users provided in config is greater than available '
                'test emails in data-set (file test_data.json).',
                'magenta')
            cprint('Variable "number_of_users" changed to {}'.format(len(deliverable_emails)), 'magenta')
        else:
            number_of_users_to_create = config.get('number_of_users')
            emails = deliverable_emails[0:number_of_users_to_create - 1]
    else:
        emails = []
        for _ in range(config.get('number_of_users')):
            emails.append(faker_factory.email())
        pass
    for email in emails:
        fake_profile = faker_factory.simple_profile()
        fake_username = fake_profile.get('username')
        fake_name = fake_profile.get('name')
        name_list = fake_name.strip().split(' ')

        fake_first_name = fake_name
        fake_last_name = ""
        if len(name_list) == 2:
            fake_first_name = name_list[0]
            fake_last_name = name_list[1]
        parameters = {
            'username': fake_username,
            'password': config.get('default_password'),
            'email': email,
            'email2': email,
            'first_name': fake_first_name,
            'last_name': fake_last_name
        }
        time.sleep(0.2)
        response = requests.post(url=api_url + '/api/users/', data=parameters)
        if response.status_code == 201:
            cprint(
                'Account successfully created.\n Email: {}; Username {}; First Name:{}; Last Name: {};'.format(
                    email, fake_username, fake_first_name, fake_last_name), 'green')
            print(response)
            print(response.text + "\n")
            users_list.append(fake_username)
        else:
            cprint('Failed to create account.\n Email:{}; Username {}; First Name:{}; Last Name: {};'.format(
                email, fake_username, fake_first_name, fake_last_name), 'red')
            print(response)
            print(response.text + "\n")
        pass

    # Step 2: Auth users
    cprint('Step 2: Auth users.\n', 'blue')
    time.sleep(4)
    for username in users_list:
        parameters = {
            'username': username,
            'password': config.get('default_password')
        }
        response = requests.post(url=api_url + '/api/auth/', data=parameters)
        if response.status_code == 200:
            cprint('User: {} successfully authenticated.'.format(username), 'green')
            print(response)
            print(response.text + '\n')
            resp_json = response.json()
            if resp_json.get('token'):
                token = resp_json.get('token')
                users_dict_tokens[username] = token
        else:
            cprint('Failed to  authenticate user: {}'.format(username), 'red')
            print(response)
            print(response.text + '\n')

    # Step 3: Create posts.
    cprint('Step 3: Create posts.', 'blue')
    cprint('{} accounts are available for creating fake activity.\n'.format(len(users_dict_tokens)), 'magenta')
    time.sleep(4)
    for user, token in users_dict_tokens.items():
        random_num_of_posts = random.randint(1, config.get('max_posts_per_user'))
        for i in range(random_num_of_posts):
            headers = {'Authorization': 'Bearer {}'.format(token)}
            parameters = {
                'title': faker_factory.sentence(),
                'content': faker_factory.text()
            }
            response = requests.post(url=api_url + '/api/posts/', data=parameters, headers=headers)
            if response.status_code == 201:
                resp_json = response.json()
                post_id = resp_json.get('id')
                if post_id:
                    posts_list.append(post_id)
                title = resp_json.get('title')
                cprint('User {} has crated post with id:{} and title: {}. \n'.format(user, post_id, title), 'green')

    # Step 4: Create like activity.
    cprint('Step 4:  Create like activity.', 'blue')
    cprint('{} accounts and {} posts are available for creating fake like activity.\n'
           .format(len(users_dict_tokens), len(posts_list)), 'magenta')
    time.sleep(0.1)
    posts_liked = 0
    if config.get('max_likes_per_user') > len(posts_list):
        get_rand_num_of_likes = partial(random.randint, 0, len(posts_list))
    else:
        get_rand_num_of_likes = partial(random.randint, 0, config.get('max_likes_per_user'))
    for user, token in users_dict_tokens.items():
        time.sleep(0.05)
        posts_list_copy = posts_list.copy()
        num_of_posts_to_like = get_rand_num_of_likes()
        for _ in range(num_of_posts_to_like):
            post_id = random.choice(posts_list_copy)
            posts_list_copy.remove(post_id)
            headers = {'Authorization': 'Bearer {}'.format(token)}
            response = requests.post(url=api_url + '/api/posts/{}/likes/'.format(post_id), headers=headers)
            if response.status_code == 201:
                posts_liked += 1
                cprint('User {} liked post with id:{}\n'.format(user, post_id), 'green')

    cprint(
        '{} users liked in general {} posts and liked posts {} times .'.format(len(users_list), len(posts_list), posts_liked),
        'magenta')
    cprint('Bot finished all activity tasks.', 'green')
    cprint('Please visit this page to view results {}/posts/'.format(api_url), 'magenta')
    cprint('Credentials:\nUsername:{}\nPassword:{}'.format(random.choice(users_list), config.get('default_password')),
           'magenta')


cli.add_command(create_activity)

if __name__ == '__main__':
    cli()
