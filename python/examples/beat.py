#!/usr/bin/env python3

import sys
sys.path.append('..')

import paho.mqtt.client as mqtt
from random import randint

import ledwall.components as comp
import ledwall.geometry as cgeo

MQTT_HOST = "192.168.178.77"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "/hexahive/data"

d = comp.Display(7,7,comp.UDPSender( server='LEDPanel-ONE'))
#d = comp.Display(7,7,comp.ConsoleSender())
mqttc = mqtt.Client()

sensor_names = {
	'28:ff:b4:6c:51:17:4:a9' : '#1 Innen (3/4)',
	'28:ff:6a:b3:50:17:4:65' : '#2 Innenliegend/Aussenwand',
	'28:ff:6:2e:50:17:4:29'  : '#3 Innen (4/5)',
	'28:ff:c1:86:50:17:4:ef' : '#4 Aussentemperatur'
}

AUSSEN_SENSOR_ADDR = '28:ff:c1:86:50:17:4:ef'

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

mqttc.on_connect = on_connect

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

class AnimClass(comp.Application):

        def __init__(self):
                super().__init__(d,25)
                self._color_beat = comp.HSVColor(0.08)
                self._border = cgeo.Rectangle(2,2,3,3)
                mqttc.loop_start()

                mqttc.on_message = self.on_message


        def on_message(self,client, userdata, msg):
            data  = msg.payload.decode('utf-8').split('/')
            value = data[1]
            addr  = data[0]
            if addr == AUSSEN_SENSOR_ADDR:
                self._color_beat.value = 1.0
                print(value)

        def paint(self):
                self.display.fill_rect(*tuple(self._border),self._color_beat)
                if self._color_beat.value > 0.01:
                    self._color_beat.value += 0.99

app = AnimClass()
app.start_loop()
