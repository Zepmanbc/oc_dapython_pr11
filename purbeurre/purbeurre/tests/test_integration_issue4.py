import time
import re

from django.core import mail
import pytest
from selenium import webdriver

from authentication.models import User


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@pytest.fixture
def createUser():
    user = User.objects.create(email='test@test.com')
    user.set_password('12345')
    user.save()


def test_reset_password(live_server, driver, createUser):
    """Test the reset password path (issue #4)"""
    driver.get(live_server.url)
    # Click on Account
    driver.find_elements_by_tag_name('a')[1].click()
    time.sleep(1)
    driver.find_element_by_partial_link_text('Mot de passe oublié').click()
    driver.find_element_by_id('id_email').send_keys("test@test.com")
    driver.find_element_by_xpath('/html/body/section/div/div/form/button').click()
    time.sleep(1)
    assert 'password_reset/done/' in driver.current_url
    assert len(mail.outbox)
    reset_link = re.search(
        r'http[s]?:[\w/-]+.[\w]+\/(?P<rest>[\w/-]+)',
        mail.outbox[0].body
    ).group()
    driver.get(reset_link)
    time.sleep(1)
    driver.find_element_by_id('id_new_password1').send_keys("qwer!@#$")
    driver.find_element_by_id('id_new_password2').send_keys("qwer!@#$")
    driver.find_element_by_xpath('/html/body/section/div/div/form/button').click()
    time.sleep(1)
    assert 'reset/done/' in driver.current_url
    driver.find_element_by_partial_link_text('identifier').click()
    driver.find_element_by_id('id_username').send_keys("test@test.com")
    driver.find_element_by_id('id_password').send_keys("qwer!@#$")
    driver.find_element_by_id('id_password').submit()
    time.sleep(1)
    # Test if Account page
    assert '/account/' in driver.current_url
