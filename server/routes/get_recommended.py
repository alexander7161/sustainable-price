import requests_cache
from flask import jsonify, request
from server import app
import json
requests_cache.install_cache()
from .logic import Logic


@app.route("/get_recommended")
def get_recommended():
    """get recommended products for a product barcode and persona"""
    barcode = request.args.get('barcode')
    print(barcode)
    persona = json.loads(request.args.get('persona'))
    print(persona)

    logic = Logic()
    data = logic.compare_products(barcode, persona)

    return jsonify(data)
