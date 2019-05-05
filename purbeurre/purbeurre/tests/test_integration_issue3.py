import os
import time

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


def test_modify_user_infos(live_server, driver, createUser):
    driver.get(live_server.url)
    # Click on Account
    driver.find_elements_by_tag_name('a')[1].click()
    time.sleep(1)
    # Fill in connection form
    driver.find_element_by_id('id_username').send_keys("test@test.com")
    driver.find_element_by_id('id_password').send_keys("12345")
    driver.find_element_by_id('id_password').submit()
    time.sleep(1)
    # Test if Account page
    assert '/account/' in driver.current_url
    driver.find_elements_by_tag_name('button')[1].click()
    time.sleep(1)
    assert '/modify/' in driver.current_url
    driver.find_element_by_id('id_first_name').send_keys("firstname")
    driver.find_element_by_id('id_last_name').send_keys("lastname")
    time.sleep(1)
    u = User.objects.all()[0]
    assert u.first_name == ''
    assert u.last_name == ''
    driver.find_element_by_id('id_last_name').submit()
    time.sleep(1)
    u = User.objects.all()[0]
    assert u.first_name == 'firstname'
    assert u.last_name == 'lastname'
    assert '/account/' in driver.current_url
    title_text = '<h1 class="text-white font-weight-bold">Firstname Lastname</h1>'
    assert title_text in driver.page_source
