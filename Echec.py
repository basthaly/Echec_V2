

class Jeu_Echec:
    def __init__(self):
        self.echiquier=[]
        self.tour=0

        for i in range (8):
            J=[]
            for j in range(8):
                J.append(0)
            self.echiquier.append(J)
        
        #Mise en place des pion noir
        self.echiquier[0][0]=(-2) #Tour
        self.echiquier[1][0]=(-3) #Cavalier
        self.echiquier[2][0]=(-4) #Fou
        self.echiquier[3][0]=(-5) #Dame
        self.echiquier[4][0]=(-6) #Roi
        self.echiquier[5][0]=(-4) #Fou
        self.echiquier[6][0]=(-3) #Cavalier
        self.echiquier[7][0]=(-2) #Tour
        for i in range (8):
            self.echiquier[i][1]=(-1) #pion

        #Mise en place des pion blanc
        self.echiquier[0][7]=(2) #Tour
        self.echiquier[1][7]=(3) #Cavalier
        self.echiquier[2][7]=(4) #Fou
        self.echiquier[3][7]=(5) #Dame
        self.echiquier[4][7]=(6) #Roi
        self.echiquier[5][7]=(4) #Fou
        self.echiquier[6][7]=(3) #Cavalier
        self.echiquier[7][7]=(2) #Tour
        for i in range (8):
            self.echiquier[i][1]=(1) #pion

    def __str__(self):
        a="|"
        for i in range(8):
            for j in range(8):
                a=a+" "(self.echiquier[i][j])" |"
            a=a+"/n"
        a=a+"/n"
        return a

    def Tr_pos(pos): #Récupère H4 et renvoie (8,4)
        for i in range (65,72,1):
            if i==ord(pos[0]):
                x=i
                break
        return (x,pos[1]-1)

    def action(self,p1,p2):
        self.tour+=1
        self.echiquier[p2[0]][p2[1]]=self.echiquier[p1[0]][p1[1]]
        self.echiquier[p2[0]][p2[1]]=(0)


##### TEST #####
jeu=Jeu_Echec()
print(jeu)


