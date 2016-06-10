# -*- coding: utf-8 -*-


import copy
from struct import unpack
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


clients = []

sps_pps_tag = bytearray('')


class FlvServer(WebSocket):

    def handleMessage(self):

        if len(self.data) < 11:

            print 'invalid message ', self.data

            return

        tagType = self.data[0] & 0xff
        datasize = struct.unpack('!i',self.data[0:4]) & 0xffffff
        timestamp = struct.unpack('!i',self.data[3:7]) & 0xffffff


        print 'tagType ',tagType, ' datsize  ', datasize ,' timestamp  ', timestamp


        if tagType == 9 and self.data[12]  == 0:

            print 'this is sequence header '
            print 'datasize = ', datasize
            print 'timestamp = ', timestamp

            sps_pps_tag = copy.deepcopy(self.data)

        for client in clients:

            if client != self:

                client.sendMessage(self.data)

                print 'handleMessage: ', type(self.data)


    def handleConnected(self):

        print self.address, 'connected'

        if len(sps_pps_tag) > 0:
            self.sendMessage(self.sps_pps_tag)

        clients.append(self)


    def handleClose(self):

        clients.remove(self)

        print self.address, 'closed'


server = SimpleWebSocketServer('', 8000, FlvServer)
server.serveforever()

