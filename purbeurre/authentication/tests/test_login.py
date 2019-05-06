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


def test_login_url():
    response = client.get('/accounts/login/')
    assert response.status_code == 200
    assert reverse('authentication:login') == '/accounts/login/'


def test_login_success(createUser):
    """ test if login is ok and user in session."""
    reponse = client.post(
            reverse('authentication:login'),
            {'username': 'test@test.com', 'password': '12345'}
        )
    assert reponse.status_code == 302
    assert client.session._session['_auth_user_id'] == '1'


def test_login_fail(createUser):
    """Test with wrong password, no connection."""
    reponse = client.post(
            reverse('authentication:login'),
            {'username': 'test@test.com', 'password': 'xxxxx'}
        )
    assert reponse.status_code == 200
    with pytest.raises(KeyError):
        client.session._session['_auth_user_id']
