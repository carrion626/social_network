import requests
import random
from faker import Faker
import yaml


fake = Faker()
MAIN_URL = 'http://127.0.0.1:8000/api/'


with open('bot_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)


def new_user():
    endpoint = 'register/'
    new_user_data = {
        "username": fake.profile(fields=['username'])['username'],
        "password": fake.password()
    }
    response = requests.post(MAIN_URL + endpoint, data=new_user_data)
    if response.status_code == 201:
        return new_user_data


def login_user(credentials):
    response = requests.post(MAIN_URL, data=credentials)
    return response.json()['tokens']['access']


def generate_post(token):
    endpoint = 'create/'
    header = {"Authorization": f"Bearer {token}"}
    max_posts_per_user = config.get('max_posts_per_user')
    for i in range(random.randint(1, max_posts_per_user)):
        random_post = {"user": "1", "content": fake.paragraph(nb_sentences=10)}
        response = requests.post(MAIN_URL + endpoint, data=random_post, headers=header)
        print(response.json()['id'])


def like_post(max_likes_per_user, post_id, token):
    header = {"Authorization": f"Bearer {token}"}
    response = requests.get(f'{MAIN_URL}posts/', headers=header)
    for i in range(random.randint(1, max_likes_per_user)):
        post_id = random.randint(0, len(response.json()) - 1)
        requests.post(f'{MAIN_URL}posts/{post_id}/like/', headers=header)
        print(f"User liked post {post_id}")


def main():
    number_of_users = config.get('number_of_users')
    for i in range(number_of_users):
        credentials = new_user()
        token = login_user(credentials)
        post_id = generate_post(token=token)

        max_likes_per_user = config.get('max_likes_per_user')

        like_post(post_id=post_id, token=token, max_likes_per_user=max_likes_per_user)


main()



