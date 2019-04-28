from django.core.management.base import BaseCommand
from products.models import Product

import requests


class Command(BaseCommand):
    help = 'Fill in database with OpenFoodFacts Products. (0 for update current)'

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
        "pates a tartiner",]

    keep_data = [
        'code',
        'product_name',
        'nutrition_grades_tags',
        'image_url',
        'url',
        'categories',
        'last_modified_t',]

    keep_data_nutriments = [
        'fat_100g',
        'saturated-fat_100g',
        'sugars_100g',
        'salt_100g',]

    keep_data_nutrient_levels = [
        'salt',
        'sugars',
        'saturated-fat',
        'fat',]

    def add_arguments(self, parser):
        parser.add_argument(
            'product_qty',
            nargs='+',
            type=int,
            help='Get N products from OpenFoodFacts, 0 for update',
        )

    def handle(self, *args, **options):
        product_qty = options['product_qty'][0]

        if product_qty == 0:
            for productdb in Product.objects.all():
                self.update_product(productdb)
        else:
            for categ in self.categories_list:
                products_list = self.get_products(categ, product_qty)
                for product in products_list:
                    self.save_in_db(product, categ)
        self.stdout.write(self.style.SUCCESS("Done"))

    def update_product(self, productdb):
        """Update product on database"""
        if self.check_if_exist(productdb.id_off):
            off_data = self.get_product_from_off(productdb.id_off)
            if off_data:
                if productdb.last_modified_t < off_data['last_modified_t']:
                    self.update_database(productdb, off_data)
                    self.stdout.write(self.style.SUCCESS("Update - {}".format(productdb.product_name)))


    def get_products(self, categ, product_qty):
        """Get a json page of <product_qty> for a category.

        Args:
            categ (string): category, but could be any query
            product_qty (int): quantity of wanted product in this category
        
        Return:
            list of json with all OpenFoodFacts data per product
        """
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
        """Clean OpenFoodFacts data.

        Args:
            product (json):all the data

        Return:
            dict: with only wanted data
                from keep_data, keep_data_nutriments 
                and keep_data_nutrient_levels lists

                fill with '' or 0 if does not exist
                fill with 'z' if nutrition_grades_tags is empty
        """
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
        """Save product in database.

        Args:
            product (json):all the data of 1 product.
            categ (string): category

        Return:
            Stored if database if does not already exists
        """
        cln_product = self.clean_data(product)
        if not self.check_if_exist(int(cln_product['code'])):
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
                last_modified_t=cln_product['last_modified_t'],
                id_off=cln_product['code'],
            )
            p.save()


    @staticmethod
    def check_if_exist(id_off):
        """Check if product allreadyexist in Database.
        
        args:
            id_off (str): code of OpenFoodFacts

        return:
            True/False if in the Database
        """
        try:
            Product.objects.get(id_off=id_off)
            exist = True
        except Product.DoesNotExist:
            exist = False
        return exist


    @staticmethod
    def get_product_from_off(code):
        """Get product from OpenFoodFacts with code.

        args:
            code (str): id of a product on OpenFoodFacts
        
        return:
            False : if does not exists
            json
        
        """
        result = False
        url = "https://fr.openfoodfacts.org/api/v0/product/{}.json".format(code)
        r = requests.get(url).json()
        if r['status']:
            result = r['product']
        return result


    def update_database(self, productdb, off_data):
        """Update a product in the Database fron OpenFoodFacts Data.

        productdb: Products object
        off_data: json
        """
        cln_product = self.clean_data(off_data)

        productdb.product_name=cln_product['product_name']
        productdb.nutrition_grades=cln_product['nutrition_grades_tags']
        productdb.fat=cln_product['fat']
        productdb.fat_100g=cln_product['fat_100g']
        productdb.saturated_fat=cln_product['saturated-fat']
        productdb.saturated_fat_100g=cln_product['saturated-fat_100g']
        productdb.sugars=cln_product['sugars']
        productdb.sugars_100g=cln_product['sugars_100g']
        productdb.salt=cln_product['salt']
        productdb.salt_100g=cln_product['salt_100g']
        productdb.image_url=cln_product['image_url']
        productdb.last_modified_t=cln_product['last_modified_t']
        productdb.save()
