import os

from django.core import serializers

import pytest
from authentication.models import User
from products.models import Product, Substitute


@pytest.fixture
def loadProducts():
    """Load 10 products from dump.json."""
    dump = os.path.dirname(os.path.abspath(__file__)) + "/dump.json"
    data = open(dump, 'r')
    for deserialized_object in serializers.deserialize("json", data):
        deserialized_object.save()


@pytest.fixture
def createUser():
    user = User.objects.create(email='test@test.com')
    user.set_password('12345')
    user.save()


@pytest.fixture
def createTwoProducts():
    p1 = Product.objects.create(
        product_name='Produit 1',
        nutrition_grades='c',
        fat='low',
        fat_100g=0.5,
        saturated_fat='low',
        saturated_fat_100g=0.5,
        sugars='low',
        sugars_100g=0.5,
        salt='low',
        salt_100g=0.5,
        image_url='',
        url='',
        category='food'
        )
    p1.save()
    p2 = Product.objects.create(
        product_name='Produit 2',
        nutrition_grades='b',
        fat='low',
        fat_100g=0.5,
        saturated_fat='low',
        saturated_fat_100g=0.5,
        sugars='low',
        sugars_100g=0.5,
        salt='low',
        salt_100g=0.5,
        image_url='',
        url='',
        category='food'
        )
    p2.save()


@pytest.fixture
def createSubstitutes(loadProducts, createUser):
    p1 = Product.objects.get(pk=1)
    p2 = Product.objects.get(pk=2)
    p3 = Product.objects.get(pk=3)
    p4 = Product.objects.get(pk=4)

    u = User.objects.get(pk=1)
    combi = [(p1, p2), (p1, p3), (p1, p4), (p2, p3), (p2, p4), (p3, p4)]
    for pr, su in combi:
        s = Substitute.objects.create(
            product_id=pr,
            substitute_id=su,
            user_id=u
        )
        s.save()
