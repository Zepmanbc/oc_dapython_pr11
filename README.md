# Pur Beurre - Du gras, oui mais de qualité

[![Build Status](https://travis-ci.org/Zepmanbc/oc_dapython_pr8.svg?branch=master)](https://travis-ci.org/Zepmanbc/oc_dapython_pr8)
[![Coverage Status](https://coveralls.io/repos/github/Zepmanbc/oc_dapython_pr8/badge.svg)](https://coveralls.io/github/Zepmanbc/oc_dapython_pr8)

Pur Beurre is an application made for Project 8 of OpenClassrooms DA Python.

It is a Django application that allows you to find a food product and choose a substitute with a better nutrition grade.

## Getting Started

You can use is directly at this adress: [https://bc-ocdapythonpr8.herokuapp.com/](https://bc-ocdapythonpr8.herokuapp.com/)

### Prerequisites

This application works with Python 3.6 and Django 2.2

You can choose the SGDB you want, just configure in [*settings.py*](https://github.com/Zepmanbc/oc_dapython_pr8/blob/master/purbeurre/purbeurre/settings.py)

### Installing

clone this repo

    git clone https://github.com/Zepmanbc/oc_dapython_pr8.git

create the virtualenv and install dependencies

    cd oc_dapython_pr8
    pipenv install

create environment variables (here is for development config)

    ENV=DEV 
    SECRET_KEY= [SECRETKEY] 
    DB_NAME=purbeurre 
    DB_USER=root 
    DB_PASSWORD=root

I suppose here that you use MySQL, you must create a database named `purbeurre` and your user's login and password are `root`.

If you use a different SGDB you can configure it in [*settings.py*](https://github.com/Zepmanbc/oc_dapython_pr8/blob/master/purbeurre/purbeurre/settings.py)

Run migrate and fill in database (here with 50 product of each category)

    purbeurre/manage.py migrate
    purbeurre/manage.py fillindb 50

Then run server

    purbeurre/manage.py runserver

## Running the tests

    pytest purbeurre/

## Deployment

Deployement config is set for Heroku. You need to create environment variables in Heroku

    ENV=PRODUCTION
    SECRET_KEY= [SECRETKEY]

The production configuration is set for Postgres, activate it in Heroku.

    heroku addons:create heroku-postgresql:hobby-dev

Keep in mind to migrate and fill in database.

## Configuration

You can access to admin section with adding `/admin/` to your url.

You can modify fill in categories in [fillindb.py](https://github.com/Zepmanbc/oc_dapython_pr8/blob/master/purbeurre/products/management/commands/fillindb.py)


## Built With

* [Django](https://www.djangoproject.com/)
* [Start Bootstrap Template](https://startbootstrap.com/themes/creative/)
* [OpenFoodFacts](https://fr.openfoodfacts.org/) : used for fill in database
