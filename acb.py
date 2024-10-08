import tkinter as tk
from tkinter import messagebox
import pyttsx3
from datetime import datetime

# Initialize the text-to-speech engine with a more conversational tone
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slow down the voice to sound more natural
engine.setProperty('volume', 1)  # Full volume
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Choose a female voice for a friendly tone

class Fridge:
    def __init__(self):
        # Initialize an empty fridge list to store items
        self.items = []

    # Function to make the fridge 'speak' using text-to-speech
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    # Function to add items to the fridge
    def add_item(self, name, quantity, mfg_date, exp_date):
        # Create a dictionary to store item details
        item = {
            'name': name,
            'quantity': quantity,
            'mfg_date': mfg_date,
            'exp_date': exp_date
        }
        self.items.append(item)
        # Provide a friendly voice response
        self.speak(f"I've added {quantity} of {name} to your fridge.")

    # Function to remove items from the fridge
    def remove_item(self, name, quantity=1):
        for item in self.items:
            if item['name'] == name:
                if item['quantity'] >= quantity:
                    item['quantity'] -= quantity
                    if item['quantity'] == 0:
                        self.items.remove(item)
                    # Voice confirmation after removing the item
                    self.speak(f"{quantity} of {name} has been removed from the fridge.")
                else:
                    # If there's not enough quantity to remove
                    self.speak(f"There's not enough {name} in the fridge to remove.")
                return
        # If the item isn't found in the fridge
        self.speak(f"I couldn't find any {name} in the fridge.")

    # Function to list all items currently in the fridge
    def list_items(self):
        if not self.items:
            self.speak("The fridge is currently empty.")
        else:
            self.speak("Here’s a list of items in your fridge:")
            for item in self.items:
                freshness_status = self.check_freshness(item)
                print(f"{item['name']} - Quantity: {item['quantity']} - Expiry: {item['exp_date']} - Status: {freshness_status}")
                self.speak(f"{item['name']}, quantity {item['quantity']}, and it is {freshness_status}.")

    # Function to check the freshness of an item based on its expiration date
    def check_freshness(self, item):
        exp_date = datetime.strptime(item['exp_date'], "%Y-%m-%d")
        # Compare expiration date with the current date
        if exp_date >= datetime.now():
            return "fresh"
        else:
            return "expired"

# Create an instance of the Fridge class
fridge = Fridge()

# Example: Add some items to test the system
fridge.add_item("Paneer", 2, "2024-10-01", "2024-10-10")
fridge.add_item("Milk", 1, "2024-10-05", "2024-10-07")

# Example: List items and check freshness
fridge.list_items()

# Example: Remove an item
fridge.remove_item("Paneer", 1)
