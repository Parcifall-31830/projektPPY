import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("'Pokemon'")
        self.root.geometry("400x500")
        self.zabawaState = False

        # Wczytywanie i skalowanie obrazków
        self.piplup = ImageTk.PhotoImage(Image.open("./imgs/piplup.png"))
        self.eevee = ImageTk.PhotoImage(Image.open("./imgs/eevee.png"))
        self.fennekin = ImageTk.PhotoImage(Image.open("./imgs/fennekin.png").resize((96, 96)))
        self.snivy = ImageTk.PhotoImage(Image.open("./imgs/snivy.png"))
        self.berry = ImageTk.PhotoImage(Image.open("./imgs/berry.png").resize((96, 96)))
        self.cookie = ImageTk.PhotoImage(Image.open("./imgs/cookie.png").resize((96, 96)))


        self.zabawa=tk.IntVar(value=100)
        self.pozywienie=tk.IntVar(value=100)
        self.zbar = ttk.Progressbar()
        self.obar=ttk.Progressbar()

        # Konfiguracja siatki
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Tworzenie ramek
        self.start_frame = ttk.Frame(self.root)
        self.main_frame = ttk.Frame(self.root)
        self.zabawa_frame=ttk.Frame(self.root)

        self.pokemon=""

        for frame in (self.start_frame, self.main_frame, self.zabawa_frame):
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
        self.start_decreaseBars_loop()

    def setup_main_frame(self, pokemon):
        self.zabawaState = False
        self.pokemon=pokemon
        self.main_frame.columnconfigure(0, weight=1, minsize=150)
        self.main_frame.columnconfigure(1, weight=1, minsize=150)

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


        self.zbar = ttk.Progressbar(self.main_frame, length=100,maximum=100,variable = self.zabawa,style="zabawa.Horizontal.TProgressbar")
        self.obar = ttk.Progressbar(self.main_frame,length=100,maximum=100,variable=self.pozywienie,style="pozywienie.Horizontal.TProgressbar")
        zabawa.grid(row=0, column=0,sticky="w",padx=2, pady=2)
        pozywienie.grid(row=1, column=0,sticky="w",padx=2, pady=2)
        self.zbar.grid(row=0, column=1,sticky="w",padx=2, pady=2)
        self.obar.grid(row=1, column=1,sticky="w",padx=2, pady=2)


        label = ttk.Label(self.main_frame,image=photo)
        label.image = photo  # zachowaj referencję
        label.grid(row=2, column=0, columnspan=2, pady=20)

        # Przycisk "Zabawa"
        ttk.Button(self.main_frame,text="Nakarm",command=self.setup_plecake_frame).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.main_frame, text="Zabawa",command=self.show_zabawa).grid(row=3, column=1, padx=10, pady=10)

    def setup_zabawa_frame(self):
        self.zabawa_frame.columnconfigure(0, weight=1)
        self.zabawa_frame.columnconfigure(1, weight=1)

        self.zbar = ttk.Progressbar(self.zabawa_frame, length=100, maximum=100,variable=self.zabawa, style="zabawa.Horizontal.TProgressbar")
        self.obar = ttk.Progressbar(self.zabawa_frame, length=100, maximum=100,variable=self.pozywienie, style="pozywienie.Horizontal.TProgressbar")

        self.zbar.grid(row=0, column=0, padx=2)
        self.obar.grid(row=1, column=0, padx=2)

        ttk.Button(self.zabawa_frame, text="Powrót", command=lambda: self.show_main(self.pokemon)).grid(
            row=0, column=7, sticky="n", padx=10, pady=10
        )

    def setup_plecake_frame(self):
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()

        ttk.Button(self.main_frame,text="jagódki(5)",image=self.berry,compound='top',command=lambda:self.nakarm(5)).grid(row=4,column=0,padx=10, pady=10)
        ttk.Button(self.main_frame,text="przysmak(8)",image=self.cookie,compound='top',command=lambda:self.nakarm(8)).grid(row=4,column=1,padx=10, pady=10)
        self.main_frame.tkraise()



    def show_start(self):
        self.start_frame.tkraise()

    def show_main(self, pokemon):
        self.zabawaState = False
        self.setup_main_frame(pokemon)
        self.main_frame.tkraise()


    def show_zabawa(self):
        self.zabawaState = True
        self.setup_zabawa_frame()
        self.zabawa_frame.tkraise()


    def start_decreaseBars_loop(self):
        self.decrease_bars()


    def nakarm(self,war):
        if self.pozywienie.get()  <100:
            self.pozywienie.set(min(100, self.pozywienie.get() + war))
        self.show_main(self.pokemon)

    def decrease_bars(self):
        if not self.zabawaState:
            if self.pozywienie.get()>0:
                self.pozywienie.set(max(0, self.pozywienie.get() - 5))
            if self.zabawa.get() >0:
                self.zabawa.set(max(0, self.zabawa.get() - 1))
            self.main_frame.after(3000, self.decrease_bars)
        else:
            if self.pozywienie.get()>0:
                self.pozywienie.set(max(0, self.pozywienie.get() - 7))
            if self.zabawa.get() >0:
                self.zabawa.set(max(100, self.zabawa.get() + 1))
            self.main_frame.after(3000, self.decrease_bars)
# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
