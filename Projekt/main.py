import random
import tkinter as tk
from tkinter import messagebox
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
        self.coin = ImageTk.PhotoImage(Image.open("./imgs/coin.png").resize((20,20)))
        self.basket = ImageTk.PhotoImage(Image.open("./imgs/basket.png").resize((60,60)))


        self.zabawa=tk.IntVar(value=100)
        self.pozywienie=tk.IntVar(value=100)
        self.coins=tk.IntVar(value=0)
        self.zbar = ttk.Progressbar()
        self.obar=ttk.Progressbar()
        self.basketLabel=ttk.Label()

        # Konfiguracja siatki
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.basket_col = 4
        self.rows = 9

        self.current_coin=None
        self.current_coin_col=0
        self.current_coin_row=0

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

        coin = ttk.Label(self.main_frame,image=self.coin)
        coin.grid(row=2,column=0,sticky="w",padx=2, pady=2)
        coinLabel = ttk.Label(self.main_frame,textvariable=self.coins)
        coinLabel.grid(row=2,column=1,sticky="w",padx=2, pady=2)


        label = ttk.Label(self.main_frame,image=photo)
        label.image = photo  # zachowaj referencję
        label.grid(row=3, column=0, columnspan=2, pady=20)


        ttk.Button(self.main_frame,text="Nakarm",command=self.setup_plecake_frame).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self.main_frame, text="Zabawa",command=self.show_zabawa).grid(row=4, column=1, padx=10, pady=10)

    def setup_zabawa_frame(self):
        self.zabawa_frame.rowconfigure(1, weight=1)
        self.zabawa_frame.columnconfigure(0, weight=1)

        top_frame = ttk.Frame(self.zabawa_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=5)

        ttk.Label(top_frame, text="Zabawa: ").grid(row=0, column=0, padx=2, pady=2, sticky="w")
        ttk.Label(top_frame, text="Pożywienie: ").grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.zbar = ttk.Progressbar(top_frame, length=100, maximum=100, variable=self.zabawa,
                                    style="zabawa.Horizontal.TProgressbar")
        self.obar = ttk.Progressbar(top_frame, length=100, maximum=100, variable=self.pozywienie,
                                    style="pozywienie.Horizontal.TProgressbar")
        self.zbar.grid(row=0, column=1, sticky="w", padx=2)
        self.obar.grid(row=1, column=1, sticky="w", padx=2)

        ttk.Label(top_frame, image=self.coin).grid(row=2, column=0, sticky="w", padx=2, pady=2)
        ttk.Label(top_frame, textvariable=self.coins).grid(row=2, column=1, sticky="w", padx=2, pady=2)

        ttk.Button(top_frame, text="Powrót", command=lambda: self.show_main(self.pokemon)).grid(row=0, column=3,sticky="ne", padx=10,pady=2)

# //==========================================================

        self.play_area = ttk.Frame(self.zabawa_frame)
        self.play_area.grid(row=1, column=0, sticky="nsew")
        for r in range(10):
            self.play_area.rowconfigure(r, weight=1)
        for c in range(6):
            self.play_area.columnconfigure(c, weight=1)

        self.basket_col = 2
        self.basketLabel = ttk.Label(self.play_area, image=self.basket)
        self.basketLabel.grid(row=9, column=self.basket_col)

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.current_coin = None
        self.spawn_coin_loop()

    def setup_plecake_frame(self):
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()

        ttk.Button(self.main_frame, text="Powrót", command=lambda: self.show_main(self.pokemon)).grid(row=4,column=0, sticky="n")
        ttk.Button(self.main_frame,text="jagódki(5)",image=self.berry,compound='top',command=lambda:self.nakarm(5)).grid(row=5,column=0,padx=10, pady=10)
        ttk.Button(self.main_frame,text="przysmak(8)",image=self.cookie,compound='top',command=lambda:self.nakarm(8)).grid(row=5,column=1,padx=10, pady=10)
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
        if war<=self.coins.get():
            if self.pozywienie.get()  <100:
                self.pozywienie.set(min(100, self.pozywienie.get() + war))
                self.coins.set(self.coins.get()-war)
            self.show_main(self.pokemon)
        else:
            tk.messagebox.showwarning("Brak monetek!","Nie posiadasz wystarczającej ilości monet aby kupić pokarm")


    def decrease_bars(self):
        if not self.zabawaState:
            if self.pozywienie.get()>0:
                self.pozywienie.set(max(0, self.pozywienie.get() - 3))
            if self.zabawa.get() >0:
                self.zabawa.set(min(100, self.zabawa.get() - 3))
            self.main_frame.after(3000, self.decrease_bars)
        else:

            if self.pozywienie.get()>0:
                self.pozywienie.set(max(0, self.pozywienie.get() - 5))
            if self.zabawa.get() <100:
                self.zabawa.set(min(100, self.zabawa.get() + 3))
            self.main_frame.after(3000, self.decrease_bars)

    def move_left(self, event=None):
        if self.basket_col > 0:
            self.basketLabel.grid_forget()
            self.basket_col -= 1
            self.basketLabel.grid(row=9, column=self.basket_col)

    def move_right(self, event=None):
        if self.basket_col < 5:
            self.basketLabel.grid_forget()
            self.basket_col += 1
            self.basketLabel.grid(row=9, column=self.basket_col)

    def drop_coin(self):
        col = random.randint(0, 5)
        self.current_coin_col = col
        self.current_coin_row = 0
        self.current_coin = ttk.Label(self.play_area, image=self.coin)
        self.current_coin.grid(row=0, column=col)
        self.animate_coin()

    def animate_coin(self):
        if self.current_coin is None:
            return

        self.current_coin.grid_forget()
        self.current_coin_row += 1

        if self.current_coin_row >= self.rows:

            if self.current_coin_col == self.basket_col:
                self.coins.set(self.coins.get() + 5)
            self.current_coin.destroy()
            self.current_coin = None
            return

        self.current_coin.grid(row=self.current_coin_row, column=self.current_coin_col)
        self.zabawa_frame.after(150, self.animate_coin)



    def spawn_coin_loop(self):
        if self.current_coin is None:
            self.drop_coin()
        self.zabawa_frame.after(300, self.spawn_coin_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
