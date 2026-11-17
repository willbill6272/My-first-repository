import pickle

def load_game():
    try:
        with open("savegame.pkl", "rb") as file:
            loaded_data = pickle.load(file)
            print("📂 Game loaded successfully!")
            return loaded_data
    except (FileNotFoundError, KeyError):
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
    with open("savegame.pkl", "wb") as file:
        pickle.dump(game_state, file)
    print("💾 Game saved successfully!")