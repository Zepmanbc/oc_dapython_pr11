import pytest
from authentication.models import User
from products.models import Product, Substitute


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
