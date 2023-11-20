import logging
from flask import Flask, request, render_template, jsonify, send_file, make_response, after_this_request

from posts import posts_blueprint
from api import api_blueprint

app = Flask(__name__)

app.register_blueprint(posts_blueprint.posts_blueprint)
app.register_blueprint(api_blueprint.api_blueprint)

logging.basicConfig(level=logging.DEBUG, filename='logs/api.log')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Ошибка 404')
    return '<h1>Страница не найдена</h1>', 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Ошибка 500')
    return '<h1>Ошибка на стороне сервера</h1>', 500


if __name__ == '__main__':
    app.run(port=9000, host='0.0.0.0')

# ВЫЛОЖИТЬ НА РЕПОЗИТОРИЙ
# ШАГ 2 в задании со звездочкой
