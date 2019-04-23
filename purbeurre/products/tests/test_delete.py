from django.test import Client

import pytest
from .pytest_fixture import createTwoProducts, createUser
from .test_save import test_save_post_ok_substitute

from products.models import Substitute

client = Client()
pytestmark = pytest.mark.django_db


def test_delete_user_not_logged(test_save_post_ok_substitute):
    """Test if user not logged in redirect to login page"""
    response = client.get('/products/delete/1')
    assert response.status_code == 302
    assert '/login/' in response.url


def test_delete_get(test_save_post_ok_substitute):
    client.login(username='test@test.com', password="12345")
    response = client.get('/products/delete/1')
    message = "Vous êtes sur le point de supprimer ce substitut ?".encode()
    assert response.status_code == 200
    assert message in response.content


def test_delete_post(test_save_post_ok_substitute):
    client.login(username='test@test.com', password="12345")
    assert Substitute.objects.all().count() == 1
    response = client.post('/products/delete/1')
    assert Substitute.objects.all().count() == 0
    assert response.status_code == 302
    assert '/myproducts/' in response.url


def test_delete_false_id(test_save_post_ok_substitute):
    client.login(username='test@test.com', password="12345")
    assert Substitute.objects.all().count() == 1
    response = client.post('/products/delete/2')
    assert response.status_code == 404
    assert Substitute.objects.all().count() == 1
