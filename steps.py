from loader import sessionStorage
import utils


def new_dialog(request, response):
    user_id = request['session']['user_id']

    if request['session']['new']:
        sessionStorage[user_id] = {}
        response['response']['text'] = 'Привет! Это навык для проверки твоей грамотности. ' \
                                       'Тебе будут предложены слова на английском, ' \
                                       'твоя задача их перевести на русский. Начнем?'

        response['response']['buttons'] = [
            {
                'title': 'Да',
                'hide': True
            },
            {
                'title': 'Нет',
                'hide': True
            }
        ]
        sessionStorage[user_id]['step'] = 'ready'
        return True


def ready_check(request, response):
    user_id = request['session']['user_id']

    if request['request']['original_utterance'].lower() in [
        'да',
        'поехали',
        'готов',
        'давай',
        "го"
    ] and sessionStorage[user_id]['step'] == 'ready':
        response['response']['text'] = 'Как тебя зовут?'
        sessionStorage[user_id]['step'] = 'name'
        return True

    elif request['request']['original_utterance'].lower() in [
        'нет',
        'не хочу',
        'неа'
    ] and sessionStorage[user_id]['step'] == 'ready':
        response['response']['text'] = 'Ну ладно, если что, возвращайся!'
        response['response']['end_session'] = True

        return True

    elif sessionStorage[user_id]['step'] == 'ready':
        response['response']['text'] = 'Прости, не понимаю тебя'

        return True


def get_name(request, response):
    user_id = request['session']['user_id']

    if sessionStorage[user_id]['step'] == 'name':
        name = request['request']['original_utterance']
        sessionStorage[user_id]['used_words'] = []

        random_word = utils.get_random_word(user_id)

        sessionStorage[user_id]['used_words'].append(random_word)

        sessionStorage[user_id]['name'] = name
        sessionStorage[user_id]['step'] = 'game'
        sessionStorage[user_id]['curent_word'] = random_word

        response['response']['buttons'] = [
            {
                'title': "Рейтинг",
                'hide': True
            }
        ]

        utils.create_user_rating_if_not_exist(sessionStorage[user_id]['name'])
        sessionStorage[user_id]['local_rating'] = 0

        response['response']['text'] = f'Приятно познакомиться, {name}. Первое слово {random_word}'
        return True


def rating(request, response):
    user_id = request['session']['user_id']
    name = sessionStorage[user_id]['name']

    answer = request['request']['original_utterance'].lower()
    local_rating = sessionStorage[user_id]['local_rating']
    curent_word = sessionStorage[user_id]['curent_word']

    if answer == 'рейтинг':
        text = (f'Лучшие игроки\n\n'
                f'{utils.get_best_users()} \n\n'
                f'Ваш лучший результат: {utils.get_user_rating(name)} \n\n'
                f'Ваш текущий рейтинг: {local_rating} \n\n\n'
                f'Напоминаю, текущее слово: {curent_word}')
        response['response']['text'] = text

        return True


def game(request, response):
    user_id = request['session']['user_id']

    if sessionStorage[user_id]['step'] == 'game':
        answer = request['request']['original_utterance'].lower()
        word = sessionStorage[user_id]['curent_word']
        translate = utils.get_trasnlate(word)

        if translate == answer:
            sessionStorage[user_id]['local_rating'] += 1

            utils.update_user_rating(sessionStorage[user_id]['name'], sessionStorage[user_id]['local_rating'])

            random_word = utils.get_random_word(user_id)

            sessionStorage[user_id]['curent_word'] = random_word
            sessionStorage[user_id]['used_words'].append(random_word)
            name = sessionStorage[user_id]['name']
            response['response']['text'] = utils.get_random_phrases(random_word, name)

            response['response']['buttons'] = [
                {
                    'title': "Рейтинг",
                    'hide': True
                }
            ]

        else:
            response['response']['text'] = f'Неправильно, повтори попытку'
        return True
