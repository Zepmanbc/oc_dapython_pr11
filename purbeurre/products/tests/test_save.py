from django.test import Client
from django.urls import reverse

import pytest
from .pytest_fixture import createTwoProducts, createUser

from products.models import Product, Substitute

client = Client()
pytestmark = pytest.mark.django_db


@pytest.fixture
def test_save_post_ok_substitute(createUser, createTwoProducts):
    """Test all good:
    user is connected
    product id and produc substitutes are ok
    POST request
    DB modification: new item in Substitute
    """
    client.login(username='test@test.com', password="12345")
    assert Substitute.objects.all().count() == 0
    response = client.post(
        '/products/save/',
        {
            'product_id': '1',
            'substitute_id': '2',
            'next': '/'
        }
    )
    assert Substitute.objects.all().count() == 1
    assert response.status_code == 302


def test_save_post_ok_allreadyexist(createUser, createTwoProducts, test_save_post_ok_substitute):
    """Test all good but allready saved.
    must return GET 'allreadysaved'

    previous: test_save_post_ok_substitute
    """
    response = client.post(
        '/products/save/',
        {
            'product_id': '1',
            'substitute_id': '2',
            'next': '/'
        }
    )
    assert Substitute.objects.all().count() == 1
    assert response.url == '/?allreadysaved'
    assert response.status_code == 302


def test_save_user_not_logged():
    """Test POST but user not logged in.
    no DB modification
    redirect to index
    """
    assert Substitute.objects.all().count() == 0
    response = client.post(
        '/products/save/',
        {
            'product_id': '1',
            'substitute_id': '2',
            'next': '/'
        }
    )
    assert client.session['keep_substitute']
    assert Substitute.objects.all().count() == 0
    assert response.status_code == 302


def test_save_get_redirect(createUser):
    """Test if request is not POST, redirect to index."""
    client.login(username='test@test.com', password="12345")
    response = client.get('/products/save/')
    assert response.status_code == 302


def test_save_post_false_id(createUser, createTwoProducts):
    """Test all good:
    user is connected
    product id and produc substitutes are ok
    POST request
    DB modification: new item in Substitute
    """
    client.login(username='test@test.com', password="12345")
    assert Substitute.objects.all().count() == 0
    with pytest.raises(Product.DoesNotExist):
        client.post(
            '/products/save/',
            {
                'product_id': '13',
                'substitute_id': '2',
                'next': '/'
            }
        )
    assert Substitute.objects.all().count() == 0


def test_save_after_login(createUser,createTwoProducts):
    """Test the path user made a selection before connect (Issue #2)."""
    client.login(username='test@test.com', password="12345")
    session = client.session
    session['keep_substitute'] = ('1', '2')
    session.save()

    assert Substitute.objects.all().count() == 0
    response = client.get(reverse('products:save'))

    assert Substitute.objects.all().count() == 1
    assert response.url == '/products/myproducts/'
    assert response.status_code == 302
