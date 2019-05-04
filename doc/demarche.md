# Améliorez un projet existant en Python

[Tableau Trello](https://trello.com/b/rq2AwW7O/ocdapythonpr11)

[Repo Github](https://github.com/Zepmanbc/oc_dapython_pr11)

[Site en ligne](https://bc-ocdapythonpr11.herokuapp.com/)

## Création des *issues* sur Github

[https://github.com/Zepmanbc/oc_dapython_pr11/issues](https://github.com/Zepmanbc/oc_dapython_pr11/issues)

![issues sur github](img/issues.png)

## [Issue #1](https://github.com/Zepmanbc/oc_dapython_pr11/issues/1) : accumulation des pages lors d'une pagination

Création d'une branche *pagination*

### Ecriture des tests

[*test_search.py*](https://github.com/Zepmanbc/oc_dapython_pr10/blob/master/purbeurre/products/tests/test_search.py)

=> test_pagination_only_one_page

    def test_pagination_only_one_page(loadProducts):
        """Test if page is only one time in url.
        Search the product, go to page 2, go to page 1
        there mus be only one `page=1` and not `page=2&page=1`
        """
        response = client.get('/products/search/?query=choucroute&page=2')
        bad_link = '<a href="/products/search/?query=choucroute&amp;page=2&page=1">Précédente</a>'
        good_link = '<a href="/products/search/?query=choucroute&page=1">Précédente</a>'
        assert bad_link not in response.rendered_content
        assert good_link in response.rendered_content

### Modification du code

[*search.html*](https://github.com/Zepmanbc/oc_dapython_pr10/blob/master/purbeurre/products/templates/products/search.html)

code original:

    <a href="{{ request.get_full_path }}&page={{ page_obj.previous_page_number }}">Précédente</a>

code modifié

    <a href="{{ request.path }}?query={{ query }}&page={{ page_obj.previous_page_number }}">Précédente</a>

(idem pour la page Suivante)

### mise à jour du test Selenium

[*test_integration.py*](https://github.com/Zepmanbc/oc_dapython_pr11/blob/master/purbeurre/purbeurre/tests/test_integration.py)

    # Go to page 2, got to page 1 and test url
    driver.find_element_by_partial_link_text('Suivante').click()
    driver.find_element_by_partial_link_text('Précédente').click()
    assert re.search('http:\/\/localhost:\d*\/products\/search\/\?query=choucroute&page=1', driver.current_url)

## Pull request + merge dans le master: mise en production



## Bug 2 : Perte de la séléction si l'utilisateur n'est pas connecté

Création d'une branche *lostsave*

### Ecriture des tests

### Modification du code

### mise à jour du test Selenium

Pull request + merge dans le master: mise en production

## Amélioration 1 : Modification nom/prénom

Création d'une branche *namemodif*

### Ecriture des tests

### Modification du code

### mise à jour du test Selenium

Pull request + merge dans le master: mise en production


## Amélioration 2 : Réinitialisation du mot de passe

Création d'une branche *resetpassword*

### Ecriture des tests

### Modification du code

### mise à jour du test Selenium

Pull request + merge dans le master: mise en production
