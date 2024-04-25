# импортируем библиотеки
from flask import Flask, request, jsonify

import utils
from loader import sessionStorage, app

import steps

@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)

    return jsonify(response)


def handle_dialog(req, res):
    if steps.new_dialog(req, res):
        return

    if steps.ready_check(req, res):
        return

    if steps.get_name(req, res):
        return

    if steps.rating(req, res):
        return

    if steps.game(req, res):
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
