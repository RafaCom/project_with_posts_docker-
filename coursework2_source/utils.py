import json
import re


class PostsDAO:
    def __init__(self, path_posts, path_comments, path_bookmarks):
        if type(path_posts) not in [str]:
            raise TypeError('Путь должен быть строкой')

        try:
            open(path_posts)
            open(path_comments)
            open(path_bookmarks)
        except FileNotFoundError as e:
            raise e

        self.path_posts = path_posts
        self.path_comments = path_comments
        self.path_bookmarks = path_bookmarks

    def load_data_posts(self):
        with open(self.path_posts, 'r', encoding='utf-8') as f:
            data_posts = json.load(f)
            return data_posts

    def load_data_comments(self):
        with open(self.path_comments, 'r', encoding='utf-8') as f:
            data_comments = json.load(f)
            return data_comments

    def load_data_bookmarks(self):
        with open(self.path_bookmarks, "r", encoding='utf-8') as f:
            bookmarks = json.load(f)
            return bookmarks

    def get_posts_all(self):
        return self.load_data_posts()

    def get_posts_by_user(self, user_name):
        list_posts_user = []
        for post_ in self.load_data_posts():
            if user_name.lower() == post_['poster_name'].lower():
                try:
                    if post_['pk']:
                        list_posts_user.append(post_)
                except KeyError:
                    return []
        if list_posts_user:
            return list_posts_user
        raise ValueError("Такого пользователя нет")

    def get_comments_by_post_id(self, post_id):
        list_comments_id = []
        list_posts_id = []
        for post_ in self.load_data_posts():
            try:
                if post_id == post_['pk']:
                    list_posts_id.append(post_)
            except KeyError:
                continue
        if list_posts_id:
            for comment in self.load_data_comments():
                for p in list_posts_id:
                    if comment['post_id'] == p['pk']:
                        list_comments_id.append(comment)
            return list_comments_id
        raise ValueError("Такого поста нет")

    def search_for_posts(self, query):
        posts_by_word = []
        for p in self.load_data_posts():
            try:
                if query.lower() in p['content'].lower():
                    posts_by_word.append(p)
            except KeyError:
                continue
        return posts_by_word

    def get_post_by_pk(self, pk):
        for p in self.load_data_posts():
            try:
                if pk == p['pk']:
                    return p
            except KeyError:
                continue

    def search_for_posts_with_tags(self, tag):
        posts_by_tag = []
        for p in self.load_data_posts():
            try:
                hashtags = re.findall(r'\#\w+', p['content'].lower())  # Ищем все слова, начинающиеся с '#'
                if '#' + tag in hashtags:
                    posts_by_tag.append(p)
            except KeyError:
                continue
        return posts_by_tag

    @staticmethod
    def hashtags_search(text):
        hashtags = re.findall(r'\#\w+', text.lower())
        new_text = [text]
        list_with_tags = new_text[-1].split()
        for tag in hashtags:
            # new = new_text[-1].replace(tag, f'<a href="/tag/{ tag[1:] }">{ tag }</a>')
            index = list_with_tags.index(tag)
            list_with_tags.pop(index)
            list_with_tags.insert(index, f'<a href="/tag/{tag[1:]}">{tag}</a>')
            new_str = ' '.join(list_with_tags)
            new_text.append(new_str)
        return new_text[-1]

    def add_in_json_bookmarks(self, post_id):
        bookmarks = self.load_data_bookmarks()
        post = self.get_post_by_pk(post_id)
        # for post_ in bookmarks:
        if post_id not in [post_['pk'] for post_ in bookmarks]:
            bookmarks.insert(0, post)
            with open('data/bookmarks.json', 'w') as file:
                json.dump(bookmarks, file, indent=4, ensure_ascii=False)

    def del_from_json_bookmarks(self, post_id):
        bookmarks = self.load_data_bookmarks()
        for post in bookmarks:
            if post_id == post['pk']:
                new_data = [p for p in bookmarks if p != post]
        with open('data/bookmarks.json', 'w') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)


# posts = PostsDAO('data/posts.json', 'data/comments.json', 'data/bookmarks.json')
# posts.add_in_json_bookmarks(3)
# posts.del_from_json_bookmarks(2)
# all_posts = posts.get_posts_all()
# all_posts_with_tags = []
# for post in all_posts:
#     all_posts_with_tags.append(posts.hashtags_search(post['content']))
# print(all_posts_with_tags)
# print(post.get_posts_by_user("leo"))
# print(get_comments_by_post_id(2))
# print(post.search_for_posts_with_tags('пирог'))
# print(get_post_by_pk(8))
# print(post.search_for_posts('у'))


# clean_text = re.sub(r"\W", " ", p['content'].lower())
#                 if query.lower() in clean_text.split():
#
# Усложненный вариант поиска по слову
