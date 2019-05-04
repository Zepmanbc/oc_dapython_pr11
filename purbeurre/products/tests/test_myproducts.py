from django.test import Client
from django.urls import reverse

import pytest
from .pytest_fixture import createTwoProducts, createUser, createSubstitutes, loadProducts

from products.models import Product, Substitute
from authentication.models import User

client = Client()
pytestmark = pytest.mark.django_db


def test_myproducts_not_logged():
    response = client.get(reverse('products:myproducts'))
    assert response.status_code == 302


def test_myproducts_show_list(createUser, createTwoProducts):
    client.login(username='test@test.com', password="12345")

    p1 = Product.objects.get(pk=1)
    p2 = Product.objects.get(pk=2)
    u = User.objects.get(pk=1)
    Substitute.objects.create(product_id=p1, substitute_id=p2, user_id=u)

    response = client.get(reverse('products:myproducts'))
    assert response.status_code == 200
    message = "Il n'y a pas de produits enregistrés".encode()
    assert message not in response.content


def test_myproducts_show_empty(createUser, createTwoProducts):
    client.login(username='test@test.com', password="12345")

    response = client.get(reverse('products:myproducts'))
    assert response.status_code == 200
    message = "Il n'y a pas de produits enregistrés".encode()
    assert message in response.content


def test_myproducts_pages(createUser, createTwoProducts):
    client.login(username='test@test.com', password="12345")
    response = client.get(reverse('products:myproducts') + '?page=1')
    assert response.status_code == 200
    response = client.get(reverse('products:myproducts') + '?page=2')
    assert response.status_code == 404


def test_myproducts_pagination(loadProducts, createUser, createSubstitutes):
    client.login(username='test@test.com', password="12345")
    response = client.get(reverse('products:myproducts') + '?page=2')
    good_link = '<a href="?page=1">Précédente</a>'
    assert good_link in response.rendered_content
