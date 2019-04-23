from django.test import Client
from django.urls import reverse

import pytest
from .pytest_fixture import createTwoProducts, createUser


client = Client()
pytestmark = pytest.mark.django_db


def test_detail_success(createTwoProducts):
    response = client.get('/products/1/detail/')
    assert response.status_code == 200
    response = client.get(reverse('products:detail', kwargs={'pk': 2}))
    assert response.status_code == 200


def test_detail_fail(createTwoProducts):
    response = client.get('/products/3/detail/')
    assert response.status_code == 404
    response = client.get(reverse('products:detail', kwargs={'pk': 4}))
    assert response.status_code == 404
