from flask import Blueprint, request, jsonify
from app.config import db
from app.jwt_token import token_required
from bson import ObjectId
from app.services.image_service import upload_image

found_bp = Blueprint("found", __name__)


# To report found items
@found_bp.route("/found-items/", methods=["POST"])
@token_required
def report_found_item():
    """API to report a found item"""
    data = request.json

    # Ensure required fields are provided
    required_fields = ["item", "location", "date"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Attach logged-in user's email from the token
    data["email"] = request.user_email
    data["_id"] = str(ObjectId())  # Generate unique ID
    data["claimed"] = False  # Mark as unclaimed by default

    db.found_items.insert_one(data)  # Store in MongoDB

    return jsonify({"message": "Found item reported successfully", "id": data["_id"]}), 201


# To display Found items
@found_bp.route("/found-items/", methods=["GET"])
@token_required
def fetch_found_items():
    """Retrieve all found items"""
    data_list = list(db.found_items.find({}))
    for data in data_list:
        data["id"] = str(data.pop("_id"))  # Convert ObjectId to string
    return jsonify({"data": data_list}), 200


# To Delete Found Items
@found_bp.route("/found-items/<id>", methods=["DELETE"])
@token_required
def delete_found_item(id):
    """Delete a found item (only by the owner)"""
    print('Delete found item endpoint is called successfully !')

    # Find item
    found_item = db.found_items.find_one({"_id": id})

    if not found_item:
        return jsonify({"error": "Item not found"}), 404

    # Check if the logged-in user is the owner
    if found_item["email"] != request.user_email:
        return jsonify({"error": "Unauthorized. You can only delete your own items."}), 403

    # Delete item
    db.found_items.delete_one({"_id": id})
    return jsonify({"message": "Item deleted successfully"}), 200


# To claim items
@found_bp.route("/found-items/claim/<id>", methods=["PUT"])
@token_required
def claim_found_item(id):
    """API to claim a found item"""

    # Print debug info
    print(f"Searching for item with ID: {id}")

    # Search using string ID
    found_item = db.found_items.find_one({"_id": str(id)})

    if not found_item:
        print("Item not found!")
        return jsonify({"error": "Item not found."}), 404

    if found_item.get("claimed", False):
        return jsonify({"error": "This item has already been claimed."}), 400

    # Ensure only the reported owner can claim the item
    if found_item["email"] != request.user_email:
        return jsonify({"error": "Unauthorized. You can only claim items reported by you."}), 403

    # Run update and capture result
    update_result = db.found_items.update_one({"_id": str(id)}, {"$set": {"claimed": True}})

    # Print MongoDB update result
    print(f"Update Acknowledged: {update_result.acknowledged}")
    print(f"Matched {update_result.matched_count} documents, Modified {update_result.modified_count} documents")

    if update_result.modified_count == 0:
        return jsonify({"error": "Failed to claim item, no changes made."}), 500

    print(f"Item {id} successfully claimed!")

    return jsonify({"message": "Item successfully claimed."}), 200


# To view Specific Product
@found_bp.route("/found-items/view/<id>", methods=["GET"])
@token_required
def view_found_item(id):
    """API to view a found item by ID (for debugging)"""

    # Fetch all found items and print them for debugging
    all_items = list(db.found_items.find({}))
    print("All Found Items in DB:")
    for item in all_items:
        print(f"Stored ID: {item['_id']} | Type: {type(item['_id'])}")

    # Ensure _id is compared as a string
    found_item = db.found_items.find_one({"_id": str(id)})  # Explicitly cast id to string

    if not found_item:
        print(f"No match found for ID: {id}")  # Debugging output
        return jsonify({"error": "Item not found."}), 404

    print(f"Found Item: {found_item}")  # Debugging output
    return jsonify(found_item), 200


# To Upload Images
@found_bp.route("/found-items/upload-image", methods=["POST"])
@token_required
def upload_found_item_image():
    """API to upload an image for a found item and update the database"""

    # Check if 'id' and 'image' are provided
    found_item_id = request.form.get("id")
    image_file = request.files.get("image")

    if not found_item_id or not image_file:
        return jsonify({"error": "Both 'id' and 'image' are required."}), 400

    # Find item
    found_item = db.found_items.find_one({"_id": found_item_id})

    if not found_item:
        return jsonify({"error": "Item not found"}), 404

    # Check if the logged-in user is the owner
    if found_item["email"] != request.user_email:
        return jsonify({"error": "Unauthorized. You can only upload images for your own items."}), 403

    # Upload image to Cloudinary
    image_url = upload_image(image_file)

    # Update found item in MongoDB with the image URL
    db.found_items.update_one({"_id": found_item_id}, {"$set": {"image_url": image_url}})

    return jsonify({"message": "Image uploaded successfully", "image_url": image_url}), 200
