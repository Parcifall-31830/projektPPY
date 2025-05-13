import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja z ramkami")
        self.root.geometry("400x500")

        # Wczytywanie i skalowanie obrazków
        self.piplup = ImageTk.PhotoImage(Image.open("./imgs/piplup.png"))
        self.eevee = ImageTk.PhotoImage(Image.open("./imgs/eevee.png"))
        self.fennekin = ImageTk.PhotoImage(Image.open("./imgs/fennekin.png").resize((96, 96)))
        self.snivy = ImageTk.PhotoImage(Image.open("./imgs/snivy.png"))

        self.zabawa=tk.IntVar(value=100)
        self.pozywienie=tk.IntVar(value=100)


        # Konfiguracja siatki
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Tworzenie ramek
        self.start_frame = ttk.Frame(self.root)
        self.main_frame = ttk.Frame(self.root)

        for frame in (self.start_frame, self.main_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self.setup_start_frame()
        self.show_start()

    def setup_start_frame(self):
        self.start_frame.columnconfigure(0, weight=1)
        self.start_frame.columnconfigure(1, weight=1)

        ttk.Label(self.start_frame, text="Wybierz pokemona", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.start_frame, text="").grid(row=1, column=0, columnspan=2, pady=40)

        ttk.Button(self.start_frame, image=self.piplup, command=lambda: self.show_main("piplup")).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.start_frame, image=self.eevee, command=lambda: self.show_main("eevee")).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(self.start_frame, image=self.fennekin, command=lambda: self.show_main("fennekin")).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.start_frame, image=self.snivy, command=lambda: self.show_main("snivy")).grid(row=3, column=1, padx=10, pady=10)

    def setup_main_frame(self, pokemon):
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Usuń wszystkie stare widgety z main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        path = f"./imgs/{pokemon}.png"
        image = Image.open(path).resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        zabawa = ttk.Label(self.main_frame, text="Zabawa: ",justify=tk.LEFT)
        pozywienie = ttk.Label(self.main_frame, text="Pożywienie: ",justify=tk.LEFT)

        style=ttk.Style(self.main_frame)
        style.theme_use('default')
        style.configure("zabawa.Horizontal.TProgressbar", background="#4ecdc4")
        style.configure("pozywienie.Horizontal.TProgressbar", background="#ffb347")


        zbar = ttk.Progressbar(self.main_frame, length=100,maximum=100,variable = self.zabawa,style="zabawa.Horizontal.TProgressbar")
        obar = ttk.Progressbar(self.main_frame,length=100,maximum=100,variable=self.pozywienie,style="pozywienie.Horizontal.TProgressbar")
        zabawa.grid(row=0, column=0,sticky="w",padx=2, pady=2)
        pozywienie.grid(row=1, column=0,sticky="w",padx=2, pady=2)
        zbar.grid(row=0, column=1,sticky="w",padx=2, pady=2)
        obar.grid(row=1, column=1,sticky="w",padx=2, pady=2)


        label = ttk.Label(self.main_frame,image=photo)
        label.image = photo  # zachowaj referencję
        label.grid(row=2, column=0, columnspan=2, pady=20)

        # Przycisk "Zabawa"
        ttk.Button(self.main_frame,text="Nakarm").grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.main_frame, text="Dzicz", command=self.show_start).grid(row=3, column=1, padx=10, pady=10)
        self.start_hunger_loop()

    def show_start(self):
        self.start_frame.tkraise()

    def show_main(self, pokemon):
        self.setup_main_frame(pokemon)
        self.main_frame.tkraise()

    def start_hunger_loop(self):
        self.decrease_hunger()

    def decrease_hunger(self):
        if self.pozywienie.get()>0:
            self.pozywienie.set(self.pozywienie.get()-5)
        self.main_frame.after(10000, self.decrease_hunger)

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
