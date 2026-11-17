from save_system import load_game
from engine import run_game

if __name__ == "__main__":
    print("🎮 Starting Modular Dungeon Crawler...")
    game_state = load_game()
    run_game(game_state)
    print("\nFinal Inventory:", game_state["inventory"])
    print("Final Gold Count:", game_state["goldcount"])
    