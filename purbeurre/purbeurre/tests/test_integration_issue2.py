import os
import time

from django.core import serializers

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from products.models import Substitute
from authentication.models import User


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


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


def test_issue2_path_connect(live_server, driver, createUser, loadProducts):
    """#issue2 user path: select product and connect"""
    # not connected, search 'choucroute'
    driver.get(live_server.url)
    index_query = driver.find_element_by_css_selector('.masthead input')
    index_query.send_keys("choucroute")
    index_query.submit()
    time.sleep(1)
    # select product
    prod2 = driver.find_elements_by_css_selector('.product-thumb img')[1]
    prod2.click()
    time.sleep(1)
    # save substitute
    driver.find_elements_by_class_name('fa-save')[0].click()
    # redirect to connect page => connect
    # Fill in connection form
    driver.find_element_by_id('id_username').send_keys("test@test.com")
    driver.find_element_by_id('id_password').send_keys("12345")
    driver.find_element_by_id('id_password').submit()
    time.sleep(1)
    # redirect to my product and substitute saved
    assert '/myproducts/' in driver.current_url
    assert Substitute.objects.count()


def test_issue2_path_register(live_server, driver, loadProducts):
    """#issue2 user path: select product and register"""
    # not connected, search 'choucroute'
    driver.get(live_server.url)
    index_query = driver.find_element_by_css_selector('.masthead input')
    index_query.send_keys("choucroute")
    index_query.submit()
    time.sleep(1)
    # select product
    prod2 = driver.find_elements_by_css_selector('.product-thumb img')[1]
    prod2.click()
    time.sleep(1)
    # save substitute
    driver.find_elements_by_class_name('fa-save')[0].click()
    # redirect to connect page => go register => register
    # click on "Créer un compte"
    driver.find_element_by_partial_link_text('compte').click()
    # Test if register page
    assert '/register/' in driver.current_url
    # fill in form
    driver.find_element_by_id('id_email').send_keys("test@test.com")
    driver.find_element_by_id('id_first_name').send_keys("Firstname")
    driver.find_element_by_id('id_last_name').send_keys("Lastname")
    driver.find_element_by_id('id_password1').send_keys("qwer!@#$")
    driver.find_element_by_id('id_password2').send_keys("qwer!@#$")
    # Test if no User in DB
    assert not User.objects.all().count()
    driver.find_element_by_id('id_password2').submit()
    time.sleep(1)
    # redirect to my product and substitute saved
    assert '/myproducts/' in driver.current_url
    assert Substitute.objects.count()
