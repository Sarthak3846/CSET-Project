
import tkinter as tk
from tkinter import messagebox 
import pyttsx3
from datetime import datetime 

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

class Fridge:
    def __init__(self):
        self.items=[]

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def add_item(self,name,quantity,mfg_date,exp_date):
        item={
            'name':name,
            'quantity':quantity,
            'mfg_date':mfg_date,
            'exp_date':exp_date
        }
        self.items.append(item)
        self.speak(f"{name} added to the fridge.")

    def remove_item(self,name,quantity=1):
        for item in self.items:
            if item['name']==name:
                if item['quantity']>=quantity:
                    item['quantity']-=quantity
                    if item['quantity']==0:
                        self.items.remove(item)
                    self.speak(f"{quantity} {name} removed from the fridge")
                else:
                    self.speak(f"Not enough {name} in the fridge to remove")
                return
        self.speak(f"{name} not found in the fridge")

    def list_items(self):
        if not self.items:
            self.speak("The fridge is empty.")
        else:
            self.speak("Here are the items in your fridge:")
            for item in self.items:
                status = self.check_freshness(item)
                print(f"{item['name']} - Quantity: {item['quantity']} - Expiration: {item['exp_date']} - Status: {status}")
                self.speak(f"{item['name']}, Quantity: {item['quantity']}, Status: {status}")           

    def check_freshness(self, item):
        exp_date = datetime.strptime(item['exp_date'], "%Y-%m-%d")
        if exp_date >= datetime.now():
            return "Fresh"
        else:
            return "Expired"



fridge = Fridge()
