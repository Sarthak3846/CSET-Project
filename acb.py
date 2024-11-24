import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import pyttsx3
from recipes import recipes  


engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


class Fridge:
    def __init__(self):
        self.items = []

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def add_item(self, name, quantity, mfg_date, exp_date):
        item = {
            'name': name,
            'quantity': int(quantity),
            'mfg_date': mfg_date,
            'exp_date': exp_date
        }
        self.items.append(item)
        self.speak(f"{name} added to the fridge.")
        messagebox.showinfo("Info", f"{name} added to the fridge.")

    def remove_item(self, name, quantity=1):
        for item in self.items:
            if item['name'] == name:
                if item['quantity'] >= quantity:
                    item['quantity'] -= quantity
                    if item['quantity'] == 0:
                        self.items.remove(item)
                    self.speak(f"{quantity} {name} removed from the fridge.")
                    messagebox.showinfo("Info", f"{quantity} {name} removed from the fridge.")
                else:
                    self.speak(f"Not enough {name} in the fridge to remove.")
                    messagebox.showwarning("Warning", f"Not enough {name} in the fridge to remove.")
                return
        self.speak(f"{name} not found in the fridge.")
        messagebox.showwarning("Warning", f"{name} not found in the fridge.")

    def list_items(self):
        if not self.items:
            self.speak("The fridge is empty.")
            messagebox.showinfo("Info", "The fridge is empty.")
        else:
            items_info = ""
            for item in self.items:
                status = self.check_freshness(item)
                item_info = f"{item['name']} - Quantity: {item['quantity']} - Expiration: {item['exp_date']} - Status: {status}\n"
                items_info += item_info
                self.speak(f"{item['name']}, Quantity: {item['quantity']}, Status: {status}")
            messagebox.showinfo("Fridge Items", items_info)

    def check_freshness(self, item):
        exp_date = datetime.strptime(item['exp_date'], "%Y-%m-%d")
        if exp_date >= datetime.now():
            return "Fresh"
        else:
            return "Expired"


class RecipeSuggester:
    def __init__(self, fridge_items):
        self.fridge_items = [item['name'] for item in fridge_items]

    def suggest_recipes(self, diet_type):
        suggested_recipes = []
        for recipe in recipes:
            if recipe["diet"] == diet_type and all(item in self.fridge_items for item in recipe["ingredients"]):
                suggested_recipes.append(recipe)

        if suggested_recipes:
            suggestions_text = f"I found {len(suggested_recipes)} recipes for your {diet_type} diet.\n"
            for recipe in suggested_recipes:
                recipe_info = f"{recipe['name']} ({recipe['calories']} calories)\n"
                suggestions_text += recipe_info
                engine.say(recipe_info)
            engine.runAndWait()
            return suggestions_text
        else:
            engine.say(f"Sorry, I couldn't find any matching recipes for your {diet_type} diet.")
            engine.runAndWait()
            return "No matching recipes found."


class NutriFridgeApp:
    def __init__(self, root):
        self.fridge = Fridge()
        self.root = root
        self.root.title("NutriFridge - Your Smart Nutrition Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="NutriFridge", font=("Helvetica", 24, "bold"), bg="#4CAF50", fg="white", pady=10)
        title_label.pack(fill=tk.X)

        add_frame = ttk.LabelFrame(self.root, text="Add Item", padding=10)
        add_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(add_frame, text="Item Name").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(add_frame, text="Quantity").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(add_frame, text="MFG Date (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(add_frame, text="EXP Date (YYYY-MM-DD)").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.name_entry = ttk.Entry(add_frame)
        self.quantity_entry = ttk.Entry(add_frame)
        self.mfg_date_entry = ttk.Entry(add_frame)
        self.exp_date_entry = ttk.Entry(add_frame)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        self.mfg_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.exp_date_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Add Item", command=self.add_item).grid(row=4, column=1, pady=10)

        remove_frame = ttk.LabelFrame(self.root, text="Remove Item", padding=10)
        remove_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(remove_frame, text="Remove Item Name").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(remove_frame, text="Quantity").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.remove_name_entry = ttk.Entry(remove_frame)
        self.remove_quantity_entry = ttk.Entry(remove_frame)

        self.remove_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.remove_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(remove_frame, text="Remove Item", command=self.remove_item).grid(row=2, column=1, pady=10)

    
        recipe_frame = ttk.LabelFrame(self.root, text="Recipe Suggestions", padding=10)
        recipe_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(recipe_frame, text="Diet Type").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.diet_type_entry = ttk.Entry(recipe_frame)
        self.diet_type_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(recipe_frame, text="Suggest Recipes", command=self.suggest_recipes).grid(row=1, column=1, pady=10)

        ttk.Button(self.root, text="List Items in Fridge", command=self.list_items).pack(pady=10)

    def add_item(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        mfg_date = self.mfg_date_entry.get()
        exp_date = self.exp_date_entry.get()
        if name and quantity and mfg_date and exp_date:
            self.fridge.add_item(name, quantity, mfg_date, exp_date)
        else:
            messagebox.showwarning("Warning", "Please enter all fields for adding an item.")

    def remove_item(self):
        name = self.remove_name_entry.get()
        quantity = int(self.remove_quantity_entry.get()) if self.remove_quantity_entry.get() else 1
        self.fridge.remove_item(name, quantity)

    def list_items(self):
        self.fridge.list_items()

    def suggest_recipes(self):
        diet_type = self.diet_type_entry.get().lower()
        if diet_type:
            suggester = RecipeSuggester(self.fridge.items)
            suggestions = suggester.suggest_recipes(diet_type)
            messagebox.showinfo("Recipe Suggestions", suggestions)
        else:
            messagebox.showwarning("Warning", "Please enter a diet type.")


root = tk.Tk()
app = NutriFridgeApp(root)
root.mainloop()
