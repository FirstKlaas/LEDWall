from sender import Sender
from color import Color
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print "Connected with result code " + str(rc)
    client.subscribe("$SYS/#")
    client.loop_start()

class MqttSender(Sender):
    def __init__(self, server='nebuhr', port=1883):
        Sender.__init__(self)
        self._server = server
        self._port   = port
        self._client = mqtt.Client()

        self._client.on_connect = on_connect
        self._client.on_message = self._on_message
        self._client.connect(server, port, 60)

    # The callback for when the client receives a CONNACK response from the server.
    def _on_connect(self, client, userdata, flags, rc):
        print "Connected with result code " + str(rc)
        client.subscribe("$SYS/#")
        client.loop_start()

    # The callback for when a PUBLISH message is received from the server.
    def _on_message(self, client, userdata, msg):
        print(msg.topic)

    def update(self):
        if not self._sendbuffer: 
            raise ValueError('Not initialized')

        self._sendbuffer[0] = Sender.CMD_SHOW
        ''' 
        for i in range(len(self.panel._data)):
            self._sendbuffer[i+1] = Color.gammaCorrection(self.panel._data[i]) if self.panel.gammaCorrection else self.panel._data[i]
  
        self._client.publish(self.panel.id,self._sendbuffer)
        '''
        offset = 0
        for c in self.panel:
            self._setPixel(offset,Color.gammaCorrection(c[0]),Color.gammaCorrection(c[1]),Color.gammaCorrection(c[2]))
            offset += 3
        self._client.publish(self.panel.id,bytearray([Sender.CMD_SHOW]))        
        
    def _setPixel(self,offset,r,g,b):
        high = (offset >> 8) & 0xff
        low  = offset & 0xff 

        self._client.publish(self.panel.id,bytearray([Sender.CMD_SET_PIXEL,high,low,r,g,b]))
        
    def raw_write(self, offset, data):
        size = len(data)
        print self.panel.byteCount
        if offset >= self.panel.byteCount:
            raise ValueError("Offset to high")
        if offset < 0:
            raise ValueError("Offset may not be negative")
        if (offset + size) > self.panel.byteCount:
            raise ValueError("Data exeeds buffer size")

        #TODO Max Payload Size testen        
        buf = [Sender.CMD_WRITE_RAW, offset >> 8, offset & 0xff, size >> 8, size & 0xff ] + [x for x in data]
        print buf
        self._client.publish(self.panel.id,bytearray(buf))

    def raw_show(self):
        self._client.publish(self.panel.id,bytearray([Sender.CMD_SHOW]))  

    def init(self,panel):
        print ('Init')
        Sender.init(self,panel)
        self._sendbuffer = bytearray(3*self.panel.count+1)
        print "sendbuffer with length  {:d} erzeugt.".format(len(self._sendbuffer))
        data = bytearray([1,self.panel.columns,self.panel.rows])
        self._client.publish(self.panel.id,data)
        #client.loop_forever()
