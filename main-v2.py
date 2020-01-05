# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import randint
from stream import Stream
from room import Room
from user import User
import FourinarowAI

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
            rows: 7
            cols: 5
            spacing: 5
            padding: 5
            Bouton:
                id: bouton_1_1
            Bouton:
                id: bouton_1_2
            Bouton:
                id: bouton_1_3
            Bouton:
                id: bouton_1_4
            Bouton:
                id: bouton_1_5

			Bouton:
                id: bouton_2_1
            Bouton:
                id: bouton_2_2
            Bouton:
                id: bouton_2_3
            Bouton:
                id: bouton_2_4
            Bouton:
                id: bouton_2_5

            Bouton:
                id: bouton_3_1
            Bouton:
                id: bouton_3_2
            Bouton:
                id: bouton_3_3
            Bouton:
                id: bouton_3_4
            Bouton:
                id: bouton_3_5

            Bouton:
                id: bouton_4_1
            Bouton:
                id: bouton_4_2
            Bouton:
                id: bouton_4_3
            Bouton:
                id: bouton_4_4
            Bouton:
                id: bouton_4_5

            Bouton:
                id: bouton_5_1
            Bouton:
                id: bouton_5_2
            Bouton:
                id: bouton_5_3
            Bouton:
                id: bouton_5_4
            Bouton:
                id: bouton_5_5

            Bouton:
                id: bouton_6_1
            Bouton:
                id: bouton_6_2
            Bouton:
                id: bouton_6_3
            Bouton:
                id: bouton_6_4
            Bouton:
                id: bouton_6_5
            Bouton:
                id: bouton_7_1
                on_press: root.joue(self, 1)
            Bouton:
                id: bouton_7_2
                on_press: root.joue(self, 2)
            Bouton:
                id: bouton_7_3
                on_press: root.joue(self, 3)
            Bouton:
                id: bouton_7_4
                on_press: root.joue(self, 4)
            Bouton:
                id: bouton_7_5
                on_press: root.joue(self, 5)
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 63, 63, 191, 1 #fuschia
                Rectangle:
                    pos: self.pos
                    size: self.size
            orientation: 'vertical'
            padding: 2
            spacing: 2
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
                text: "Authentifiez vous pour jouer .."
                font_size: max(self.height, self.width) / 8
                text_size: self.width, None
                halign: 'center'
                valign: 'middle'    
            TextInput:
                id: login
                #text: root.textinputtext
                hint_text: "login"
                size_hint_y: 0.2
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            TextInput:
                id: password
                #text: root.textinputtext
                hint_text: "password"   
                #password = "True
            Button:
                id: deleg
                background_normal: "images/violet_clair.png"
                text: 'Déléguer '
                font_size: max(self.height, self.width) / 16
                size_hint_y: 0.15
                on_press: root.automatic_playe()    
            Button:
                id: jouer
                background_normal: "images/violet_clair.png"
                text: 'Jouer'
                font_size: max(self.height, self.width) / 8
                size_hint_y: 0.25
                on_press: root.authentication()
''')


class Interface(BoxLayout):

    def __init__(self):
        super(Interface, self).__init__()
        
        self.IP = '212.47.247.190'
        self.PORT = 4444
        self.BOARDWIDTH = 5
        self.BOARDHEIGHT = 6
        self.ROND = "images/rond.png"
        self.RONDG = "images/rond2.png"
        self.CROIX = "images/croix.png"
        self.CROIXG = "images/croix2.png"
        self.EGAL = "images/egal.png"
        self.DEFAULT_BACK = "images/orange.png"
        self.SERV_FLAG = ""
        self.serv_tile = "S"
        self.client_tile = ""
        self.CLIENT_FLAG = ""
        self.WIN_CLI_FLAG = ""
        self.WIN_SRV_FLAG  = ""
        self.board = []
        self.boutons = []
        self.ids.message.text = ""
        self.qui_commence = randint(0, 1)
        self.jeu_en_cours = False
        self.a_qui_le_tour = ""
        self.push_boutns=[]
        self.user = None
        self.room = None
        self.stream = None


        # Initialisation
        self.initialisation()

        

        event = Clock.schedule_interval(self.joue_machine, 2)

    def initialisation(self):
        #self.qui_commence = randint(0, 1)
        #self.jeu_en_cours = False
        self.a_qui_le_tour = ""
        self.ids.message.text = ""
        self.board = []
        self.boutons = []
        self.push_boutns=[]
        # Reinitialisation de la board
        # We construct our table with empty cases
        for x in range(self.BOARDWIDTH):
    	     self.board.append([' '] * self.BOARDHEIGHT)
        for x in range(self.BOARDWIDTH):
             self.boutons.append([0] * self.BOARDHEIGHT)
        for x in range(self.BOARDWIDTH):
        	 self.push_boutns.append(0)

        # self.boutons[colonne][ligne]
        self.boutons[0][0] = self.ids.bouton_1_1
        self.boutons[1][0] = self.ids.bouton_1_2
        self.boutons[2][0] = self.ids.bouton_1_3
        self.boutons[3][0] = self.ids.bouton_1_4
        self.boutons[4][0] = self.ids.bouton_1_5

        self.boutons[0][1] = self.ids.bouton_2_1
        self.boutons[1][1] = self.ids.bouton_2_2
        self.boutons[2][1] = self.ids.bouton_2_3
        self.boutons[3][1] = self.ids.bouton_2_4
        self.boutons[4][1] = self.ids.bouton_2_5

        self.boutons[0][2] = self.ids.bouton_3_1
        self.boutons[1][2] = self.ids.bouton_3_2
        self.boutons[2][2] = self.ids.bouton_3_3
        self.boutons[3][2] = self.ids.bouton_3_4
        self.boutons[4][2] = self.ids.bouton_3_5

        self.boutons[0][3] = self.ids.bouton_4_1
        self.boutons[1][3] = self.ids.bouton_4_2
        self.boutons[2][3] = self.ids.bouton_4_3
        self.boutons[3][3] = self.ids.bouton_4_4
        self.boutons[4][3] = self.ids.bouton_4_5

        self.boutons[0][4] = self.ids.bouton_5_1
        self.boutons[1][4] = self.ids.bouton_5_2
        self.boutons[2][4] = self.ids.bouton_5_3
        self.boutons[3][4] = self.ids.bouton_5_4
        self.boutons[4][4] = self.ids.bouton_5_5

        self.boutons[0][5] = self.ids.bouton_6_1
        self.boutons[1][5] = self.ids.bouton_6_2
        self.boutons[2][5] = self.ids.bouton_6_3
        self.boutons[3][5] = self.ids.bouton_6_4
        self.boutons[4][5] = self.ids.bouton_6_5

        self.push_boutns[0] = self.ids.bouton_7_1
        self.push_boutns[1] = self.ids.bouton_7_2
        self.push_boutns[2] = self.ids.bouton_7_3
        self.push_boutns[3] = self.ids.bouton_7_4
        self.push_boutns[4] = self.ids.bouton_7_5
        ## Mise en place du background-image  pour les boutons push
        for item in self.push_boutns:
                item.background_normal = "images/3.jpeg"
    def start_game(self):

        self.initialisation()
        #self.board = [[' ', ' ', ' '] for k in range(4)]
        for item in self.boutons:
            for b in item:
                b.background_normal = self.DEFAULT_BACK

        # quel jouer joue en premier en mets ici que c'est le client en statique (voir après)
        self.qui_commence = 1
        # si c'est la machine qui joue en premier
        if self.qui_commence == 0:
            # la machine commence
            self.a_qui_le_tour = "serveur"
            self.joue_machine(0)
            self.ids.message.text = "Le serveur joue"
            self.a_qui_le_tour = "client"
        else:
            # l'utilisateur commence
            self.a_qui_le_tour = "client"
            self.ids.message.text = "Le client commence la partie"

    def define_user_flag(self):
        if self.user.color == 'X':
            self.CLIENT_FLAG = self.CROIX
            self.client_tile = "x"
            self.SERV_FLAG = self.ROND
            self.WIN_CLI_FLAG = self.CROIXG
            self.WIN_SRV_FLAG = self.RONDG
        elif self.user.color == 'O':
            self.CLIENT_FLAG = self.ROND
            self.client_tile = "o"
            self.SERV_FLAG = self.CROIX
            self.WIN_CLI_FLAG = self.RONDG
            self.WIN_SRV_FLAG = self.CROIXG
        elif self.user.color == '=':
            self.CLIENT_FLAG = self.EGAL
            self.client_tile = "="  
            self.SERV_FLAG = self.ROND 

    def get_flags(self,tile):
        if tile == self.client_tile:
            return self.CLIENT_FLAG
        elif tile == ' ':
            return self.DEFAULT_BACK
        else:
            self.serv_tile = tile
            return self.SERV_FLAG     
             

    def authentication(self):
        if self.jeu_en_cours:
            self.ids.message.text = "Une partie est déja en cours "
            return
        if self.ids.login.text == "" or self.ids.password.text=="":
            self.ids.message.text = "Veuillez remplir les champs"
        else:
            self.user = User(self.ids.login.text,self.ids.password.text)
            self.stream =  Stream(self.IP, self.PORT, self.user)
            self.ids.message.text = ""
            self.stream.isAuthentified = True
            if self.stream.isAuthentified :
                self.user.color = 'X'
                self.define_user_flag()
                self.ids.message.text = "Authentification réussie"
                self.ids.password.text = ""
                self.ids.login.text = ""
                self.jeu_en_cours = True
                self.start_game()

    def drawBoard(self,board):
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                self.boutons[x][y].background_normal= self.get_flags(board[x][y])
               
    def joue_machine(self, t):
        # Joue au hasard
        if self.a_qui_le_tour == "serveur" and self.jeu_en_cours:
            fini = False
            while not fini:
                ## normalement on récupère le board duu serveur apres qu'ila jouer 
                # new_board = self.stream.get_boad()
                #fini = True
                ##Vérifier que labord récupéré est de la même taille que la notre 
                #if len(new_board) == len(self.board) and len(new_board[0]) == len(self.board[0]):
                    #self.board = new_board
                    #self.drawBaoard(self.board)
                colonne = randint(0, 4)
                for y in range(self.BOARDHEIGHT-1, -1, -1):
                    if self.board[colonne][y] == ' ':
                        self.board[colonne][y] = self.serv_tile
                        self.boutons[colonne][y].background_normal = self.SERV_FLAG
                        fini = True
                        break
            #if not self.verifie_gagne():
            if not self.isWinner(self.board, self.serv_tile,self.boutons,self.WIN_SRV_FLAG):
                self.a_qui_le_tour = "client"
                self.ids.message.text = "à vous de jouer "
            else:
                self.ids.message.text = "Le serveur gagne !!!"
                self.jeu_en_cours = False

    def automatic_playe(self):
        if self.jeu_en_cours and self.a_qui_le_tour == "client": 
            # recupérer un move à partir de l'IA
            move,select=FourinarowAI.getBestMove(self.board,self.client_tile,self.serv_tile,5)
            self.makeMove(self.board, self.boutons, self.client_tile,self.CLIENT_FLAG, move)
            ##envoyer le move
            #self.stream.move(move)
            if not self.isWinner(self.board, self.client_tile,self.boutons,self.WIN_CLI_FLAG):
                   self.a_qui_le_tour = "serveur"
                   self.ids.message.text = "C'est le tour du serveur "
            else:
                   self.ids.message.text = "Je gagne !!!"
                   self.jeu_en_cours = False                

    def joue(self, wid, move):
        if self.jeu_en_cours and self.a_qui_le_tour == "client":  
            if self.isValidMove(self.board,move-1):
                ##envoyer le move
                #self.stream.move(move)
                self.makeMove(self.board, self.boutons, self.client_tile,self.CLIENT_FLAG, move-1)
                #self.a_qui_le_tour = "serveur"
                #self.verifie_gagne()
                if not self.isWinner(self.board, self.client_tile,self.boutons,self.WIN_CLI_FLAG):
                   self.a_qui_le_tour = "serveur"
                   self.ids.message.text = "C'est le tour du serveur "
                else:
                   self.ids.message.text = "Je gagne !!!"
                   self.jeu_en_cours = False

    def makeMove(self,board, boutons, player, player_flag, column):
    # this function parse column x choosen by user and put it at the first empty column, the loop parse from the head to the bottom
	    for y in range(self.BOARDHEIGHT-1, -1, -1):
		    if board[column][y] == ' ':
			    board[column][y] = player
			    boutons[column][y].background_normal = player_flag
			    return

    def isValidMove(self,board, move):
		    # This function verify if the move input is in the interval [0-width] and the head of column table is not emty else return false
        if move < 0 or move >= (self.BOARDWIDTH):
              return False

        if board[move][0] != ' ':
              return False
        return True            

    def isBoardFull(self,board):
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
               if board[x][y] == ' ':
                  return False
        return True

    # check if the player is winner (diagonal , horizontal vertical ) 4 respectively tile 
    def isWinner(self,board, tile,boutons,win_flag):
    # check horizontal spaces
        for y in range(self.BOARDHEIGHT):
        # check if 4 tile are respectively egal a tile in horizontal space 
            for x in range(self.BOARDWIDTH - 3):
                if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                  for i in range(0,4):
                    boutons[x+i][y].background_normal = win_flag
                  return True

    # check vertical spaces
        for x in range(self.BOARDWIDTH):
          # check if 4 tile are respectively egal a tile in vertical space 
            for y in range(self.BOARDHEIGHT - 3):
                if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                  for i in range(0,4): 
                    boutons[x][y+i].background_normal = win_flag
                  return True

        # check / diagonal spaces
        for x in range(self.BOARDWIDTH - 3):
             for y in range(3, self.BOARDHEIGHT):
                 if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                   for i in range(0,4): 
                      boutons[x+i][y-i].background_normal = win_flag
                   return True

        # check \ diagonal spaces
        for x in range(self.BOARDWIDTH - 3):
            for y in range(self.BOARDHEIGHT - 3):
                if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                  for i in range(0,4): 
                    boutons[x+i][y+i].background_normal = win_flag
                  return True

        return False
class Game(App):

    def build(self):
        return Interface()

Game().run()
    
