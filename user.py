
class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.roomId = -1
        self.color = ""
        self.available_color = ['X', 'O', '=']
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setRoomId(self, roomId):
        self.roomId = roomId
    
    def SetColor(self, color):
        self.color = color
