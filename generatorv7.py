import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class OptionPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Game Generator")
        self.root.geometry("768x768")
        
        # Hintergrundbild laden und anzeigen
        try:
            self.bg_image = Image.open("rgg2.jpg")
            self.bg_image = self.bg_image.resize((768, 768), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            
            # Canvas für Hintergrundbild
            self.canvas = tk.Canvas(root, width=768, height=768)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
        except Exception as e:
            print(f"Fehler beim Laden des Hintergrundbildes: {e}")
            self.canvas = tk.Canvas(root, width=768, height=768)
            self.canvas.pack(fill="both", expand=True)

        # Fenster Transparenz
        root.attributes("-alpha", 0.98)
        
        # Style für ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#252625', foreground='#FFFFFF')
        style.map('.', background=[('active', '#024670')])
        
        # Verlaufsliste oben
        self.history_label = ttk.Label(
            self.canvas,
            text="Verlauf:",
            font=('Arial', 12, 'bold'),
            foreground='#3498db'  # Verlauf in Blau
        )
        self.history_label.place(relx=0.5, rely=0.35, anchor="center")
        self.history = []
        
        # Button in der Mitte
        self.pick_button = ttk.Button(
            self.canvas, 
            text="Roll",
            command=self.pick_random,
            style="Big.TButton"        # Stilname zuweisen
        )
        self.pick_button.place(relx=0.5, rely=0.58, anchor="center")
       
        # Button-Stil anpassen
        style = ttk.Style()
        style.configure(
            "Big.TButton",             # Name des spezifischen Stils
            font=('Arial', 20, 'bold'),  # Große Schrift für den Roll-Button
            padding=(5, 5)           # Innenabstand für größere Größe
        )
       
        
        # Ergebnis 
        self.result_label = ttk.Label(
            self.canvas,
            text="Ergebnis",
            font=('Arial', 24, 'bold'),
            foreground='#2ecc71'  # Ergebnis in Grün
        )
        self.result_label.place(relx=0.5, rely=0.30, anchor="center")
        
        # Eingabefelder in zwei Spalten mit Standardwerten
        self.entries = []
        self.default_values = ["CS", "HS", "LOL", "StrafJib", "", ""]  # Standardwerte
        
        # Linke Spalte (Optionen 1-3)
        for i in range(3):
            label = ttk.Label(self.canvas, text=f"Option {i+1}:")
            label.place(relx=0.1, rely=0.70 + i*0.08, anchor="w")
            
            entry = tk.Entry(self.canvas, width=20, fg='white', bg='#252625')
            entry.insert(0, self.default_values[i])  # Standardwert einfügen
            entry.place(relx=0.25, rely=0.70 + i*0.08, anchor="w")
            self.entries.append(entry)
        
        # Rechte Spalte (Optionen 4-6)
        for i in range(3):
            label = ttk.Label(self.canvas, text=f"Option {i+4}:")
            label.place(relx=0.55, rely=0.70 + i*0.08, anchor="w")
            
            entry = tk.Entry(self.canvas, width=20, fg='white', bg='#252625')
            entry.insert(0, self.default_values[i+3])  # Standardwert einfügen
            entry.place(relx=0.7, rely=0.70 + i*0.08, anchor="w")
            self.entries.append(entry)
        
        # Reset-Button
        self.reset_button = ttk.Button(
            self.canvas,
            text="Reset",
            command=self.reset_fields
        )
        self.reset_button.place(relx=0.95, rely=0.95, anchor="se")
    
    def pick_random(self):
        # Nur gefüllte Textfelder berücksichtigen, die noch nicht im Verlauf sind
        active_options = []
        for entry in self.entries:
            text = entry.get().strip()
            if text and text not in self.history:
                active_options.append(text)
        
        if not active_options:
            self.result_label.config(text="Mach Reset amk")
            return
        
        chosen = random.choice(active_options)
        self.history.append(chosen)
        
        self.result_label.config(text=f"-> {chosen} <-")
        
        history_text = "Verlauf: " + " -> ".join(self.history)
        self.history_label.config(text=history_text)
    
    def reset_fields(self):
        """Setzt alle Eingabefelder und den Verlauf zurück."""
        for i, entry in enumerate(self.entries):
            entry.delete(0, tk.END)  # Löscht den Inhalt des Eingabefeldes
            entry.insert(0, self.default_values[i])  # Standardwerte wieder einfügen
        self.history = []  # Verlauf leeren
        self.history_label.config(text="Verlauf:")  # Verlaufstext zurücksetzen
        self.result_label.config(text="Ergebnis")  # Ergebnis zurücksetzen

def main():
    root = tk.Tk()
    app = OptionPicker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
