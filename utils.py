import random
import json

from loader import sessionStorage


def get_random_word(user_id):
    with open('data/words.json', 'r', encoding='utf-8') as f:
        words = list(json.load(f))

    while True:
        random_word = random.choice(words)
        if random_word not in sessionStorage[user_id]['used_words']:
            return random_word


def get_trasnlate(word):
    with open('data/words.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data[word]


def get_random_phrases(word, name):
    phrases = [
        f'{name}! Ты просто супер! Следующее слово {word}',
        f'Молодец! Идем дальше: {word}',
        f'Отлично! Следующее слово {word}',
        f'А ты умный, {name}! Теперь это - {word}',
        f'Правильно! Что насчет {word}?'
    ]
    return random.choice(phrases)


def get_best_users(tail=10):
    with open('data/rating.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    best = sorted(data, key=lambda x: x['rating'], reverse=True)[:tail]

    text = ''

    count = 1
    for user in best:
        text += f'{count}. {user["user"]} - {user["rating"]}\n'
        count += 1

    return text


def create_user_rating_if_not_exist(name):
    with open('data/rating.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if name not in [user['user'] for user in data]:
        data.append({'user': name, 'rating': 0})

    with open('data/rating.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def get_user_rating(name):
    with open('data/rating.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for user in data:
        if user['user'] == name:
            return user['rating']


def update_user_rating(name, local_rating):
    with open('data/rating.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_rating = get_user_rating(name)

    if local_rating > user_rating:
        for user in data:
            if user['user'] == name:
                user['rating'] = local_rating

    with open('data/rating.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
