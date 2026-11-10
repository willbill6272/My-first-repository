import random
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


print("\nFinal Inventory:", inventory)
print("Final Gold Count:", goldcount)