from app.config import db
from app.services.email_service import send_email
from fuzzywuzzy import fuzz
from flask import Blueprint, jsonify
from app.jwt_token import token_required

match_bp = Blueprint("match", __name__)

@match_bp.route("/match-items/", methods=["GET"])
@token_required
def find_matches():
    """ Finds matches between lost and found items and sends notifications. """
    lost_items = list(db.lost_items.find({}))
    found_items = list(db.found_items.find({}))

    matches = []

    for lost in lost_items:
        lost_id = str(lost["_id"])
        lost_item = lost.get("item", "").strip().lower()
        lost_location = lost.get("location", "").strip().lower()
        lost_date = lost.get("date", "")
        lost_contact = lost.get("email", "")  # Get user email
        lost_image = lost.get("image_url", "")  # Get lost item image

        for found in found_items:
            found_id = str(found["_id"])
            found_item = found.get("item", "").strip().lower()
            found_location = found.get("location", "").strip().lower()
            found_date = found.get("date", "")
            found_contact = found.get("email", "")  # Get finder email
            found_image = found.get("image_url", "")  # Get found item image

            item_match = fuzz.ratio(lost_item, found_item) > 40
            location_match = fuzz.partial_ratio(lost_location, found_location) > 50
            date_match = abs(int(found_date.replace("-", "")) - int(lost_date.replace("-", ""))) <= 1

            if item_match and location_match and date_match:
                match_data = {
                    "lost_item": {
                        "id": lost_id,
                        "item": lost["item"],
                        "location": lost["location"],
                        "date": lost["date"],
                        "contact": lost_contact,
                        "image_url": lost_image
                    },
                    "found_item": {
                        "id": found_id,
                        "item": found["item"],
                        "location": found["location"],
                        "date": found["date"],
                        "contact": found_contact,
                        "image_url": found_image
                    }
                }
                matches.append(match_data)

                # Update lost item with found_item_id for reference
                db.lost_items.update_one({"_id": lost_id}, {"$set": {"matched_found_item": found_id}})

                # Send Notification Email
                if lost_contact:
                    send_email(lost_contact, lost, found)
                else:
                    print('No contact email found!')

    return jsonify({"matches": matches}), 200
