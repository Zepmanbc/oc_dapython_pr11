from django.test import Client
from django.urls import reverse

import pytest

from authentication.models import User

client = Client()
pytestmark = pytest.mark.django_db


@pytest.fixture
def createUser():
    user = User.objects.create(email='test@test.com')
    user.set_password('12345')
    user.save()


def test_register_url():
    response = client.get('/accounts/register/')
    assert response.status_code == 200
    assert reverse('authentication:register') == '/accounts/register/'


def test_register_success():
    """ all goood: succes => modify db, user in request, redirect"""
    assert User.objects.all().count() == 0
    reponse = client.post(
            reverse('authentication:register'),
            {
                'email': 'test@test.com',
                'password1': '12345###',
                'password2': '12345###'
            }
        )
    assert User.objects.all().count() == 1
    assert reponse.status_code == 302
    assert client.session._session['_auth_user_id'] == '1'


def test_register_already_exist(createUser):
    """ no redirection no change in db not connected """
    assert User.objects.all().count() == 1
    reponse = client.post(
        reverse('authentication:register'),
        {
            'email': 'test@test.com',
            'password1': '12345###',
            'password2': '12345###'
        }
    )
    assert User.objects.all().count() == 1
    assert reponse.status_code == 200
    with pytest.raises(KeyError):
        client.session._session['_auth_user_id']
# all goood: succes => modify db, user in request, redirect

# user allready exists
