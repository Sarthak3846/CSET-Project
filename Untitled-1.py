import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class Fridge:
    
    def __init__(self):
        self.items = []

    def add_item(self, name, quantity, mfg_date, exp_date):
        item = {
            'name': name,
            'quantity': quantity,
            'mfg_date': mfg_date,
            'exp_date': exp_date
        }
        self.items.append(item)
        return f"{name} added!"

    def remove_item(self, name, quantity=1):
        for item in self.items:
            if item['name'] == name:
                if item['quantity'] >= quantity:
                    item['quantity'] -= quantity
                    if item['quantity'] == 0:
                        self.items.remove(item)
                    return f"{quantity} {name} removed!"
                return f"Not enough {name} to remove."
        return f"{name} not found."

    def list_items(self):
        if not self.items:
            return "The fridge is empty."
        else:
            item_list = []
            for item in self.items:
                status = self.check_freshness(item)
                item_list.append(f"{item['name']} - Quantity: {item['quantity']} - Expiration: {item['exp_date']} - Status: {status}")
            return "\n".join(item_list)

    def check_freshness(self, item):
        exp_date = datetime.strptime(item['exp_date'], "%Y-%m-%d")
        return "Fresh" if exp_date >= datetime.now() else "Expired"

class FridgeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Fridge Interface")
        self.fridge = Fridge()

        # Input fields
        self.name_label = tk.Label(master, text="Item Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        self.quantity_label = tk.Label(master, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.pack()

        self.mfg_label = tk.Label(master, text="Manufacturing Date (YYYY-MM-DD):")
        self.mfg_label.pack()
        self.mfg_entry = tk.Entry(master)
        self.mfg_entry.pack()

        self.exp_label = tk.Label(master, text="Expiration Date (YYYY-MM-DD):")
        self.exp_label.pack()
        self.exp_entry = tk.Entry(master)
        self.exp_entry.pack()

        # Buttons
        self.add_button = tk.Button(master, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remove Item", command=self.remove_item)
        self.remove_button.pack()

        self.list_button = tk.Button(master, text="List Items", command=self.list_items)
        self.list_button.pack()

        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.pack()

    def add_item(self):
        name = self.name_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            mfg_date = self.mfg_entry.get()
            exp_date = self.exp_entry.get()
            result = self.fridge.add_item(name, quantity, mfg_date, exp_date)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity.")

    def remove_item(self):
        name = self.name_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            result = self.fridge.remove_item(name, quantity)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity.")

    def list_items(self):
        result = self.fridge.list_items()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = FridgeApp(root)
    root.mainloop()
import pyttsx3
engine = pyttsx3.init()

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()
