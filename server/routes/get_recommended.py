import requests_cache
from flask import jsonify, request
from server import app
import requests
requests_cache.install_cache()


@app.route("/get_recommended")
def get_recommended():
    """get recommended products for a product barcode and persona"""
    barcode = request.args.get('barcode')
    persona = request.args.get('persona')

    r = requests.get('https://hackzurich-api.migros.ch/products',
                     auth=('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

    print("From cache: %s" % (r.from_cache))

    r.raise_for_status()
    data = r.json()
    return jsonify([{"productID": "firstID",
                     "name": "tomatoes",
                     "image": None
                     },
                    {"productID": "secondID",
                     "name": "potatos",
                     "image": None
                     }])
