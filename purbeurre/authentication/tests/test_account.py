from django.test import Client
from django.urls import reverse

import pytest

from authentication.models import User

client = Client()
pytestmark = pytest.mark.django_db


def test_not_logged_redirect():
    # if not logged, redirect to login page
    response = client.get(reverse('authentication:account')).status_code
    assert response == 302


def test_loggedin_user():
    # if logged, show page
    user = User.objects.create(email='test@test.com')
    user.set_password('12345')
    user.save()
    client.login(email="test@test.com", password="12345")

    response = client.get(reverse('authentication:account')).status_code
    assert response == 200


def test_keep_substitute_redirection():
    """Test if user had a substitute save before connect. Issue #2"""
    user = User.objects.create(email='test@test.com')
    user.set_password('12345')
    user.save()

    client.login(email="test@test.com", password="12345")

    session = client.session
    session['keep_substitute'] = ('1', '2')
    session.save()

    response = client.get(reverse('authentication:account')).status_code
    assert response == 302
