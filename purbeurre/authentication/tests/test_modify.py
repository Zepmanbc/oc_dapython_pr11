from django.test import Client
from django.urls import reverse

import pytest

from authentication.models import User

client = Client()
pytestmark = pytest.mark.django_db


@pytest.fixture
def createUser():
    user = User.objects.create(
        email='test@test.com',
        first_name='firstname',
        last_name='lastname'
        )
    user.set_password('12345')
    user.save()


def test_modify_basic(createUser):
    """Test if modification of user infos are ok."""
    u = User.objects.get(pk=1)
    assert u.first_name == 'firstname'
    assert u.last_name == 'lastname'
    client.login(email="test@test.com", password="12345")
    response = client.post(
            reverse('authentication:modify'),
            {'first_name': 'prenom', 'last_name': 'nom'}
        )
    assert response.status_code == 302
    assert response.url == '/auth/account/'
    u = User.objects.get(pk=1)
    assert u.first_name == 'prenom'
    assert u.last_name == 'nom'
