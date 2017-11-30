### Jeu de morpion

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import randint

interface=Builder.load_string('''
<Bouton@Button>:
    background_normal: "images/orange.png"

<Interface>:
    BoxLayout:
        canvas.before:
            Color:
                rgba: 63, 127, 191, 1 #vert
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'horizontal' if root.height < root.width else "vertical"
        padding: 20
        spacing: 20
        GridLayout:
            canvas.before:
                Color:
                    rgba: 0.61, 0.238, 0.248, 1 #jaune
                Rectangle:
                    pos: self.pos
                    size: self.size
            rows: 3
            cols: 3
            spacing: 20
            padding: 20
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
                id: bouton_2_1
                on_press: root.joue(self, 2, 1)
            Bouton:
                id: bouton_2_2
                on_press: root.joue(self, 2, 2)
            Bouton:
                id: bouton_2_3
                on_press: root.joue(self, 2, 3)
            Bouton:
                id: bouton_3_1
                on_press: root.joue(self, 3, 1)
            Bouton:
                id: bouton_3_2
                on_press: root.joue(self, 3, 2)
            Bouton:
                id: bouton_3_3
                on_press: root.joue(self, 3, 3)
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
                on_press: root.nouveau_jeu()
''')

class Interface(BoxLayout):

    grille = [['vide', 'vide', 'vide'] for k in range(3)]
    boutons = [[0,0,0] for k in range(3)]
    qui_commence = randint(0, 1)
    jeu_en_cours = False
    a_qui_le_tour = ""

    def __init__(self):
        super(Interface, self).__init__()
        self.ids.message.text = ""
        self.boutons[0][0] = self.ids.bouton_1_1
        self.boutons[0][1] = self.ids.bouton_1_2
        self.boutons[0][2] = self.ids.bouton_1_3
        self.boutons[1][0] = self.ids.bouton_2_1
        self.boutons[1][1] = self.ids.bouton_2_2
        self.boutons[1][2] = self.ids.bouton_2_3
        self.boutons[2][0] = self.ids.bouton_3_1
        self.boutons[2][1] = self.ids.bouton_3_2
        self.boutons[2][2] = self.ids.bouton_3_3
        event = Clock.schedule_interval(self.joue_machine, 2)

    def nouveau_jeu(self):
        # Reinitialisation de la grille
        self.grille = [['vide', 'vide', 'vide'] for k in range(3)]
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

    def joue_machine(self,t):
        ### Joue au hasard
        if self.a_qui_le_tour == "rond" and self.jeu_en_cours:
            fini = False
            while not fini :
                ligne = randint(0,2)
                colonne = randint(0,2)
                if self.grille[ligne][colonne] == "vide":
                    self.grille[ligne][colonne] = "rond"
                    self.boutons[ligne][colonne].background_normal = "images/rond.png"
                    fini = True
            if not self.verifie_gagne():
                self.a_qui_le_tour = "croix"
                self.ids.message.text = "C'est ton tour ..."

    def joue(self, wid, x, y):
        if self.jeu_en_cours and self.a_qui_le_tour == "croix":
            if self.grille[x-1][y-1] == "vide":
                wid.background_normal = "images/croix.png"
                self.grille[x-1][y-1] = "croix"
                self.a_qui_le_tour = "rond"
                self.verifie_gagne()

    def verifie_gagne(self):
        gagne = False
        gagnant = None
        # Verifications horizontales
        if self.grille[0][0] == self.grille[0][1] and  self.grille[0][0] == self.grille[0][2] and  self.grille[0][0] != "vide":
            gagnant = self.grille[0][0]
            gagne = True
        elif self.grille[1][0] == self.grille[1][1] and  self.grille[1][0] == self.grille[1][2] and  self.grille[1][0] != "vide":
            gagnant = self.grille[1][0]
            gagne = True
        elif self.grille[2][0] == self.grille[2][1] and  self.grille[2][0] == self.grille[2][2] and  self.grille[2][0] != "vide":
            gagnant = self.grille[2][0]
            gagne = True
        # Verifications verticales
        elif self.grille[0][0] == self.grille[1][0] and self.grille[0][0] == self.grille[2][0] and  self.grille[0][0] != "vide":
            gagnant = self.grille[0][0]
            gagne = True
        elif self.grille[0][1] == self.grille[1][1] and self.grille[0][1] == self.grille[2][1] and  self.grille[0][1] != "vide":
            gagnant = self.grille[0][1]
            gagne = True
        elif self.grille[0][2] == self.grille[1][2] and self.grille[0][2] == self.grille[2][2] and  self.grille[0][2] != "vide":
            gagnant = self.grille[0][2]
            gagne = True
        # Verifications diagonales
        elif self.grille[0][0] == self.grille[1][1] and self.grille[0][0] == self.grille[2][2] and  self.grille[0][0] != "vide":
            gagnant = self.grille[0][0]
            gagne = True
        elif self.grille[0][2] == self.grille[1][1] and self.grille[0][2] == self.grille[2][0] and  self.grille[0][2] != "vide":
            gagnant = self.grille[0][2]
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
