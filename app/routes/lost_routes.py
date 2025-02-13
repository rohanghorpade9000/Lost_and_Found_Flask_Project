from flask import Blueprint, request, jsonify
from app.config import db
from bson import ObjectId
from app.jwt_token import token_required
from app.services.image_service import upload_image


lost_bp = Blueprint("lost", __name__)

#To report a lost item
@lost_bp.route("/lost-items/", methods=["POST"])
@token_required
def store_data():
    """API to report a lost item (only for authenticated users)"""
    data = request.json

    # Ensure required fields are provided (excluding email, as it's taken from token)
    required_fields = ["item", "location", "date"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Attach logged-in user's email from the token
    data["email"] = request.user_email
    data["_id"] = str(ObjectId())  # Generate unique ID
    data["claimed"] = False  # Mark as unclaimed by default

    db.lost_items.insert_one(data)  # Store in MongoDB

    return jsonify({"message": "Lost item reported successfully", "id": data["_id"]}), 201


#To display all lost items
@lost_bp.route("/lost-items/", methods=["GET"])
@token_required
def get_lost_items():
    """Retrieve all lost items (only for authenticated users)"""

    print("Token Verified! User:", request.user_email)  # Debugging

    data_list = list(db.lost_items.find({}))
    for data in data_list:
        data["id"] = str(data.pop("_id"))

    return jsonify({"data": data_list}), 200


#To delete a lost item
@lost_bp.route("/lost-items/<id>", methods=["DELETE"])
@token_required
def delete_item(id):
    """Delete a lost item (only by the owner)"""

    # Find item
    lost_item = db.lost_items.find_one({"_id": id})

    if not lost_item:
        return jsonify({"error": "Item not found"}), 404

    # Check if the logged-in user is the owner
    if lost_item["email"] != request.user_email:
        return jsonify({"error": "Unauthorized. You can only delete your own items."}), 403

    # Delete item
    db.lost_items.delete_one({"_id": id})
    return jsonify({"message": "Item deleted successfully"}), 200


# To upload image of lost item
@lost_bp.route("/lost-items/upload-image", methods=["POST"])
@token_required
def upload_lost_item_image():
    """Upload an image for a lost item (only by the owner)"""

    # Check if 'id' and 'image' are provided
    lost_item_id = request.form.get("id")
    image_file = request.files.get("image")

    if not lost_item_id or not image_file:
        return jsonify({"error": "Both 'id' and 'image' are required."}), 400

    # Find item
    lost_item = db.lost_items.find_one({"_id": lost_item_id})

    if not lost_item:
        return jsonify({"error": "Item not found"}), 404

    # Check if the logged-in user is the owner
    if lost_item["email"] != request.user_email:
        return jsonify({"error": "Unauthorized. You can only upload images for your own items."}), 403

    # Upload image to Cloudinary
    image_url = upload_image(image_file)

    # Update lost item in MongoDB with the image URL
    db.lost_items.update_one({"_id": lost_item_id}, {"$set": {"image_url": image_url}})

    return jsonify({"message": "Image uploaded successfully", "image_url": image_url}), 200


#To get history of lost items
@lost_bp.route("/lost-items/history", methods=["GET"])
@token_required
def get_lost_items_history():
    """Retrieve all lost items reported by the logged-in user"""

    # Fetch lost items only for the logged-in user
    user_lost_items = list(db.lost_items.find({"email": request.user_email}))

    for item in user_lost_items:
        item["id"] = str(item.pop("_id"))  # Convert ObjectId to string

    return jsonify({"lost_items": user_lost_items}), 200

