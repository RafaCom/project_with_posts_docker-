import json

import pytest

from utils import PostsDAO

PATH_POSTS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/posts.json'
PATH_COMMENTS = '/Users/rafaelsirinan/Desktop/Python Projects/project_with_posts/coursework2_source/data/comments.json'

with open(PATH_POSTS, 'r') as f:
    data_posts = json.load(f)

with open(PATH_COMMENTS, 'r') as f:
    data_comments = json.load(f)


class TestPosts:
    def test_load_data_posts(self):
        post = PostsDAO(PATH_POSTS, PATH_COMMENTS)
        assert post.load_data_posts() == data_posts, 'Ошибка в загрузке постов'

    def test_load_data_comments(self):
        post = PostsDAO(PATH_POSTS, PATH_COMMENTS)
        assert post.load_data_comments() == data_comments, 'Ошибка в загрузке комментариев'

    def test_get_posts_by_user(self):
        post = PostsDAO(PATH_POSTS, PATH_COMMENTS)
        assert post.get_posts_by_user('leo')[0]['poster_name'] == 'leo', 'Ошибка в описке постов по имени'

    def test_get_comments_by_post_id(self):
        post = PostsDAO(PATH_POSTS, PATH_COMMENTS)
        # for comment in data_comments:
        #     if comment['post_id'] == 1:
        assert post.get_comments_by_post_id(1)[0]['post_id'] == 1, 'Ошибка в поиске комментариев по id поста'

    def test_search_for_posts(self):
        post = PostsDAO(PATH_POSTS, PATH_COMMENTS)
        # for p in data_posts:
        #     if p['content'].split()[0] == 'утром':
        assert post.search_for_posts('утром')[0]['poster_name'] == 'larry'

    def test_get_post_by_pk(self):
        post = PostsDAO(PATH_POSTS, PATH_COMMENTS)
        # for p in data_posts:
        #     if p['pk'] == 3:
        assert post.get_post_by_pk(3)['pk'] == 3, 'Ошибка в поиске постов по id'

    def test_init_type_error(self):
        with pytest.raises(TypeError):
            post = PostsDAO(2, 3)

    def test_init_file_not_found_error(self):
        with pytest.raises(FileNotFoundError):
            post = PostsDAO('posts.json', 'comments.json')


""" Изучить тесты, понять насколько правильно выполняю их """
