import json

def load_game():
    try:
        with open("player.json", "r") as file:
            loaded_data = json.load(file)
            print("📂 Game loaded successfully from JSON!")
            return loaded_data
    except (FileNotFoundError, json.JSONDecodeError):
        print("No save file found. Starting a fresh game!")
        return {
            "playerhealth": 50,
            "monsterhealth": 25,
            "goldcount": 0,
            "inventory": {
                "item1": "empty",
                "item2": "empty",
                "item3": "empty",
                "item4": "empty",
                "item5": "empty",
            },
            "weapon_unlocks": {
                "sword": True,
                "spear": False,
                "bow": False,
                "nunchucks": True,
            }
        }

def save_game(game_state):
    with open("player.json", "w") as file:
        json.dump(game_state, file, indent=4)
    print("💾 Game saved successfully to JSON!")