# data/items.py
# Responsible for providing static item descriptions used across the app.
#
# What it contains:
# - Top-level Python dictionaries mapping item display names (str) to
#   human-readable description strings (str). Provided dictionaries include
#   `pokemonItems`, `keyItems`, and `pokeBalls`.
#
# Intended use:
# - Import this module and read the appropriate dictionary to obtain an
#   item's description for rendering in templates, APIs, or UI components.
#   Example: from data import items; items.pokemonItems["Potion"]
#
# Notes:
# - This file is static content (not a database). Update these dictionaries
#   when adding or changing items and keep icon mappings in sync with
#   `data/item_icons.py`.

pokemonItems = {
    "Potion": "A spray-type medicine for treating wounds. It restores the HP of one Pokémon by 20 points.",
    "Super Potion": "A spray-type medicine for treating wounds. It restores the HP of one Pokémon by 50 points.",
    "Hyper Potion": "A spray-type medicine for treating wounds. It restores the HP of one Pokémon by 200 points.",

    "Antidote": "A spray-type medicine. It cures a Pokémon of poisoning.",
    "Paralyze Heal": "A spray-type medicine. It cures a Pokémon of paralysis.",
    "Burn Heal": "A spray-type medicine. It heals a Pokémon of a burn.",

    "Full Heal": "A medicine that cures all status problems of one Pokémon.",
    "Full Restore": "A medicine that fully restores the HP and heals any status problem of one Pokémon.",

    "Revive": "A medicine that revives a fainted Pokémon. It restores half the Pokémon’s HP.",
    "Max Revive": "A medicine that revives a fainted Pokémon. It fully restores the Pokémon’s HP.",

    "Repel": "An item that prevents weak wild Pokémon from appearing for 100 steps.",
    "Super Repel": "An item that prevents weak wild Pokémon from appearing for 200 steps.",
    "Max Repel": "An item that prevents weak wild Pokémon from appearing for 250 steps.",

    "Escape Rope": "A long, durable rope. Use it to escape instantly from a cave or dungeon.",

    "X Attack": "An item that raises the Attack stat of a Pokémon in battle.",
    "X Defense": "An item that raises the Defense stat of a Pokémon in battle.",
    "X Speed": "An item that raises the Speed stat of a Pokémon in battle.",
    "X Special": "An item that raises the Special Attack and Special Defense of a Pokémon in battle."
}



keyItems = {
    "Bicycle": "A folding Bike that enables much faster movement than the Running Shoes.",

    "Town Map": "A very convenient map that can be viewed anytime. It even shows your present location.",

    "VS Seeker": "A device that searches for trainers who want to rematch.",

    "Itemfinder": "A device that signals when there is a hidden item nearby.",

    "Poké Flute": "A flute that awakens Pokémon from sleep.",

    "Silph Scope": "A scope that makes unseeable Pokémon visible.",

    "Lift Key": "A Key that operates the elevator in Team Rocket’s Hideout.",

    "Card Key": "A card-type Key that opens doors in the Silph Co. building.",

    "Coin Case": "A case for holding Coins obtained at the Game Corner.",

    "Fame Checker": "A device that stores information on famous people encountered during your adventure."
}



pokeBalls = {
    "Poke Ball": "A device for catching wild Pokémon. It is thrown like a ball at the target.",

    "Great Ball": "A good, high-performance Ball that provides a higher Pokémon catch rate than a standard Poké Ball.",

    "Ultra Ball": "An ultra-high-performance Ball that provides a higher Pokémon catch rate than a Great Ball.",

    "Master Ball": "The best Ball. It will catch any wild Pokémon without fail.",

    "Safari Ball": "A special Ball that is used only in the Safari Zone."
}