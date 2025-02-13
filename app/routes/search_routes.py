from flask import Blueprint, request, jsonify
from app.config import db
from app.routes.users_routes import token_required
from fuzzywuzzy import fuzz

search_bp = Blueprint("search", __name__)

@search_bp.route("/nearby-lost-items", methods=["GET"])
@token_required
def search_nearby_items():
    """API to retrieve lost and found items near a given location"""
    location_query = request.args.get("location", "").strip().lower()

    if not location_query:
        return jsonify({"error": "Location query is required."}), 400

    # Fetch lost & found items
    lost_items = list(db.lost_items.find({}))
    found_items = list(db.found_items.find({}))

    # Filter items with fuzzy location matching
    nearby_lost_items = [
        {**item, "id": str(item["_id"])}
        for item in lost_items
        if fuzz.partial_ratio(location_query, item.get("location", "").strip().lower()) > 50
    ]

    nearby_found_items = [
        {**item, "id": str(item["_id"])}
        for item in found_items
        if fuzz.partial_ratio(location_query, item.get("location", "").strip().lower()) > 50
    ]

    return jsonify({
        "nearby_lost_items": nearby_lost_items,
        "nearby_found_items": nearby_found_items,
    }), 200
