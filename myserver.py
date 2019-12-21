import PodSixNet.Channel
import PodSixNet.Server
from time import sleep


class ClientChannel(PodSixNet.Channel.Channel):
    #def Network(self, data):
    #    print data

    def Network_myaction(self, data):
        #print 'myaction:', data
        print 'myaction:', data['message']


class GameServer(PodSixNet.Server.Server):

    channelClass = ClientChannel

    def Connected(self, channel, addr):
        print 'new connection:', channel


address = raw_input("Host:port (localhost:8000): ")
if not address:
    host, port = "localhost", 8000
    print "STARTING SERVER ON LOCALHOST"
else:
    host, port = address.split(":")
    print "STARTING SERVER ON", host
gameServe = GameServer(localaddr=('localhost', 8000))
while True:
    gameServe.Pump()
    sleep(0.01)