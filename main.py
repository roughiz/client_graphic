# Jeu de morpion

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import randint


interface = Builder.load_string('''
<Bouton@Button>:
    background_normal: "images/orange.png"

<Interface>:
    BoxLayout:
        canvas.before:
            Color:
                rgba: 63, 63, 191, 1 #vert
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'horizontal' if root.height < root.width else "vertical"
        padding: 10
        spacing: 10
        GridLayout:
            canvas.before:
                Color:
                    rgb: 0, 0,64, 0,12 #jaune
                Rectangle:
                    pos: self.pos
                    size: self.size
            rows: 6
            cols: 7
            spacing: 4
            padding: 4
            Bouton:
                id: bouton_1_1
                on_press: root.joue(self, 1, 1)
            Bouton:
                id: bouton_1_2
                on_press: root.joue(self, 1, 2)
            Bouton:
                id: bouton_1_3
                on_press: root.joue(self, 1, 3)
            Bouton:
                id: bouton_1_4
                on_press: root.joue(self, 1, 4)
            Bouton:
                id: bouton_1_5
                on_press: root.joue(self, 1, 5)
            Bouton:
                id: bouton_1_6
                on_press: root.joue(self, 1, 6)                
            Bouton:
                id: bouton_1_7
                on_press: root.joue(self, 1, 7)
			Bouton:
                id: bouton_2_1
                on_press: root.joue(self, 2, 1)
            Bouton:
                id: bouton_2_2
                on_press: root.joue(self, 2, 2)
            Bouton:
                id: bouton_2_3
                on_press: root.joue(self, 2, 3)
            Bouton:
                id: bouton_2_4
                on_press: root.joue(self, 2, 4)
            Bouton:
                id: bouton_2_5
                on_press: root.joue(self, 2, 5)
            Bouton:
                id: bouton_2_6
                on_press: root.joue(self, 2, 6)                
            Bouton:
                id: bouton_2_7
                on_press: root.joue(self, 2, 7)
            Bouton:
                id: bouton_3_1
                on_press: root.joue(self, 3, 1)
            Bouton:
                id: bouton_3_2
                on_press: root.joue(self, 3, 2)
            Bouton:
                id: bouton_3_3
                on_press: root.joue(self, 3, 3)
            Bouton:
                id: bouton_3_4
                on_press: root.joue(self, 3, 4)
            Bouton:
                id: bouton_3_5
                on_press: root.joue(self, 3, 5)
            Bouton:
                id: bouton_3_6
                on_press: root.joue(self, 3, 6)                
            Bouton:
                id: bouton_3_7
                on_press: root.joue(self, 3, 7)
            Bouton:
                id: bouton_4_1
                on_press: root.joue(self, 4, 1)
            Bouton:
                id: bouton_4_2
                on_press: root.joue(self, 4, 2)
            Bouton:
                id: bouton_4_3
                on_press: root.joue(self, 4, 3)
            Bouton:
                id: bouton_4_4
                on_press: root.joue(self, 4, 4)
            Bouton:
                id: bouton_4_5
                on_press: root.joue(self, 4, 5)
            Bouton:
                id: bouton_4_6
                on_press: root.joue(self, 4, 6)                
            Bouton:
                id: bouton_4_7
                on_press: root.joue(self, 4, 7)
            Bouton:
                id: bouton_5_1
                on_press: root.joue(self, 5, 1)
            Bouton:
                id: bouton_5_2
                on_press: root.joue(self, 5, 2)
            Bouton:
                id: bouton_5_3
                on_press: root.joue(self, 5, 3)
            Bouton:
                id: bouton_5_4
                on_press: root.joue(self, 5, 4)
            Bouton:
                id: bouton_5_5
                on_press: root.joue(self, 5, 5)
            Bouton:
                id: bouton_5_6
                on_press: root.joue(self, 5, 6)                
            Bouton:
                id: bouton_5_7
                on_press: root.joue(self, 5, 7)
            Bouton:
                id: bouton_6_1
                on_press: root.joue(self, 6, 1)
            Bouton:
                id: bouton_6_2
                on_press: root.joue(self, 6, 2)
            Bouton:
                id: bouton_6_3
                on_press: root.joue(self, 6, 3)
            Bouton:
                id: bouton_6_4
                on_press: root.joue(self, 6, 4)
            Bouton:
                id: bouton_6_5
                on_press: root.joue(self, 6, 5)
            Bouton:
                id: bouton_6_6
                on_press: root.joue(self, 6, 6)                
            Bouton:
                id: bouton_6_7
                on_press: root.joue(self, 6, 7)

        BoxLayout:
            canvas.before:
                Color:
                    rgba: 63, 63, 191, 1 #fuschia
                Rectangle:
                    pos: self.pos
                    size: self.size
            orientation: 'vertical'
            padding: 20
            spacing: 20
            Label:
                canvas.before:
                    Color:
                        rgba: 0.56, 0.09, 0.7, 1 #violet
                    Rectangle:
                        pos: self.pos
                        size: self.size
                id: message
                size_hint_y: 0.75
                color: [1,1,1,1]
                text: "A toi de jouer ..."
                font_size: max(self.height, self.width) / 8
                text_size: self.width, None
                halign: 'center'
                valign: 'middle'
            Button:
                background_normal: "images/violet_clair.png"
                text: 'Nouveau jeu'
                font_size: max(self.height, self.width) / 8
                size_hint_y: 0.25
                on_press: root.start_game()
''')


class Interface(BoxLayout):

    def __init__(self):
        super(Interface, self).__init__()
        
        self.BOARDWIDTH = 7
        self.BOARDHEIGHT = 6
        self.ROND = "images/rond.png"
        self.CROIX = "images/croix.png"
        self.board = []
        self.boutons = []
        self.ids.message.text = ""
        self.qui_commence = randint(0, 1)
        self.jeu_en_cours = False
        self.a_qui_le_tour = ""


        # Initialisation
        self.initialisation()

        

        event = Clock.schedule_interval(self.joue_machine, 2)

    def initialisation(self):

    	self.qui_commence = randint(0, 1)
        self.jeu_en_cours = False
        self.a_qui_le_tour = ""
        self.ids.message.text = ""
    	self.board = []
        self.boutons = []
        # Reinitialisation de la board
        # We construct our table with empty cases
        for x in range(self.BOARDWIDTH):
    	     self.board.append([' '] * self.BOARDHEIGHT)
        for x in range(self.BOARDWIDTH):
             self.boutons.append([0] * self.BOARDHEIGHT)
        # self.boutons[colonne][ligne]
        self.boutons[0][0] = self.ids.bouton_1_1
        self.boutons[1][0] = self.ids.bouton_1_2
        self.boutons[2][0] = self.ids.bouton_1_3
        self.boutons[3][0] = self.ids.bouton_1_4
        self.boutons[4][0] = self.ids.bouton_1_5
        self.boutons[5][0] = self.ids.bouton_1_6
        self.boutons[6][0] = self.ids.bouton_1_7

        self.boutons[0][1] = self.ids.bouton_2_1
        self.boutons[1][1] = self.ids.bouton_2_2
        self.boutons[2][1] = self.ids.bouton_2_3
        self.boutons[3][1] = self.ids.bouton_2_4
        self.boutons[4][1] = self.ids.bouton_2_5
        self.boutons[5][1] = self.ids.bouton_2_6
        self.boutons[6][1] = self.ids.bouton_2_7

        self.boutons[0][2] = self.ids.bouton_3_1
        self.boutons[1][2] = self.ids.bouton_3_2
        self.boutons[2][2] = self.ids.bouton_3_3
        self.boutons[3][2] = self.ids.bouton_3_4
        self.boutons[4][2] = self.ids.bouton_3_5
        self.boutons[5][2] = self.ids.bouton_3_6
        self.boutons[6][2] = self.ids.bouton_3_7

        self.boutons[0][3] = self.ids.bouton_4_1
        self.boutons[1][3] = self.ids.bouton_4_2
        self.boutons[2][3] = self.ids.bouton_4_3
        self.boutons[3][3] = self.ids.bouton_4_4
        self.boutons[4][3] = self.ids.bouton_4_5
        self.boutons[5][3] = self.ids.bouton_4_6
        self.boutons[6][3] = self.ids.bouton_4_7

        self.boutons[0][4] = self.ids.bouton_5_1
        self.boutons[1][4] = self.ids.bouton_5_2
        self.boutons[2][4] = self.ids.bouton_5_3
        self.boutons[3][4] = self.ids.bouton_5_4
        self.boutons[4][4] = self.ids.bouton_5_5
        self.boutons[5][4] = self.ids.bouton_5_6
        self.boutons[6][4] = self.ids.bouton_5_7

        self.boutons[0][5] = self.ids.bouton_6_1
        self.boutons[1][5] = self.ids.bouton_6_2
        self.boutons[2][5] = self.ids.bouton_6_3
        self.boutons[3][5] = self.ids.bouton_6_4
        self.boutons[4][5] = self.ids.bouton_6_5
        self.boutons[5][5] = self.ids.bouton_6_6
        self.boutons[6][5] = self.ids.bouton_6_7

    def start_game(self):

        self.initialisation()
        #self.board = [[' ', ' ', ' '] for k in range(4)]
        for item in self.boutons:
            for b in item:
                b.background_normal = "images/orange.png"
        self.qui_commence = randint(0, 1)
        self.jeu_en_cours = True
        # Premier coup
        if self.qui_commence == 0:
            # la machine commence
            self.a_qui_le_tour = "rond"
            self.joue_machine(0)
            self.ids.message.text = "C'est ton tour ..."
            self.a_qui_le_tour = "croix"
        else:
            # l'utilisateur commence
            self.a_qui_le_tour = "croix"
            self.ids.message.text = "C'est toi qui commence ..."

    def joue_machine(self, t):
        # Joue au hasard
        if self.a_qui_le_tour == "rond" and self.jeu_en_cours:
            fini = False
            while not fini:
                ligne = randint(0, 5)
                colonne = randint(0, 6)
                if self.board[colonne][ligne] == " ":
                    self.board[colonne][ligne] = "rond"
                    self.boutons[colonne][ligne].background_normal = "images/rond.png"
                    fini = True
            if not self.verifie_gagne():
                self.a_qui_le_tour = "croix"
                self.ids.message.text = "C'est ton tour ..."

    def joue(self, wid, x, y):
        if self.jeu_en_cours and self.a_qui_le_tour == "croix":
            if self.board[y - 1][x - 1] == " ":
            	print("ligne"+str(x)+"colonne:"+str(y))
                wid.background_normal = "images/croix.png"
                self.board[y - 1][x - 1] = "croix"
                self.a_qui_le_tour = "rond"
                self.verifie_gagne()

    def verifie_gagne(self):
        gagne = False
        gagnant = None
        # Verifications horizontales
        if self.board[0][0] == self.board[0][1] and self.board[0][0] == self.board[0][2] and self.board[0][0] != " ":
            gagnant = self.board[0][0]
            gagne = True
        elif self.board[1][0] == self.board[1][1] and self.board[1][0] == self.board[1][2] and self.board[1][0] != " ":
            gagnant = self.board[1][0]
            gagne = True
        elif self.board[2][0] == self.board[2][1] and self.board[2][0] == self.board[2][2] and self.board[2][0] != " ":
            gagnant = self.board[2][0]
            gagne = True
        # Verifications verticales
        elif self.board[0][0] == self.board[1][0] and self.board[0][0] == self.board[2][0] and self.board[0][0] != " ":
            gagnant = self.board[0][0]
            gagne = True
        elif self.board[0][1] == self.board[1][1] and self.board[0][1] == self.board[2][1] and self.board[0][1] != " ":
            gagnant = self.board[0][1]
            gagne = True
        elif self.board[0][2] == self.board[1][2] and self.board[0][2] == self.board[2][2] and self.board[0][2] != " ":
            gagnant = self.board[0][2]
            gagne = True
        # Verifications diagonales
        elif self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] != " ":
            gagnant = self.board[0][0]
            gagne = True
        elif self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[0][2] != " ":
            gagnant = self.board[0][2]
            gagne = True
        if gagne:
            self.jeu_en_cours = False
            if gagnant == "rond":
                self.ids.message.text = "Je gagne !!!"
            else:
                self.ids.message.text = "Bravo ! Tu gagnes !!!"
        return gagne


class Morpion(App):

    def build(self):
        return Interface()


Morpion().run()
