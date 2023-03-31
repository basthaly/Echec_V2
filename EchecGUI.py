from Echec import Jeu_Echec

import tkinter as tk
from PIL import Image, ImageTk

class FenetrePersonnalisee(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Jeu d'échecs")
        self.geometry("854x480")
        self.minsize(200, 200)
        self.case_taille=50

        self.canvas = tk.Canvas(self, width=854, height=480)
        self.canvas.pack()

        self.jeu = Jeu_Echec()
        
        self.menu()

        self.canvas.bind("<Configure>", self.redessiner_echiquier)
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.bind("<Configure>", self.on_resize)
        self.update_idletasks()

        self.selected_piece = None
        self.selected_piece_coords = Nonek

        self.inverser_echiquier = False
        self.fullscreen = False
        self.save_taille = (0,0)
        self.piece_selectionnee = None

        self.mise_a_jour_piece_images()

        self.redessiner_echiquier()

    def mouse_click(self, event):
        x, y = event.x // self.case_taille, event.y // self.case_taille
        if self.inverser_echiquier:
            x, y = 7 - x, 7 - y

        if self.selected_piece:
            if (y, x) != self.selected_piece_coords:
                self.move_piece(self.selected_piece_coords, (y, x))
            self.selected_piece = None
            self.selected_piece_coords = None
        else:
            piece = self.jeu.echiquier[y][x]
            if piece != 0 and self.jeu.piece_couleur(piece) == self.jeu.joueur:
                self.selected_piece = piece
                self.selected_piece_coords = (y, x)

        self.redessiner_echiquier()

    def move_piece(self, start, end):
        self.jeu.action(start, end, self.jeu.joueur)

    def on_resize(self, event=None):
        self.case_taille = self.calculer_case_taille()
        self.canvas.config(width=event.width, height=event.height)  # Mettre à jour la taille du canvas
        self.redessiner_echiquier()

    def menu(self):
        menubar = tk.Menu(self)

        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Inverser échiquier", command=self.inverser)
        menubar.add_cascade(label="Options", menu=options_menu)

        self.resolution_menu = tk.Menu(menubar, tearoff=0)
        self.resolution_menu.add_command(label="480p", command=lambda: self.changer_taille(854, 480))
        self.resolution_menu.add_command(label="720p", command=lambda: self.changer_taille(1280, 720))
        self.resolution_menu.add_command(label="1080p", command=lambda: self.changer_taille(1920, 1080))
        self.resolution_menu.add_separator()
        self.resolution_menu.add_command(label="Plein écran", command=self.mode_plein_ecran)
        menubar.add_cascade(label="Résolution", menu=self.resolution_menu)

        self.config(menu=menubar)

    def calculer_case_taille(self):
        largeur = self.winfo_width()
        hauteur = self.winfo_height()
        return min(largeur, hauteur) // 8

    def dessiner_echiquier(self):
        for i in range(8):
            for j in range(8):
                if self.inverser_echiquier:
                    x, y = (7 - i) * self.case_taille, (7 - j) * self.case_taille
                else:
                    x, y = i * self.case_taille, j * self.case_taille
                couleur = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x, y, x + self.case_taille, y + self.case_taille, fill=couleur)
                # self.canvas.create_image(x, y, image=image, anchor=tk.NW, tags=("piece",))

                piece = self.jeu.echiquier[j][i]
                if (j, i) == self.selected_piece_coords:
                    self.canvas.create_rectangle(x, y, x + self.case_taille, y + self.case_taille, fill="yellow")
                if piece != 0:
                    couleur = "blanc" if piece > 0 else "noir"
                    nom_piece = self.jeu.piece_nom(abs(piece))
                    image = self.piece_images[f"{couleur}_{nom_piece}"]
                    self.canvas.create_image(x, y, image=image, anchor=tk.NW)

    def redessiner_echiquier(self, event=None):
        self.canvas.delete("all")
        self.mise_a_jour_piece_images()
        self.dessiner_echiquier()    

    def changer_taille(self, largeur, hauteur):
        self.geometry(f"{largeur}x{hauteur}")
        self.canvas.config(width=largeur, height=hauteur)
        self.canvas.update()

    def mode_plein_ecran(self):
        self.fullscreen = not self.fullscreen
        self.attributes('-fullscreen', self.fullscreen)
        self.resolution_menu.entryconfig("480p", state=tk.DISABLED if self.fullscreen else tk.NORMAL)
        self.resolution_menu.entryconfig("720p", state=tk.DISABLED if self.fullscreen else tk.NORMAL)
        self.resolution_menu.entryconfig("1080p", state=tk.DISABLED if self.fullscreen else tk.NORMAL)

    def inverser(self):
        self.inverser_echiquier = not self.inverser_echiquier
        self.redessiner_echiquier()

    def charger_piece_images(self):
        piece_images = {}
        pieces = ["pion", "tour", "cavalier", "fou", "roi", "reine"]
        couleurs = ["blanc", "noir"]

        for piece in pieces:
            for couleur in couleurs:
                chemin = f"//nas-bastha/home/Drive/Travail/Echec_v2/images/pieces/{couleur}_{piece}.png"
                image = Image.open(chemin)
                image = image.resize((self.case_taille, self.case_taille), Image.LANCZOS)
                piece_images[f"{couleur}_{piece}"] = ImageTk.PhotoImage(image)

        return piece_images
    
    def mise_a_jour_piece_images(self):
        self.piece_images = self.charger_piece_images()

if __name__ == "__main__":
    app = FenetrePersonnalisee()
    app.mainloop()