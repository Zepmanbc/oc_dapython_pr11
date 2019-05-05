import os
import time
import re

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


def test_homepage(live_server, driver, loadProducts):
    driver.get(live_server.url)
    expected = "Pur Beurre - Du gras, oui, mais de qualité"
    assert driver.title == expected


def test_full_path(live_server, driver, loadProducts):
    # Open index
    driver.get(live_server.url)
    # click on Account picture
    driver.find_elements_by_tag_name('a')[1].click()
    # Test if login page
    assert '/login/' in driver.current_url
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
    # Test if account page
    assert '/account/' in driver.current_url
    # Test User is connected
    assert 'test@test.com' in driver.page_source
    assert len(driver.get_cookies()) == 2
    # Test User created in DB
    assert User.objects.all().count()
    # Click logout
    driver.find_elements_by_tag_name('a')[3].click()
    time.sleep(1)
    # Test if index page
    assert live_server.url in driver.current_url
    # Test User not connected
    assert len(driver.get_cookies()) == 1
    # Click on Account
    driver.find_elements_by_tag_name('a')[1].click()
    time.sleep(1)
    # Fill in connection form
    driver.find_element_by_id('id_username').send_keys("test@test.com")
    driver.find_element_by_id('id_password').send_keys("qwer!@#$")
    driver.find_element_by_id('id_password').submit()
    time.sleep(1)
    # Test if Account page
    assert '/account/' in driver.current_url
    # Test User is connected
    assert 'test@test.com' in driver.page_source
    assert len(driver.get_cookies()) == 2
    # Go to index
    driver.find_elements_by_tag_name('a')[0].click()
    # Search 'nothing' in index input box
    index_query = driver.find_element_by_css_selector('.masthead input')
    index_query.send_keys("nothing")
    index_query.submit()
    time.sleep(1)
    # Test if no result
    assert 'pas de produits correspondant' in driver.page_source
    # Search 'choucroute' in navbar input box
    navbar_query = driver.find_element_by_css_selector('.navbar input')
    navbar_query.send_keys("choucroute")
    navbar_query.send_keys(Keys.RETURN)
    time.sleep(1)
    # Test if products in result
    assert 'product-thumb' in driver.page_source
    # Go to page 2
    driver.find_element_by_partial_link_text('Suivante').click()
    time.sleep(1)
    # Test if page=2 in url
    assert 'page=2' in driver.current_url
    # Go back
    driver.back()
    time.sleep(1)
    # Go to page 2, got to page 1 and test url
    driver.find_element_by_partial_link_text('Suivante').click()
    driver.find_element_by_partial_link_text('Précédente').click()
    assert re.search(r'http://localhost:[0-9]*/products/search/\?query=choucroute&page=1', driver.current_url)
    # Scroll to top of page, click on 2nd product
    driver.execute_script("window.scrollTo(0, 0);")
    prod2 = driver.find_elements_by_css_selector('.product-thumb img')[1]
    prod2.click()
    time.sleep(1)
    # Test if result page
    assert '/result/' in driver.current_url
    # Test if no Substitute in DB
    assert not Substitute.objects.all().count()
    # Click on 'sauvegarder' 1st product
    driver.find_elements_by_class_name('fa-save')[0].click()
    # Test if Substitute saved in DB
    assert Substitute.objects.all().count()
    time.sleep(1)
    # Test if myproducts page
    assert '/myproducts/' in driver.current_url
    # Click on Account
    driver.find_elements_by_tag_name('a')[1].click()
    time.sleep(1)
    # Test if account page
    assert '/account/' in driver.current_url
    # Click on my products
    driver.find_elements_by_tag_name('a')[2].click()
    time.sleep(1)
    # Test if myproducts page
    assert '/myproducts/' in driver.current_url
    # look at details and go back
    driver.find_elements_by_css_selector('.product-thumb-myproduct a img')[1].click()
    time.sleep(1)
    # Test if detail page
    assert '/detail/' in driver.current_url
    driver.find_elements_by_tag_name('button')[2].click()
    time.sleep(1)
    # Test if myproducts page
    assert '/myproducts/' in driver.current_url
    # Click on delete picture
    driver.find_elements_by_class_name('fa-trash-alt')[0].click()
    time.sleep(1)
    # Test if delete page
    assert '/delete/' in driver.current_url
    driver.find_elements_by_tag_name('form')[1].submit()
    time.sleep(1)
    # Test if myproducts page
    assert '/myproducts/' in driver.current_url
    # Test if no Substitue saved : "Il n'y a pas de produits enregistrés"
    assert 'pas de produits enregistrés' in driver.page_source
    # Test if no Substitute in DB
    assert not Substitute.objects.all().count()
    # Click on "Mentions légales"
    driver.find_element_by_partial_link_text('Mentions').click()
    time.sleep(1)
    # Test if legal page
    assert 'legal' in driver.current_url
    # Click on logo
    driver.find_elements_by_tag_name('a')[0].click()
    time.sleep(1)
    # Test if index page
    assert live_server.url in driver.current_url
