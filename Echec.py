#!/usr/bin/python
# -*-coding:Latin-1 -* 

"""
Dans ce programme, les pièces d'échecs sont représentées par des entiers sur l'échiquier.
Les pièces blanches ont des valeurs positives, tandis que les pièces noires ont des valeurs négatives.
Les valeurs absolues des entiers correspondent aux pièces comme suit :

1 (ou -1) : Pion
2 (ou -2) : Tour
3 (ou -3) : Cavalier
4 (ou -4) : Fou
5 (ou -5) : Dame
6 (ou -6) : Roi

Les cases vides de l'échiquier sont représentées par le chiffre 0.
Ainsi, chaque case de l'échiquier contient un entier.
Cette entier indique la pièce présente sur cette case et la couleur de cette pièce (positive pour les Blancs, négative pour les Noirs).
"""

class Jeu_Echec:
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

    def Tr_pos(self,pos): #Récupère H4 et renvoie (8,4)
        for i in range (65,73):
            if chr(i)==pos[0]:
                # x=i-65
                x = 72 - ord(pos[0])
                break
        return (x,int(pos[1])-1)

    def est_dans_echiquier(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    # def action(self,p1,p2):
    #     self.tour+=1
    #     self.echiquier[p2[0]][p2[1]]=self.echiquier[p1[0]][p1[1]]
    #     self.echiquier[p1[0]][p1[1]]=(0)
    
    def action(self, p1, p2, joueur):
        if self.echiquier[p1[0]][p1[1]] * joueur > 0:  # Vérifie si la pièce appartient au joueur actuel
            self.tour += 1
            self.echiquier[p2[0]][p2[1]] = self.echiquier[p1[0]][p1[1]]
            self.echiquier[p1[0]][p1[1]] = 0
            self.joueur = -joueur  # Change le joueur actuel
        else:
            print("C'est au tour du joueur", joueur, "de jouer.")

    def deplac(self,p1,p2):
        pos1=self.Tr_pos(p1)
        pos2=self.Tr_pos(p2)
        self.action(pos1,pos2)



# Exemple d'utilisation
if __name__ == "__main__":
    jeu = Jeu_Echec()
    print(jeu)

    # Effectuer un déplacement
    jeu.deplac("A1", "A2")
    print(jeu)


