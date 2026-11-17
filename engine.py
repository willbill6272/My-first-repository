import random
from save_system import save_game

available_items = {
    1: {"name": "Health Potion", "price": 15, "description": "Restores health in a pinch."},
    2: {"name": "Mysterious Necklace", "price": 50, "description": "A mysterious man offers you a simple chain necklace."},
}

def pickup(state, itempickup):
    for slot in state["inventory"]:
        if state["inventory"][slot] == "empty":
            state["inventory"][slot] = itempickup
            print(f"Added {itempickup} to {slot}!")
            return
    print("Inventory is full!")

def market(state):
    print("\n=== 🛒 WELCOME TO THE MARKETPLACE ===")
    print("Here you can buy items using your gold!")
    for item_key, data in available_items.items():
        print(f"[{item_key}] {data['name']} - 💰 {data['price']}g")
        print(f"    \"{data['description']}\"")
    print("=====================================")
    
    choice = input("Enter the number of the item you want to buy (or press Enter to exit): ")
    
    if choice == "1":
        if state["goldcount"] >= 15:
            state["goldcount"] -= 15
            pickup(state, "potion")
            print("🎉 Purchased Health Potion!")
        else:
            print("❌ You don't have enough gold!")
    elif choice == "2":
        if state["goldcount"] >= 50:
            state["goldcount"] -= 50
            pickup(state, "necklace")
            print("🎉 Purchased Mysterious Necklace!")
        else:
            print("❌ You don't have enough gold!")
    else:
        print("Leaving the marketplace...")

def run_game(state):
    playeralive = True
    
    while playeralive:
        longtext = f"""\nattack? (spear, sword, bow, nunchucks),
or type "market" to shop, "save", "quit",
Inventory: {state['inventory']}
Weapons: {state['weapon_unlocks']}
Gold: {state['goldcount']}g: """

        X = input(longtext).strip().lower()
        
        if X == "nunchuck":
            X = "nunchucks"
            
        if X == "spear":
            if not state["weapon_unlocks"].get("spear", False):
                print("🔒 You haven't unlocked the spear yet!")
                continue
                
            damage = round(random.triangular(1, 5, 3))
            state["monsterhealth"] -= damage
            
            if damage == 5:
                print("💥 CRITICAL HIT: 5 max damage!")
            else:
                print(f"You hit the monster for {damage} damage! Monster HP: {state['monsterhealth']}")
                
        elif X == "yes" or X == "":
            continue
            
        elif X == "nunchucks":
            if not state["weapon_unlocks"].get("nunchucks", False):
                print("🔒 You haven't unlocked the nunchucks yet!")
                continue
                
            state["monsterhealth"] -= 1
            print("🥷 You flail the nunchucks around and graze the monster for 1 damage!")
            print(f"Monster HP: {state['monsterhealth']}")
            
        elif X == "sword":
            if not state["weapon_unlocks"].get("sword", False):
                print("🔒 You haven't unlocked the sword yet!")
                continue
                
            damage = round(random.triangular(1, 10, 7))
            if damage == 10:
                state["monsterhealth"] -= damage
                print("💥 CRITICAL HIT: 10 max damage! Monster HP:", state["monsterhealth"])
            elif damage > 3:
                state["monsterhealth"] -= damage
                print(f"You hit the monster for {damage} damage! Monster HP: {state['monsterhealth']}")
            else:
                print(f"You rolled a {damage}... It bounced right off the monster's armor!")
                
        elif X == "market":
            market(state)
            continue
            
        elif X == "save":
            save_game(state)
            continue
            
        elif X == "no":
            print("You fled the battle!")
            break
            
        elif X == "bow":
            if not state["weapon_unlocks"].get("bow", False):
                print("🔒 You haven't unlocked the bow yet!")
                continue
                
            bow_roll = random.randint(1, 10)
            if bow_roll == 1:
                self_damage = random.randint(10, 15)
                state["playerhealth"] -= self_damage
                print(f"🏹 You hit yourself for {self_damage} damage! Your HP: {state['playerhealth']}")
                if state["playerhealth"] <= 0:
                    print("\n💀 GAME OVER! You killed yourself.")
                    playeralive = False
                continue
            elif 2 <= bow_roll <= 5:
                print("🏹 Your arrow missed completely!")
                continue
            else:
                damage = random.randint(10, 15)
                state["monsterhealth"] -= damage
                print(f"💥 DIRECT HIT for {damage} damage! Monster HP: {state['monsterhealth']}")
                
        elif X == "quit" or X == "exit":
            if input("Are you sure you want to quit? (yes/no): ").strip().lower() == "yes":
                print("Thanks for playing!")
                break
            else:
                continue
        else:
            print("Invalid input!")
            continue

        # Check if monster died
        if state["monsterhealth"] <= 0:
            print("\n🏆 VICTORY! You slaughtered the beast!")
            pickup(state, "potion")
            state["weapon_unlocks"]["spear"] = True
            state["goldcount"] += 10
            print("💰 You found 10 gold pieces!")
            save_game(state)
            break

        # Monster Counter-Attack
        mdamage = round(random.triangular(1, 10, 5))
        state["playerhealth"] -= mdamage
        print(f"The monster hits you for {mdamage} damage. Your HP: {state['playerhealth']}")

        if state["playerhealth"] <= 0:
            print("\n💀 GAME OVER! You perished.")
            playeralive = False
            break