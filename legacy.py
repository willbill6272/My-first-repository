import random
import pickle

# --- SAVE / LOAD INITIALIZATION ---
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

playeralive = True
monsteralive = True

# --- MARKETPLACE DATA ---
available_items = {
    1: {
        "name": "Health Potion",
        "price": 15,
        "description": "Restores health in a pinch."
    },
    2: {
        "name": "Mysterious Necklace",
        "price": 50,
        "description": "A mysterious man offers you a simple chain necklace."
    },
}

# --- FUNCTIONS ---
def pickup(itempickup):
    for slot in inventory:
        if inventory[slot] == "empty":
            inventory[slot] = itempickup
            print(f"Added {itempickup} to {slot}!")
            return
    print("Inventory is full!")

def market():
    global goldcount
    print("\n=== 🛒 WELCOME TO THE MARKETPLACE ===")
    print("Here you can buy items using your gold!")
    for item_key, data in available_items.items():
        print(f"[{item_key}] {data['name']} - 💰 {data['price']}g")
        print(f"    \"{data['description']}\"")
    print("=====================================")
    
    choice = input("Enter the number of the item you want to buy (or press Enter to exit): ")
    
    if choice == "1":
        if goldcount >= 15:
            goldcount -= 15
            pickup("potion")
            print("🎉 Purchased Health Potion!")
        else:
            print("❌ You don't have enough gold!")
    elif choice == "2":
        if goldcount >= 50:
            goldcount -= 50
            pickup("necklace")
            print("🎉 Purchased Mysterious Necklace!")
        else:
            print("❌ You don't have enough gold!")
    else:
        print("Leaving the marketplace...")

# --- MAIN GAME LOOP ---
while playeralive:
    # Update save_data inside the loop
    save_data = {
        "playerhealth": playerhealth,
        "monsterhealth": monsterhealth,
        "inventory": inventory,
        "weapon_unlocks": weapon_unlocks,
        "goldcount": goldcount
    }
    
    longtext = f"""\nattack? (spear, sword, bow, nunchucks),
or type "market" to shop, "save", "quit",
Inventory: {inventory}
Weapons: {weapon_unlocks}
Gold: {goldcount}g: """

    X = input(longtext).strip().lower()
    
    if X == "nunchuck":
        X = "nunchucks"
        
    if X == "spear":
        if not weapon_unlocks.get("spear", False):
            print("🔒 You haven't unlocked the spear yet!")
            continue
            
        damage = round(random.triangular(1, 5, 3))
        monsterhealth = monsterhealth - damage
        
        if damage == 5:
            print("💥 CRITICAL HIT: 5 max damage!")
        else:
            print(f"You hit the monster for {damage} damage! Monster HP: {monsterhealth}")
            
    elif X == "yes" or X == "":
        continue
        
    elif X == "nunchucks":
        if not weapon_unlocks.get("nunchucks", False):
            print("🔒 You haven't unlocked the nunchucks yet!")
            continue
            
        damage = 1
        monsterhealth -= damage
        print("🥷 You flail the nunchucks around, almost hitting yourself, and graze the monster for 1 damage!")
        print(f"Monster HP: {monsterhealth}")
        
    elif X == "sword":
        if not weapon_unlocks.get("sword", False):
            print("🔒 You haven't unlocked the sword yet!")
            continue
            
        damage = round(random.triangular(1, 10, 7))
        if damage == 10:
            monsterhealth = monsterhealth - damage
            print("💥 CRITICAL HIT: 10 max damage! Monster HP:", monsterhealth)
        elif damage > 3:
            monsterhealth = monsterhealth - damage
            print(f"You hit the monster for {damage} damage! Monster HP: {monsterhealth}")
        else:
            print(f"You rolled a {damage}... It bounced right off the monster's armor! Failed to hit.")
            
    elif X == "market":
        market()
        continue
        
    elif X == "save":
        with open("savegame.pkl", "wb") as file:
            pickle.dump(save_data, file)
        print("💾 Game saved successfully!")
        continue
        
    elif X == "no":
        print("You fled the battle!")
        break
        
    elif X == "bow":
        if not weapon_unlocks.get("bow", False):
            print("🔒 You haven't unlocked the bow yet!")
            continue
            
        bow_roll = random.randint(1, 10)
        
        if bow_roll == 1:
            self_damage = random.randint(10, 15)
            playerhealth -= self_damage
            print(f"🏹 You forgot how bows work and hit yourself for {self_damage} damage! Your HP: {playerhealth}")
            
            if playerhealth <= 0:
                print("\n💀 GAME OVER! You accidentally killed yourself in the dungeon.")
                playeralive = False
                break
            continue
            
        elif 2 <= bow_roll <= 5:
            print("🏹 Your arrow flew wide and missed the monster completely!")
            continue
            
        else:
            damage = random.randint(10, 15)
            monsterhealth -= damage
            print(f"💥 DIRECT HIT! The arrow pierces the beast for {damage} damage! Monster HP: {monsterhealth}")
            
    elif X == "quit" or X == "exit":
        confirm = input("Are you sure you want to quit? (yes/no): ").strip().lower()
        if confirm == "yes":
            print("Thanks for playing! See you next time.")
            playeralive = False
            break
        else:
            continue
    else:
        print("Invalid input! You fumbled your weapon.")
        continue

    # Check if monster died
    if monsterhealth <= 0:
        print("\n🏆 VICTORY! You slaughtered the beast!")
        monsteralive = False
        pickup("potion")
        weapon_unlocks["spear"] = True
        goldcount += 10
        print("💰 You found 10 gold pieces on the beast!")
        
        # Auto-save victory progress so you don't lose the gold/spear unlock
        with open("savegame.pkl", "wb") as file:
            pickle.dump(save_data, file)
        print("💾 Victory progress saved automatically!")
        break

    # Monster's Counter-Attack
    mdamage = round(random.triangular(1, 10, 5))
    playerhealth = playerhealth - mdamage
    
    if mdamage == 10:
        print(f"🚨 DEVASTATING ATTACK: 10 damage! Your HP: {playerhealth}")
    elif mdamage >= 8:
        print(f"⚠️ The monster lashes out with a heavy blow for {mdamage} damage! Your HP: {playerhealth}")
    else:
        print(f"The monster hits you for {mdamage} damage. Your HP: {playerhealth}")

    # Check if the player died
    if playerhealth <= 0:
        print("\n💀 GAME OVER! You perished in the dungeon.")
        playeralive = False
        break

print("\nFinal Inventory:", inventory)
print("Final Gold Count:", goldcount)
