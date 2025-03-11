import random
import tkinter as tk
from tkinter import font

# Global variables
inventory = []
discovered_rooms = set()
password_numbers = [random.randint(0, 9) for _ in range(4)]  # Generates a 4-digit code
steps_remaining = 12  # Step counter

# Create the main window
root = tk.Tk()
root.title("Escape Room Game")
root.geometry("500x500")
root.configure(bg="#282c34")  # Dark background for modern look

# Define fonts
btn_font = font.Font(family="Helvetica", size=10, weight="bold")
text_font = font.Font(family="Arial", size=12)

# Create text area to display game messages
game_text = tk.Text(
    root, height=8, width=55, wrap="word", bg="#abb2bf", fg="black", font=text_font
)
game_text.pack(pady=10)

# Create label to display steps remaining
steps_label = tk.Label(
    root,
    text=f"Steps remaining: {steps_remaining}",
    bg="#282c34",
    fg="white",
    font=text_font,
)
steps_label.pack(pady=5)

# Frame for main action buttons
btn_frame = tk.Frame(root, bg="#282c34")
btn_frame.pack(side=tk.LEFT, padx=10, pady=5)

# Frame for exploration buttons
explore_frame = tk.Frame(root, bg="#282c34")
explore_frame.pack(side=tk.LEFT, padx=10, pady=5)


# Function to update game text
def update_text(message):
    game_text.delete("1.0", tk.END)
    game_text.insert("1.0", message)


# Function to update steps label
def update_steps_label():
    steps_label.config(text=f"Steps remaining: {steps_remaining}")


# Function to check inventory
def check_inventory():
    update_text(
        f"Your inventory: {', '.join(inventory)}"
        if inventory
        else "Your inventory is empty."
    )


# Function to clear explore buttons
def clear_explore_buttons():
    for widget in explore_frame.winfo_children():
        widget.destroy()


# Function to decrement steps and check if game is over
def decrement_steps():
    global steps_remaining
    steps_remaining -= 1
    update_steps_label()
    if steps_remaining <= 0:
        update_text("He got you! You took too long.")


# Room functions
def enter_room_0():
    decrement_steps()
    clear_explore_buttons()
    if "flashlight" in inventory:
        update_text(
            "You see a bed covered with a sheet. What do you want to explore?\n1. Look under the bed\n2. Inspect the walls\n3. Check the floor"
        )
        create_explore_buttons(
            ["Bed", "Walls", "Floor"], [explore_bed, explore_walls, explore_floor]
        )
    else:
        update_text("It's too dark to see anything. You need a flashlight.")


def explore_bed():
    if "flashlight" in inventory:
        update_text("Congratulations! You found him under the bed!")
    else:
        update_text("A monster jumps out and... GAME OVER!")


def explore_walls():
    decrement_steps()
    update_text("You see scratch marks but nothing useful.")


def explore_floor():
    decrement_steps()
    update_text("The floor creaks, but nothing happens.")


def enter_room_1():
    decrement_steps()
    clear_explore_buttons()
    update_text(
        "You are in a storage room. What do you want to check?\n1. Shelf 1\n2. Shelf 2\n3. Shelf 3"
    )
    create_explore_buttons(
        ["Shelf 1", "Shelf 2", "Shelf 3"], [shelf_1, shelf_2, shelf_3]
    )


def shelf_1():
    decrement_steps()
    update_text("This shelf is empty.")


def shelf_2():
    decrement_steps()
    if "flashlight" not in inventory:
        inventory.append("flashlight")
        update_text("You found a flashlight.")
    else:
        update_text("You already have a flashlight.")


def shelf_3():
    decrement_steps()
    if "key_6" not in inventory:
        inventory.append("key_6")
        update_text("You found a key labeled '6'.")
    else:
        update_text("You already have this key.")


def enter_room_2():
    decrement_steps()
    clear_explore_buttons()
    if "fire_extinguisher" in inventory:
        update_text(
            f"You extinguish the fire and find a number: {password_numbers[0]}XXX"
        )
    else:
        update_text("The room is on fire! You need a fire extinguisher to proceed.")


def enter_room_3():
    decrement_steps()
    clear_explore_buttons()
    update_text(
        "You enter a room with a bed, a table, and a wardrobe. What do you want to check?\n1. Bed\n2. Table\n3. Wardrobe"
    )
    create_explore_buttons(
        ["Bed", "Table", "Wardrobe"], [find_extinguisher, check_table, check_wardrobe]
    )


def find_extinguisher():
    decrement_steps()
    if "fire_extinguisher" not in inventory:
        inventory.append("fire_extinguisher")
        update_text("You found a fire extinguisher under the bed!")
    else:
        update_text("There's nothing left here.")


def check_table():
    decrement_steps()
    update_text("You found a locked drawer.")


def check_wardrobe():
    decrement_steps()
    update_text("Just old clothes inside.")


# Create buttons dynamically for exploration
def create_explore_buttons(labels, commands):
    for i in range(len(labels)):
        tk.Button(
            explore_frame,
            text=f"{i+1}. {labels[i]}",
            command=commands[i],
            font=btn_font,
            bg="#61afef",
            fg="black",
            width=15,
        ).pack(pady=2)


# Function to start a new game
def new_game():
    global inventory, discovered_rooms, password_numbers, steps_remaining
    inventory = []
    discovered_rooms = set()
    password_numbers = [random.randint(0, 9) for _ in range(4)]
    steps_remaining = 12
    update_steps_label()
    update_text(
        "New game started. Explore the rooms to find clues and items. You are running away, try to find him before he finds you."
    )


# Main buttons for entering rooms
room_buttons = [
    ("Room 0", enter_room_0),
    ("Room 1", enter_room_1),
    ("Room 2", enter_room_2),
    ("Room 3", enter_room_3),
    ("Check Inventory", check_inventory),
    ("New Game", new_game),
    ("Exit", root.quit),
]

for text, command in room_buttons:
    tk.Button(
        btn_frame,
        text=text,
        command=command,
        font=btn_font,
        bg="#98c379",
        fg="black",
        width=20,
    ).pack(pady=5)

# Run the GUI application
root.mainloop()
