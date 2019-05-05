from django.test import Client
from django.urls import reverse

import pytest

client = Client()
pytestmark = pytest.mark.django_db


def test_index_page_name():
    # index return 200 with index name
    response = client.get(reverse('index')).status_code
    assert response == 200


def test_index_page_url():
    # index return 200 with index url
    response = client.get('/').status_code
    assert response == 200


def test_legal_page_name():
    # legal return 200 with legal name
    response = client.get(reverse('legal')).status_code
    assert response == 200


def test_legal_page_url():
    # legal return 200 with legal url
    response = client.get('/legal').status_code
    assert response == 200


def test_fake_page_url():
    # index return 404
    response = client.get('/zzNotExistPaGe').status_code
    assert response == 404


def test_delete_keep_substitute_session():
    """test if session variable 'keep_substitute' is deleted (Issue #2)"""
    client.get(reverse('index'))

    session = client.session
    session['keep_substitute'] = ('1', '2')
    session.save()
    assert client.session['keep_substitute']
    client.get(reverse('index'))
    with pytest.raises(KeyError):
        client.session['keep_substitute']
