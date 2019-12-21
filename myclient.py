from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import thread


class BoxesGame(ConnectionListener):
    def __init__(self):
        pass
        # put something here that will run when you initialize the class
        address = raw_input("Address of Server (localhost:8000): ")
        try:
            if not address:
                host, port = "localhost", 8000
            else:
                host, port = address.split(":")
            self.Connect((host, int(port)))
        except:
            print "Error Connecting to Server: " + host + ":" + port
            print "Usage:", "host:port"
            print "e.g.", "localhost:31425"
            exit()
        print "Client started"

    def update(self):
        connection.Pump()
        self.Pump()
        #sleep to make the game 60fps
        sleep(0.02)

    def send(self, message):
        self.Send({'action': 'myaction', 'message': message})
        #self.update()

    def Network(self, data):
        print 'network data:', data

    def Network_connected(self, data):
        print 'connected to the server'

    def Network_disconnected(self, data):
        print 'disconnected from the server'


    def Network_error(self, data):
        print 'error:', data['error'][1]

    def Network_myaction(self, data):
        print 'myaction:', data


def input_thread(L):
    char = raw_input()
    L.append(char)


def continuous_update():
    L = []
    thread.start_new_thread(input_thread, (L,))

    print("Press [ENTER] to send to server: ")

    while True:
        if L:
            #print(L[0])
            bg.send(L[0])
            #return L[0]
            break
        bg.update()


bg=BoxesGame()
#bg.update()
while 1:
    #bg.update()
    #message = continuous_update()
    continuous_update()
    #message = raw_input("text to send: ")
    #bg.send(message)
    bg.update()
