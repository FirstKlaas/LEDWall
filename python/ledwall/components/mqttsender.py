from sender import Sender
from color import Color
import paho.mqtt.client as mqtt
from socket import error as SocketError

def on_connect(client, userdata, flags, rc):
    print "Connected with result code " + str(rc)
    client.subscribe("$SYS/#")
    client.loop_start()

def on_message(self, client, userdata, msg):
    print(msg.topic)

class MqttSender(Sender):
    def __init__(self, server='nebuhr', port=1883):
        Sender.__init__(self)
        self._server = server
        self._port   = port
        self._client = mqtt.Client()

        self._client.on_connect = on_connect
        self._client.on_message = on_message

        #self._client.connect(server, port, 60)

    # The callback for when a PUBLISH message is received from the server.

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
        self._publish([Sender.CMD_SHOW] + self._frame_number)        
        
    def _setPixel(self,offset,r,g,b):
        self._publish([Sender.CMD_SET_PIXEL] + self.itob(offset) + self._frame_number + [r,g,b])
        
    def raw_write(self, offset, data):
        size = len(data)
        print self.panel.byteCount
        if offset >= self.panel.byteCount:
            raise ValueError("Offset to high")
        if offset < 0:
            raise ValueError("Offset may not be negative")
        if (offset + size) > self.panel.byteCount:
            raise ValueError("Data exeeds buffer size")

        self._publish([Sender.CMD_WRITE_RAW] + self.itob(offset) + self.itob(size) + [x for x in data])

    def raw_show(self):
        self._publish([Sender.CMD_SHOW] + self._frame_number)  

    def init(self,panel):
        print ('Init')
        Sender.init(self,panel)
        self._sendbuffer = bytearray(3*self.panel.count+1)
        self._publish([1,self.panel.columns,self.panel.rows]+self._frame_number)

    def _publish(self, data):
        try:
            self._client.publish(self.panel.id,bytearray(buf))
        except SocketError:
            print "Could not send data."

    def itob(self, value):
        return [(value >> 8) & 0xFF, value & 0xFF]

    @property
    def _frame_number(self):
        return self.itob(self.panel.frame)