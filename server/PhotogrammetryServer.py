import SocketServer
import Photogrammetry
import ast

class PhotogrammetryServer(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self): #TODO
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        #options = ast.literal_eval(data)
        #actions = options['actions']
        #url = options['url']
        
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
        #self.request.send(self.data.upper())
