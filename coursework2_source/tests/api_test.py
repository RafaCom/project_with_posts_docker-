import pytest
from flask import Flask

from app import app


def test_endpoint_posts():
    client = app.test_client()

    response = client.get('/api/posts')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list), 'Возвращается не список'
    assert data[0]['pk'] == 1, 'Нет ключей у элементов'


def test_endpoint_one_post():
    client = app.test_client()

    response = client.get('/api/posts/1')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict), 'Возвращается не список'
    assert data['pk'] == 1, 'Нет ключей у элементов'
