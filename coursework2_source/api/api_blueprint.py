import logging

from flask import Blueprint, render_template, request, send_file, jsonify

from utils import PostsDAO

api_blueprint = Blueprint('api_blueprint', __name__)

PATH_POSTS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/posts.json'
PATH_COMMENTS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/comments.json'
PATH_BOOKMARKS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/bookmarks' \
                 '.json'

posts = PostsDAO(PATH_POSTS, PATH_COMMENTS, PATH_BOOKMARKS)

logging.basicConfig(level=logging.DEBUG)


@api_blueprint.route('/api/posts', methods=['GET'])
def get_posts_json():
    logging.info('Запрошен api-эндпоинт всех постов')
    filename = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/posts.json'
    return send_file(filename, mimetype='application/json')


@api_blueprint.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post_by_id_json(post_id):
    logging.info('Запрошен api-эндпоинт поста по id')
    post = posts.get_post_by_pk(post_id)
    return jsonify(post)
