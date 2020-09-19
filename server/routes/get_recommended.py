
from flask import jsonify
from server import app
import requests


@app.route("/get_recommended")
def get_recommended():
    """get recommended products for a product id and user profile"""

    r = requests.get('https://hackzurich-api.migros.ch/products',
                     auth=('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

    r.raise_for_status()
    data = r.json()
    return data
