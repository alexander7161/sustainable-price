from flask import jsonify, request, Response
from server import app


@app.route("/test_api")
def test_api():
    """test"""
    return jsonify([{"test": "working!"}])
