from django.test import Client
from django.urls import reverse

import pytest

from authentication.models import User

client = Client()
pytestmark = pytest.mark.django_db


def test_not_logged_redirect():
    # if not logged, redirect to login page
    response = client.get(reverse('authentication:logout')).status_code
    assert response == 302


def test_loggedin_user():
    # test if user is logged
    # go to lougout page: redirection
    # user not legged anymore
    user = User.objects.create(email='test@test.com')
    user.set_password('12345')
    user.save()
    client.login(email="test@test.com", password="12345")
    assert client.session._session['_auth_user_id'] == '1'
    response = client.get(reverse('authentication:logout')).status_code
    assert response == 302
    with pytest.raises(KeyError):
        client.session._session['_auth_user_id']
