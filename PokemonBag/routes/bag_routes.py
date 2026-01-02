# Description:
# This file implements a Flask Blueprint that exposes REST API endpoints
# for the Pokémon Bag feature.
#
# It provides:
# - Available bag categories (Items, Poké Balls, Key Items)
# - Item lists filtered by category
# - Individual item details (name, description, icon)
# - A complete icon mapping for frontend consumption
#
# The routes aggregate data from item description dictionaries and
# icon mappings, returning structured JSON responses intended for
# frontend or game UI integration.



from flask import Blueprint, jsonify

from data.items import pokemonItems, keyItems, pokeBalls
from data.item_icons import itemIcons

bag_bp = Blueprint("bag", __name__, url_prefix="/api/bag")

# ---------------- CATEGORIES ----------------
@bag_bp.route("/categories", methods=["GET"])
def get_categories():
    return jsonify([
        "Items",
        "Balls",
        "Key Items"
    ])


# ---------------- ITEMS BY CATEGORY ----------------
@bag_bp.route("/items/<category>", methods=["GET"])
def get_items_by_category(category):
    category_map = {
        "Items": pokemonItems,
        "Balls": pokeBalls,
        "Key Items": keyItems
    }

    if category not in category_map:
        return jsonify({"error": "Invalid category"}), 404

    items = []
    for name, description in category_map[category].items():
        items.append({
            "name": name,
            "description": description,
            "icon": itemIcons.get(name)
        })

    return jsonify(items)


# ---------------- SINGLE ITEM ----------------
@bag_bp.route("/item/<item_name>", methods=["GET"])
def get_single_item(item_name):
    all_items = {
        **pokemonItems,
        **pokeBalls,
        **keyItems
    }

    if item_name not in all_items:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({
        "name": item_name,
        "description": all_items[item_name],
        "icon": itemIcons.get(item_name)
    })


# ---------------- ICON MAP ----------------
@bag_bp.route("/icons", methods=["GET"])
def get_icon_map():
    return jsonify(itemIcons)
