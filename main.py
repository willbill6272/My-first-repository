import random
import pickle

# Try to open the save file and load the data back into your variables
try:
    with open("savegame.pkl", "rb") as file:
        loaded_data = pickle.load(file)
        
    playerhealth = loaded_data["playerhealth"]
    monsterhealth = loaded_data["monsterhealth"]
    inventory = loaded_data["inventory"]
    weapon_unlocks = loaded_data["weapon_unlocks"] # Load saved weapon unlocks
    goldcount = loaded_data["goldcount"] # 🛠️ Fixed: Extracts the specific gold value safely
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
    # Default weapon unlocks for a fresh game (Sword & Nunchucks unlocked, Spear & Bow locked)
    weapon_unlocks = {
        "sword": True,
        "spear": False,
        "bow": False,
        "nunchucks": True, # Pluralized to match your input checks
    }
    playerhealth = 50
    monsterhealth = 25
    goldcount = 0

playeralive = True
monsteralive = True

def pickup(itempickup):
    for slot in inventory:
        if inventory[slot] == "empty":
            inventory[slot] = itempickup
            print(f"Added {itempickup} to {slot}!")
            return # Stops running once it finds the first empty slot
    print("Inventory is full!")

while playeralive:
    # Update save_data inside the loop so it captures current stats, unlocks, and gold
    save_data = {
        "playerhealth": playerhealth,
        "monsterhealth": monsterhealth,
        "inventory": inventory,
        "weapon_unlocks": weapon_unlocks,
        "goldcount": goldcount # 🛠️ Added: Gold is now tracked in save data packets
    }
    
    longtext = f"""\nattack? (spear, sword, bow, nunchucks),
or you can use an item if you have any, you have:
Inventory: {inventory}
Weapons: {weapon_unlocks}
Gold: {goldcount}g
or type "save" or "quit": """

    X = input(longtext)
    
    if X == "nunchuck":
        X = "nunchucks"
        
    if X == "spear":
        # Check if the weapon is unlocked before allowing use
        if not weapon_unlocks.get("spear", False):
            print("🔒 You haven't unlocked the spear yet!")
            continue
            
        damage = round(random.triangular(1, 5, 3))
        monsterhealth = monsterhealth - damage
        
        # Check for the critical hit FIRST
        if damage == 5:
            print("💥 CRITICAL HIT: 5 max damage!")
        else:
            print(f"You hit the monster for {damage} damage! Monster HP: {monsterhealth}")
            
    elif X == "yes" or X == " ":
        continue
        
    elif X == "nunchucks":
        # Check if the weapon is unlocked before allowing use
        if not weapon_unlocks.get("nunchucks", False):
            print("🔒 You haven't unlocked the nunchucks yet!")
            continue
            
        damage = 1
        monsterhealth -= damage
        print("🥷 You flail the nunchucks around, almost hitting yourself, and graze the monster for 1 damage!")
        print(f"Monster HP: {monsterhealth}")
        
    elif X == "sword":
        # Check if the weapon is unlocked before allowing use
        if not weapon_unlocks.get("sword", False):
            print("🔒 You haven't unlocked the sword yet!")
            continue
            
        damage = round(random.triangular(1, 10, 7))
        # Check for max damage or armor misses before normal hits!
        if damage == 10:
            monsterhealth = monsterhealth - damage
            print("💥 CRITICAL HIT: 10 max damage! Monster HP:", monsterhealth)
        elif damage > 3:
            monsterhealth = monsterhealth - damage
            print(f"You hit the monster for {damage} damage! Monster HP: {monsterhealth}")
        else:
            # Handles rolls of 1, 2, and 3 (the armor miss mechanic)
            print(f"You rolled a {damage}... It bounced right off the monster's armor! Failed to hit.")
            
    elif X == "save":
        with open("savegame.pkl", "wb") as file:
            pickle.dump(save_data, file)
        print("💾 Game saved successfully!")
        continue
        
    elif X == "no":
        print("You fled the battle!")
        break
        
    elif X == "bow":
        # Check if the weapon is unlocked before allowing use
        if not weapon_unlocks.get("bow", False):
            print("🔒 You haven't unlocked the bow yet!")
            continue
            
        bow_roll = random.randint(1, 10)
        
        if bow_roll == 1:
            # 10% Chance: Bow snaps or arrow backfires!
            self_damage = random.randint(10, 15)
            playerhealth -= self_damage
            print(f"🏹 You forgot how bows work and hit yourself for {self_damage} damage! Your HP: {playerhealth}")
            
            # Check if the backfire killed you on the spot!
            if playerhealth <= 0:
                print("\n💀 GAME OVER! You accidentally killed yourself in the dungeon.")
                playeralive = False
                break
            continue # 🚀 Jumps back to input, skipping the monster's attack!
            
        elif bow_roll >= 2 and bow_roll <= 5:
            print("🏹 Your arrow flew wide and missed the monster completely!")
            continue # 🚀 Skips the monster's turn and lets you try again!
            
        else:
            # 50% Chance (Rolls 6-10): Extreme flat damage
            damage = random.randint(10, 15)
            monsterhealth -= damage
            print(f"💥 DIRECT HIT! The arrow pierces the beast for {damage} damage! Monster HP: {monsterhealth}")
            
    elif X == "quit" or X == "exit":
        confirm = input("Are you sure you want to quit? (yes/no): ")
        if confirm == "yes":
            print("Thanks for playing! See you next time.")
            playeralive = False
            break
        else:
            continue
    else:
        print("Invalid input! You fumbled your weapon.")
        continue

    # Check if monster died before it gets to strike back
    if monsterhealth <= 0:
        print("\n🏆 VICTORY! You slaughtered the beast!")
        monsteralive = False
        pickup("potion")
        weapon_unlocks["spear"] = True
        goldcount += 10 # 💰 Bonus reward: finding gold when slaying the monster!
        print("💰 You found 10 gold pieces on the beast!")
        break

    # Monster's Counter-Attack
    mdamage = round(random.triangular(1, 10, 5))
    playerhealth = playerhealth - mdamage
    
    # Monster special dialog logic (Highest damage checked first!)
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

print("Final Inventory:", inventory)
print("Final Gold Count:", goldcount)
