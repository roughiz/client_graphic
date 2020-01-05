# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from room import Room
from user import User

class Stream(object):

    def __init__(self, ip, port, user):
        self.ip = ip
        self.port = port
        self.user = user
        self.sock = None
        self.isAuthentified = False

    def connect_to_server(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        try:
            self.sock.connect((self.ip, self.port))
        except socket.error:
            print('La connection avec le serveur a echoué')

    def negociate_version(self, version):
        self.sock.send(('VERSION:'+version).encode())
        version = self.sock.recv(1024)
        return version.decode("ascii").split(':')[1]

    def parse_rooms(self, rooms):
        if not rooms.startswith('ROOM'):
            print("Error doesn't startswith")
            return None
        rooms_info = rooms.strip().split('ROOM:')[1:]
        rooms = []
        for room_info in rooms_info:
            if 'SUCCESS' in room_info:
                room_info = room_info.replace('SUCCESS:Rooms sent', '')
                fields = room_info.split(',')
                print(fields)
                rooms.append(Room(fields[0], fields[1], fields[2]))
        return rooms

    def create_account(self):
        self.sock.send(('CREATE_ACCOUNT:'+self.user.getUsername()+',PASSWORD:'+self.user.getPassword()).encode())
        response = self.sock.recv(1024).decode("ascii")
        print(response)
        if response == 'CONFIRM_ACCOUNT':
            self.sock.send(('CONFIRM_ACCOUNT:' + self.user.getUsername()
                            + ',PASSWORD:' + self.user.getPassword()).encode())
            response = self.sock.recv(1024).decode("ascii")
            print(response)
            if response == 'SUCCESS:ACCOUNT_CREATED':
                rooms = self.sock.recv(1024).decode("ascii")
                while 'SUCCESS' not in rooms and 'ERROR' not in rooms:
                    rooms += self.sock.recv(1024).decode("ascii")
                if 'ERROR' not in rooms:
                    print(rooms)
                    return self.parse_rooms(rooms)

            elif 'SUCCESS' in response:
                rooms = response.replace('SUCCESS:AUTHENTICATED', '')
                while 'SUCCESS'.encode() not in rooms:
                    rooms += self.sock.recv(1024).decode("ascii")
                if 'ERROR' not in rooms:
                    print(rooms)
                    return self.parse_rooms(rooms)
        return False

    def auth(self):
        self.sock.send(('PASSWORD:'+self.user.getPassword()).encode())
        response = self.sock.recv(1024).decode("ascii")
        print(response)

        if response == 'SUCCESS:AUTHENTICATED':
            self.isAuthentified = True
            rooms = self.sock.recv(1024).decode("ascii")
            while 'SUCCESS' not in rooms and 'ERROR' not in rooms:
                rooms += self.sock.recv(1024).decode("ascii")
            if 'ERROR' not in rooms:
                print(rooms)
                return self.parse_rooms(rooms)

        elif 'SUCCESS' in response:
            self.isAuthentified = True
            rooms = response.replace('SUCCESS:AUTHENTICATED', '')
            while 'SUCCESS'.encode() not in rooms:
                rooms += self.sock.recv(1024).decode("ascii")
            if 'ERROR' not in rooms:
                print(rooms)
                return self.parse_rooms(rooms)
        return None

    def login(self):
        self.sock.send(('LOGIN:' + self.user.getUsername()).encode())
        response = self.sock.recv(1024).decode()
        print(response)
        if response == 'UNKNOWN_LOGIN':
            self.create_account()
        elif response == 'ASK_PASSWORD':
            self.auth()

    def getSock(self):
        return self.sock

    def create_room(self):
        self.sock.send('CREATE_ROOM'.encode())
        response = self.sock.recv(1024).decode("ascii")
        print(response)
        if 'SUCCESS:' in response:
            try:
                id = int(response.split(':')[1])
                self.user.setRoomId(id)
                return True
            except ValueError:
                print('CREATE_ROOM: id value is not an integer')
                return False
        else:
            print("Room couldn't be created")

    def join_room(self, Id):
        self.sock.send(('SELECT_ROOM:%d' % Id).encode())
        response = self.sock.recv(1024).decode("ascii")
        if 'SUCCESS:' in response:
            print('Room %d joined' % Id)
        else:
            print("Room couldn't be joined")

    def get_color(self):
        color_response = self.sock.recv(1024).decode("ascii")
        if color_response.upper() in user.available_color:
            self.user.SetColor(color_response.upper())
            print("Color %s used" % color_response)
        else:
            print("Color not valid")

    def begin(self):
        begin_result = self.sock.recv(1024).decode("ascii")
        print("The first player to play is %s" % begin_result)

    # Return the board -> [Size, [[Line 1], [Line 2], [...]]]
    def get_board(self):
        raw_board = self.sock.recv(1024).decode("ascii").split(',')
        final_board = [int(raw_board.pop(0)), []]

        temp_board = []
        for line in range(0,len(raw_board), final_board[0]):
            for column in range(line,line+final_board[0]):
                temp_board.append(raw_board[column])
            final_board[1].append(temp_board)
            temp_board = []

        return final_board

    def move(self, column):
        move_order = self.sock.recv(1024).decode("ascii")
        if "MOVE" in move_order:
            self.sock.send(('MOVE:%d' % column).encode())

    def quit_room(self):
        self.sock.send('QUIT_ROOM'.encode())
        response = self.sock.recv(1024).decode("ascii")
        if 'SUCCESS:' in response:
            print('ROOM EXITED')
            return True
        else:
            print('Error exiting room')
            return False

    def quit_server(self):
        self.sock.send('QUIT_SERVER'.encode())
        self.getSock().close()
        exit(0)

    # Return list of player
    def ask_player_list(self):
        self.sock.send('ASK_LIST'.encode())
        response = self.sock.recv(1024).decode("ascii")
        if 'LIST:' in response:
            return response.split('LIST:')[1].split(',')
        return False

    def query_login(self, pseudo):
        self.sock.send(('QUERY_LOGIN:%s' % pseudo).encode())
        response = self.sock.recv(1024).decode("ascii")
        if 'LOGIN_INFO:' in response:
            return response.split('LOGIN_INFO:')[1].split(',')
        print("ERROR: User doesn't exist")
        return False

if __name__ == '__main__':
    usr = User('yacine6', 'password')
    stream = Stream('212.47.247.190', 4444, usr)
    stream.connect_to_server()
    print(stream.negociate_version('1.0'))
    stream.login()
    stream.create_room()
    stream.join_room(stream.user.roomId)
    stream.get_color()
    print(stream.get_board())
    stream.getSock().close()
