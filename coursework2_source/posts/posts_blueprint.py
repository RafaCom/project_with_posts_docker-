import logging
import cgi

from flask import Blueprint, render_template, request, redirect

from utils import PostsDAO

posts_blueprint = Blueprint('posts_blueprint', __name__)

PATH_POSTS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/posts.json'
PATH_COMMENTS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/comments.json'
PATH_BOOKMARKS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/bookmarks' \
                 '.json'

posts = PostsDAO(PATH_POSTS, PATH_COMMENTS, PATH_BOOKMARKS)

logging.basicConfig(level=logging.DEBUG, filename='logs/api.log')


@posts_blueprint.route('/', methods=['GET', 'POST'])
def index_page():
    logging.info('Запрошена главная страница')
    all_posts = posts.get_posts_all()
    all_bookmarks = posts.load_data_bookmarks()
    return render_template('index.html', all_posts=all_posts, sum_posts=len(all_posts), sum_bookmarks=len(all_bookmarks))


@posts_blueprint.route('/posts/<int:post_id>')
def post_page(post_id):
    logging.info(f'Запрошена страница с постом номер - {post_id}')
    post = posts.get_post_by_pk(post_id)
    post_new_text = posts.hashtags_search(post['content'])
    # print(post_new_text)
    comments = posts.get_comments_by_post_id(post_id)
    return render_template('post.html', post=post, comments=comments, sum_comments=len(comments), text=post_new_text)


@posts_blueprint.route('/search')
def search_page():
    s = request.args['s']
    logging.info(f'Запрошена страница поиска по слову: {s}')
    post_list = posts.search_for_posts(s)
    return render_template('search.html', post_list=post_list, sum_posts=len(post_list), s=s)


@posts_blueprint.route('/users/<username>')
def user_page(username):
    logging.info(f'Запрошена страница пользователя {username}')
    posts_by_user = posts.get_posts_by_user(username)
    for post in posts_by_user:
        hashtags = posts.hashtags_search(post['content'])
    return render_template('user-feed.html', posts_by_user=posts_by_user, username=username, hashtags=hashtags)


@posts_blueprint.route('/tag/<tag_name>')
def page_with_tag(tag_name):
    logging.info(f'Запрошена страница c тегом: {tag_name}')
    posts_with_tag = posts.search_for_posts_with_tags(tag_name)
    return render_template('tag.html', posts_with_tag=posts_with_tag, tag_name=tag_name)


@posts_blueprint.route('/bookmarks/add/<int:post_id>')
def add_in_bookmarks(post_id):
    posts.add_in_json_bookmarks(post_id)
    return redirect('/', code=302)


@posts_blueprint.route('/bookmarks/remove/<int:post_id>')
def del_in_bookmarks(post_id):
    posts.del_from_json_bookmarks(post_id)
    return redirect('/', code=302)


@posts_blueprint.route('/bookmarks')
def bookmarks_page():
    all_bookmarks = posts.load_data_bookmarks()
    return render_template('bookmarks.html', all_bookmarks=all_bookmarks)

