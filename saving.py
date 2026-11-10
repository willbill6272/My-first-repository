import pickle
def save():
    try:
        with open("savegame.pkl", "rb") as file:
            loaded_data = pickle.load(file)
            
        playerhealth = loaded_data["playerhealth"]
        monsterhealth = loaded_data["monsterhealth"]
        inventory = loaded_data["inventory"]
        weapon_unlocks = loaded_data["weapon_unlocks"]
        goldcount = loaded_data["goldcount"]
        print("📂 Game loaded successfully!")
        
    except (FileNotFoundError, KeyError):
        print("No save file found. Starting a fresh game!")
        inventory = {
            "item1": "empty",
            "item2": "empty",
            "item3": "empty",
            "item4": "empty",
            "item5": "empty",
        }
        # Default weapon unlocks for a fresh game
        weapon_unlocks = {
            "sword": True,
            "spear": False,
            "bow": False,
            "nunchucks": True,
        }
        playerhealth = 50
        monsterhealth = 25
        goldcount = 0