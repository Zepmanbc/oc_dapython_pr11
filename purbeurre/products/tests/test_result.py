from django.test import Client

import pytest

from products.models import Product

client = Client()
pytestmark = pytest.mark.django_db

from .pytest_fixture import createTwoProducts


def test_search_good_id_return_something(createTwoProducts):
    """
    Produit 1 : nutrition grade c 
    Produit 2 : nutrition grade b
    Produit 2 > c : return Produit 2
    """
    response = client.get('/products/1/result/')
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 1


def test_search_good_id_return_nothing(createTwoProducts):
    """
    Produit 1 : nutrition grade c
    Produit 2 : nutrition grade b
    Produit 1 < b : return nothing
    """
    response = client.get('/products/2/result/')
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 0


def test_search_false_id(createTwoProducts):
    with pytest.raises(Product.DoesNotExist):
        client.get('/products/3/result/')


def test_allreadysaved_message(createTwoProducts):
    response = client.get('/products/1/result/')
    assert 'message' not in response.context_data
    response = client.get('/products/1/result/?allreadysaved')
    assert response.status_code == 200
    assert 'message' in response.context_data
