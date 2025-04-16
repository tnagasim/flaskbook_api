from flask import Blueprint, jsonify, request

from api import calculation


api = Blueprint("api", __name__)
