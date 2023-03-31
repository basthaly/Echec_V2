#!/usr/bin/python
# -*-coding:Latin-1 -* 


## Import ici
## Fin des import

class Jeu_Echec:
    """
    Dans ce programme, les pièces d'échecs sont représentées par des entiers sur l'échiquier.
    Les pièces blanches ont des valeurs positives, tandis que les pièces noires ont des valeurs négatives.
    Les valeurs absolues des entiers correspondent aux pièces comme suit :

    1 (ou -1) : Pion
    2 (ou -2) : Tour
    3 (ou -3) : Cavalier
    4 (ou -4) : Fou
    5 (ou -5) : Roi
    6 (ou -6) : Dame

    Les cases vides de l'échiquier sont représentées par le chiffre 0.
    Ainsi, chaque case de l'échiquier contient un entier.
    Cette entier indique la pièce présente sur cette case et la couleur de cette pièce (positive pour les Blancs, négative pour les Noirs).
    """
    def __init__(self):
        self.echiquier=[]
        self.tour=0
        self.joueur = 1  # 1 pour les Blancs, -1 pour les Noirs

        for i in range (8):
            J=[]
            for j in range(8):
                J.append(0)
            self.echiquier.append(J)

        # Mise en place des pions noirs
        for i in range(8):
            self.echiquier[1][i] = -1  # pion
        self.echiquier[0] = [-2, -3, -4, -5, -6, -4, -3, -2]  # autres pièces

        # Mise en place des pions blancs
        for i in range(8):
            self.echiquier[6][i] = 1  # pion
        self.echiquier[7] = [2, 3, 4, 5, 6, 4, 3, 2]  # autres pièces

    def __str__(self):
        a="Tour : "+str(self.tour)+"\n"
        for j in range(8):
            a=a+"   "+str(j+1)+"  "
        a=a+"\n"
        for i in reversed(range(8)):
            for j in range(8):
                if self.echiquier[i][j] < 0:
                    a = a + "| " + str(self.echiquier[i][j]) + " |"
                else:
                    a = a + "|  " + str(self.echiquier[i][j]) + " |"
            a = a + " " + chr(72 - i) + "\n"
        a = a + "\n"
        return a
    
    def piece_nom(self, piece):
        nom_piece_dict = {
            1: "pion",
            2: "tour",
            3: "cavalier",
            4: "fou",
            5: "roi",
            6: "reine",
        }
        return nom_piece_dict.get(piece, "")
    
    def piece_couleur(self, piece):
        if piece == 0:
            return None
        elif piece > 0:
            return 1
        else:
            return -1

    def Tr_pos(self,pos): #Récupère H4 et renvoie (8,4)
        for i in range (65,73):
            if chr(i)==pos[0]:
                # x=i-65
                x = 72 - ord(pos[0])
                break
        return (x,int(pos[1])-1)

    def est_dans_echiquier(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8
    
    def action(self, p1, p2, joueur):
        piece = self.echiquier[p1[0]][p1[1]]
        valid_moves = []

        if piece * joueur > 0:  # Vérifie si la pièce appartient au joueur actuel
            piece_type = abs(piece)

            if piece_type == 1:
                valid_moves = self.pion_mouvements_valides(*p1)
            elif piece_type == 2:
                valid_moves = self.tour_mouvements_valides(*p1)
            elif piece_type == 3:
                valid_moves = self.cavalier_mouvements_valides(*p1)
            elif piece_type == 4:
                valid_moves = self.fou_mouvements_valides(*p1)
            elif piece_type == 5:
                valid_moves = self.roi_mouvements_valides(*p1)
            elif piece_type == 6:
                valid_moves = self.dame_mouvements_valides(*p1)

            if p2 in valid_moves:  # Vérifie si le mouvement est valide
                self.tour += 1
                self.echiquier[p2[0]][p2[1]] = self.echiquier[p1[0]][p1[1]]
                self.echiquier[p1[0]][p1[1]] = 0
                self.joueur = -joueur  # Change le joueur actuel
            else:
                print("Mouvement non valide.")
        else:
            print("C'est au tour du joueur", joueur, "de jouer.")

    def deplace(self,p1,p2):
        pos1=self.Tr_pos(p1)
        pos2=self.Tr_pos(p2)
        self.action(pos1,pos2,self.joueur)

    def pion_mouvements_valides(self, y, x):
        valid_moves = []
        piece = self.echiquier[y][x]
        piece_couleur = self.piece_couleur(piece)

        if piece_couleur is None:
            return []

        forward = -1 if piece_couleur == 1 else 1
        start_rank = 6 if piece_couleur == 1 else 1

        # Mouvement en avant d'une case
        if self.est_dans_echiquier(x, y + forward) and self.echiquier[y + forward][x] == 0:
            valid_moves.append((y + forward, x ))

        # Mouvement en avant de deux cases si le pion est sur sa rangée initiale
        if y == start_rank and self.echiquier[y + forward][x] == 0 and self.echiquier[y + 2 * forward][x] == 0:
            valid_moves.append((y + 2 * forward,x))

        # Mouvements diagonaux pour capturer une pièce adverse
        for dx in [-1, 1]:
            if self.est_dans_echiquier(x + dx, y + forward) and self.piece_couleur(self.echiquier[y + forward][x + dx]) == -piece_couleur:
                valid_moves.append((y + forward, x + dx))

        return valid_moves
    
    def tour_mouvements_valides(self, y, x):
        valid_moves = []
        piece = self.echiquier[y][x]
        piece_couleur = self.piece_couleur(piece)

        if piece_couleur is None:
            return []

        # Vérifier les mouvements dans les 4 directions : haut, bas, gauche et droite
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Continuer dans la direction actuelle jusqu'à ce que l'on rencontre une pièce ou que l'on sorte de l'échiquier
            while self.est_dans_echiquier(nx, ny):
                target_piece = self.echiquier[ny][nx]
                target_piece_couleur = self.piece_couleur(target_piece)

                if target_piece_couleur != piece_couleur:
                    valid_moves.append((ny, nx))

                if target_piece != 0:  # Arrêter le mouvement lorsque l'on rencontre une pièce
                    break

                nx += dx
                ny += dy

        return valid_moves
    
    def cavalier_mouvements_valides(self, y, x):
        valid_moves = []
        piece = self.echiquier[y][x]
        piece_couleur = self.piece_couleur(piece)

        if piece_couleur is None:
            return []

        # Vérifier les mouvements en forme de L
        mouvements = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]
        for dx, dy in mouvements:
            nx, ny = x + dx, y + dy

            if self.est_dans_echiquier(nx, ny):
                target_piece = self.echiquier[ny][nx]
                target_piece_couleur = self.piece_couleur(target_piece)

                if target_piece_couleur != piece_couleur:
                    valid_moves.append((ny, nx))

        return valid_moves
    
    def fou_mouvements_valides(self, y, x):
        valid_moves = []
        piece = self.echiquier[y][x]
        piece_couleur = self.piece_couleur(piece)

        if piece_couleur is None:
            return []

        # Vérifier les mouvements diagonaux
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Continuer dans la direction actuelle jusqu'à ce que l'on rencontre une pièce ou que l'on sorte de l'échiquier
            while self.est_dans_echiquier(nx, ny):
                target_piece = self.echiquier[ny][nx]
                target_piece_couleur = self.piece_couleur(target_piece)

                if target_piece_couleur != piece_couleur:
                    valid_moves.append((ny, nx))

                if target_piece != 0:  # Arrêter le mouvement lorsque l'on rencontre une pièce
                    break

                nx += dx
                ny += dy

        return valid_moves
    
    def roi_mouvements_valides(self, y, x):
        valid_moves = []
        piece = self.echiquier[y][x]
        piece_couleur = self.piece_couleur(piece)

        if piece_couleur is None:
            return []

        # Vérifier les mouvements dans toutes les directions
        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1),  # Mouvements verticaux et horizontaux
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Mouvements diagonaux
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if self.est_dans_echiquier(nx, ny):
                target_piece = self.echiquier[ny][nx]
                target_piece_couleur = self.piece_couleur(target_piece)

                if target_piece_couleur != piece_couleur:
                    valid_moves.append((ny, nx))

        return valid_moves
    
    def dame_mouvements_valides(self, y, x):
        valid_moves = []
        piece = self.echiquier[y][x]
        piece_couleur = self.piece_couleur(piece)

        if piece_couleur is None:
            return []
        
        valid_moves.append(self.tour_mouvements_valides(y, x))
        valid_moves.append(self.fou_mouvements_valides(y, x))
        valid_moves=(valid_moves[0]+valid_moves[1])

        return valid_moves
