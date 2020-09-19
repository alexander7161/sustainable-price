
from flask import jsonify
from server import app


@app.route("/get_recommended")
def get_recommended():
    """get recommended products for a product id and user profile"""
    state = [{"name": "test"}]
    return jsonify(state)
