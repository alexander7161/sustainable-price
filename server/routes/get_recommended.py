import requests_cache
from flask import jsonify, request
from server import app
import json
requests_cache.install_cache()
from .logic import Logic

PARAM_SUSTAINABLE = 'sustainable'
PARAM_HEALTHY = 'healthy'
PARAM_SAVER = 'saver'

MAP_ARG_TO_PERSONA = {
    PARAM_SUSTAINABLE: {'price': 0, 'sustainability': 1, 'nutri_score': 0},
    PARAM_HEALTHY: {'price': 0, 'sustainability': 0, 'nutri_score': 1},
    PARAM_SAVER: {'price': 1, 'sustainability': 0, 'nutri_score': 0},
    f"{PARAM_SUSTAINABLE}-{PARAM_HEALTHY}": {'price': 0, 'sustainability': 0.5, 'nutri_score': 0.5},
    f"{PARAM_SUSTAINABLE}-{PARAM_SAVER}": {'price': 0.5, 'sustainability': 0.5, 'nutri_score': 0},
    f"{PARAM_HEALTHY}-{PARAM_SAVER}": {'price': 0.5, 'sustainability': 0, 'nutri_score': 0.5},
    'all': {'price': 0.333, 'sustainability': 0.334, 'nutri_score': 0.333},
}

@app.route("/get_recommended")
def get_recommended():
    """get recommended products for a product barcode and persona"""
    barcode = request.args.get('barcode')
    print(barcode)
    persona = request.args.get('persona').split("-")
    print(persona)

    print(map_persona(persona))

    logic = Logic()
    data = logic.compare_products(barcode, map_persona(persona))

    return jsonify(data)


def map_persona(persona):
    if len(persona) == 1:
        return MAP_ARG_TO_PERSONA[persona[0]]
    elif len(persona) == 3:
        return MAP_ARG_TO_PERSONA['all']
    else:
        if PARAM_SUSTAINABLE in persona and PARAM_HEALTHY in persona:
            return MAP_ARG_TO_PERSONA[f"{PARAM_SUSTAINABLE}-{PARAM_HEALTHY}"]
        elif PARAM_SUSTAINABLE in persona and PARAM_SAVER in persona:
            return MAP_ARG_TO_PERSONA[f"{PARAM_SUSTAINABLE}-{PARAM_SAVER}"]
        elif PARAM_HEALTHY in persona and PARAM_SAVER in persona:
            return MAP_ARG_TO_PERSONA[f"{PARAM_HEALTHY}-{PARAM_SAVER}"]


