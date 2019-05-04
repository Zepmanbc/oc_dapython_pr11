from django.test import Client
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
import pytest

from authentication.models import User
from products.models import Product, Substitute

client = Client()
pytestmark = pytest.mark.django_db

from .pytest_fixture import createTwoProducts, loadProducts


def test_search_success(createTwoProducts):
    """Search real query: return something"""
    response = client.get('/products/search/?query=produit')
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 2


def test_search_nothing(createTwoProducts):
    """Search false query: return something"""
    response = client.get('/products/search/?query=stuff')
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 0


def test_search_failed(createTwoProducts):
    # Test a good page
    response = client.get('/products/search/?query=produit&page=1')
    assert response.status_code == 200
    # PAge 2 does not exist : 404
    response = client.get('/products/search/?query=produit&page=2')
    assert response.status_code == 404
    # missing query : 500
    with pytest.raises(MultiValueDictKeyError):
        response = client.get('/products/search/')


def test_pagination_only_one_page(loadProducts):
    """Test if page is only one time in url.
    Search the product, go to page 2, go to page 1
    there mus be only one `page=1` and not `page=2&page=1`
    """
    response = client.get('/products/search/?query=choucroute&page=2')
    bad_link = '<a href="/products/search/?query=choucroute&amp;page=2&page=1">Précédente</a>'
    good_link = '<a href="/products/search/?query=choucroute&page=1">Précédente</a>'
    assert bad_link not in response.rendered_content
    assert good_link in response.rendered_content
