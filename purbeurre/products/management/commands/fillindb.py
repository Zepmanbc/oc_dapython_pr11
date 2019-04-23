from django.core.management.base import BaseCommand
from products.models import Product

import requests


class Command(BaseCommand):
    help = 'Fill in database with OpenFoodFacts Products'

    categories_list = [
        "choucroute",
        "sandwich",
        "fromage",
        "crepe",
        "compotes",
        "pizza",
        "ravioli",
        "creme chocolat",
        "yaourt aux fruits",
        "pates a tartiner"
    ]

    keep_data = [
        'product_name',
        'nutrition_grades_tags',
        'image_url',
        'url',
        'categories',
    ]

    keep_data_nutriments = [
        'fat_100g',
        'saturated-fat_100g',
        'sugars_100g',
        'salt_100g',
    ]

    keep_data_nutrient_levels = [
        'salt',
        'sugars',
        'saturated-fat',
        'fat',
    ]

    def add_arguments(self, parser):
        parser.add_argument('product_qty', nargs='+', type=int)

    def handle(self, *args, **options):
        product_qty = options['product_qty']

        for categ in self.categories_list:
            products_list = self.get_products(categ, product_qty)
            for product in products_list:
                self.save_in_db(product, categ)
        self.stdout.write(self.style.SUCCESS("Done"))

    def get_products(self, categ, product_qty):
        url = "https://fr.openfoodfacts.org/cgi/search.pl"
        payloads = {
            'action': 'process',
            'search_terms': categ,
            'page_size': product_qty,
            'json': 1
        }
        r = requests.get(url, payloads).json()
        return r['products']
        self.stdout.write(self.style.SUCCESS("Get from OFF: %" % categ))

    def clean_data(self, product):
        clean_product = {}
        for elem in self.keep_data:
            # if not product[elem] or elem not in product:
            if elem not in product:
                product[elem] = ''
            clean_product[elem] = product[elem]
        for elem in self.keep_data_nutriments:
            if elem not in product['nutriments']:
                product['nutriments'][elem] = 0
            clean_product[elem] = product['nutriments'][elem]
        for elem in self.keep_data_nutrient_levels:
            # if not product['nutrient_levels'][elem]:
            if elem not in product['nutrient_levels']:
                product['nutrient_levels'][elem] = ''
            clean_product[elem] = product['nutrient_levels'][elem]
        clean_product['nutrition_grades_tags'] = \
            clean_product['nutrition_grades_tags'][0]
        if len(clean_product['nutrition_grades_tags']) > 1:
            clean_product['nutrition_grades_tags'] = 'z'
        return clean_product

    def save_in_db(self, product, categ):
        cln_product = self.clean_data(product)

        p = Product(
            product_name=cln_product['product_name'],
            nutrition_grades=cln_product['nutrition_grades_tags'],
            fat=cln_product['fat'],
            fat_100g=cln_product['fat_100g'],
            saturated_fat=cln_product['saturated-fat'],
            saturated_fat_100g=cln_product['saturated-fat_100g'],
            sugars=cln_product['sugars'],
            sugars_100g=cln_product['sugars_100g'],
            salt=cln_product['salt'],
            salt_100g=cln_product['salt_100g'],
            image_url=cln_product['image_url'],
            url=cln_product['url'],
            category=categ,
        )
        p.save()
