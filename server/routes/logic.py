import requests
from requests.auth import HTTPBasicAuth
import re
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from country_list import countries_for_language
from .nutriscore_calculation import simplified_nutriscore

import requests_cache

requests_cache.install_cache('demo_cache')


class Logic:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="xxx")

        countries = dict(countries_for_language('de'))

        country_names_german = list(countries.values())

        country_names_german.append('EU')
        country_names_german.append('Europäische Union')
        self.country_names_german = country_names_german

    # param user_weigths example
    # user_weights = {
    #     'price': 0.4,
    #     'sustainability': 0.4,
    #     'nutri_score': 0.2,
    # }
    def compare_products(self, original_gtin, user_weights):
        # get product details
        original_product_id = self.product_id_from_gtin(gtin=original_gtin)
        print(original_product_id)
        original_product_details = self.product_details_from_id(product_id=original_product_id)

        print(original_product_details)

        # get related products from group
        related_product_ids = self.get_group_products(category_code=original_product_details['product_category'])

        print(related_product_ids)

        # get related product information
        all_product_details = [original_product_details]
        for product_id in related_product_ids:
            all_product_details.append(self.product_details_from_id(product_id=product_id))

        # compute scores
        # add 'score' to dicts
        all_product_details = list(map(lambda x: dict(x, **{'score': 0.0}), all_product_details))

        # compute price score
        all_prices_abs = list(map(lambda x: x['price'], all_product_details))
        all_quantities = list(map(lambda x: float(re.sub('[^0-9.]', '', x['display_quantity'])), all_product_details))
        all_prices = [p / q for p, q in zip(all_prices_abs, all_quantities)]

        max_price = float(max(all_prices))
        min_price = float(min(all_prices))

        print(all_product_details)
        print(user_weights['price'])

        all_product_details = list(map(lambda x: dict(
            x,
            **{'score': x['score'] + user_weights['price'] * (
                    x['price'] / float(re.sub('[^0-9.]', '', x['display_quantity'])) - min_price) / (
                                max_price - min_price)}
        ), all_product_details))

        all_product_details = list(map(lambda x: dict(
            x,
            **{'score_price': (x['price'] / float(re.sub('[^0-9.]', '', x['display_quantity'])) - min_price) / (
                    max_price - min_price),
               'score_price_color': self.value_color((x['price'] / float(re.sub('[^0-9.]', '', x['display_quantity'])) - min_price) / (
                       max_price - min_price))}
        ), all_product_details))

        # compute sustainability score
        def get_distance_score(origin_distance_km):
            green = 300
            yellow = 4000
            orange = 11000
            # max_distance = 18000
            if (origin_distance_km <= green):
                return 1
            elif (origin_distance_km <= yellow):
                return 0.66
            elif (origin_distance_km <= orange):
                return 0.33
            else:
                return 0

        all_product_details = list(map(lambda x: dict(
            x,
            **{'score': x['score'] + user_weights['sustainability'] * get_distance_score(x['origin_distance_km'])}
        ), all_product_details))

        all_product_details = list(map(lambda x: dict(
            x,
            **{'score_sustainability': get_distance_score(x['origin_distance_km']),
               'score_sustainability_color': self.value_color(get_distance_score(x['origin_distance_km']))}
        ), all_product_details))

        # compute nutrition score
        nutri_score_weight = {
            'A': 1.00,
            'B': 0.75,
            'C': 0.50,
            'D': 0.25,
            'E': 0.00,
        }

        all_product_details = list(map(lambda x: dict(
            x,
            **{'score': x['score'] + user_weights['nutri_score'] * nutri_score_weight[x['nutri_score']]}
        ), all_product_details))

        all_product_details = list(map(lambda x: dict(
            x,
            **{'score_nutri_score': nutri_score_weight[x['nutri_score']],
               'score_nutri_score_color': self.value_color(nutri_score_weight[x['nutri_score']])}
        ), all_product_details))

        return sorted(all_product_details, key=lambda product: product['score'], reverse=True)

    def product_id_from_gtin(self, gtin):
        query = {
            'gtins': gtin,
            'verbosity': 'id'
        }

        response = requests.get(
            'https://hackzurich-api.migros.ch/products',
            params=query,
            auth=HTTPBasicAuth('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

        return response.json()['ids'][0]

    def product_details_from_id(self, product_id):
        query = {
            'verbosity': 'full'
        }

        response = requests.get(
            f'https://hackzurich-api.migros.ch/products/{product_id}',
            params=query,
            auth=HTTPBasicAuth('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

        original_product = response.json()

        # product name
        original_product_name = original_product['names']['name_rpa']

        # get nutrients
        nutrients = {}

        for nutrient in original_product['nutrition_facts']['standard']['nutrients']:
            if nutrient['name'] == 'Energie':
                nutrients['energy'] = nutrient['quantity']
            elif nutrient['name'] == 'davon Zucker':
                nutrients['sugars'] = nutrient['quantity']
            elif nutrient['name'] == 'davon gesättigte Fettsäuren':
                nutrients['saturated_fat'] = nutrient['quantity']
            elif nutrient['name'] == 'Salz':
                nutrients['sodium'] = nutrient['quantity']

        original_product_nutri_score = simplified_nutriscore(nutrients)

        # origin
        origin_string = '-'.join(original_product['origins'].values())

        for country_name in self.country_names_german:
            if country_name.lower() in origin_string.lower():
                location_origin_str = country_name
                continue

        location_origin = self.geolocator.geocode(location_origin_str)
        location_ch = self.geolocator.geocode("Schweiz")

        original_product_origin_distance = geodesic(
            (location_origin.latitude, location_origin.longitude),
            (location_ch.latitude, location_ch.longitude)
        ).kilometers

        # category
        original_product_category = original_product['categories'][0]['code']

        # rating
        original_product_rating = original_product['ratings']['average_all']

        # price
        original_product_price = original_product['price']['item']['price']
        # original_product_base_price = original_product['price']['base']['price']

        # quantity/unit
        original_product_quantity = original_product['price']['item']['quantity']
        original_product_unit = original_product['price']['item']['unit']
        original_product_display_quantity = original_product['price']['item']['display_quantity']

        # label available?
        original_product_label = False
        if 'labels' in original_product:
            original_product_label = original_product['labels'][0] in ["CO2", "L02", "L03", "L04", "L05", "L06", "L07",
                                                                       "L09", "L10", "L14", "L16", "L17", "L28", "L29",
                                                                       "L33", "L34", "L35", "L36", "L38", "L41", "L42",
                                                                       "L43", "L44", "L45", "L46", "L55", "L56", "L57",
                                                                       "L59", "L60", "L62", "L64", "L65", "L67", "L68",
                                                                       "L69", "L71", "TIW"]
            original_product_label = True

        # product picture URL
        original_product_picture_url = original_product['image']['original']

        return {
            'product_id': product_id,
            'product_name': original_product_name,
            'origin_distance_km': original_product_origin_distance,
            'has_label': original_product_label,
            'product_category': original_product_category,
            'customer_rating': original_product_rating,
            'nutri_score': original_product_nutri_score,
            'price': original_product_price,
            # 'base_price': original_product_base_price,
            'picture_url': original_product_picture_url,
            'quantity': original_product_quantity,
            'display_quantity': original_product_display_quantity,
            'unit': original_product_unit,
        }

    def get_group_products(self, category_code):
        # TODO: INCREASE LIMIT
        LIMIT = 3

        query_category = {
            'limit': LIMIT,
            'facets[category][]': category_code
        }

        similar_products = requests.get(
            'https://hackzurich-api.migros.ch/products',
            params=query_category,
            auth=HTTPBasicAuth('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

        similar_products = similar_products.json()['products']
        related_product_ids = []
        for similar_product in similar_products:
            related_product_ids.append(similar_product['id'])

        return related_product_ids

    # param: normalized_base_price, float. A value between 0 and 1
    def value_color(self, value: float):
        if value < 0.3:
            return "red"
        elif value >= 0.3 and value < 0.6:
            return "orange"
        else:
            return "green"
