#!/usr/bin/env python3

import sys
sys.path.append('..')

import math
import paho.mqtt.client as mqtt
from random import randint

import ledwall.components as comp
import ledwall.geometry as cgeo

import ledwall.components.sprite as sprite

MQTT_HOST = "192.168.178.77"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "/hexahive/data"

cm = sprite.ColorMap()
number_color = comp.HSVColor()

cm += ('x', number_color)

ziffern_sprites = [
    sprite.Sprite([
        "xxx",
        "x.x",
        "x.x",
        "x.x",
        "xxx"
    ],cm),

    sprite.Sprite([
        ".x.",
        ".x.",
        ".x.",
        ".x.",
        ".x."
    ],cm),

    sprite.Sprite([
        "xxx",
        "..x",
        "xxx",
        "x..",
        "xxx"
    ],cm),

    sprite.Sprite([
        "xxx",
        "..x",
        "xxx",
        "..x",
        "xxx"
    ],cm),

    sprite.Sprite([
        "x.x",
        "x.x",
        "xxx",
        "..x",
        "..x"
    ],cm),

    sprite.Sprite([
        "xxx",
        "x..",
        "xxx",
        "..x",
        "xxx"
    ],cm),

    sprite.Sprite([
        "xxx",
        "x..",
        "xxx",
        "x.x",
        "xxx"
    ],cm),

    sprite.Sprite([
        "xxx",
        "..x",
        "..x",
        "..x",
        "..x"
    ],cm),

    sprite.Sprite([
        "xxx",
        "x.x",
        "xxx",
        "x.x",
        "xxx"
    ],cm),

    sprite.Sprite([
        "xxx",
        "x.x",
        "xxx",
        "..x",
        "xxx"
    ],cm)
]

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
                self._border = cgeo.Rectangle(0,6,7,1)
                mqttc.loop_start()

                mqttc.on_message = self.on_message
                self._value = 0
                self._fraction = 0
                self._trigger_frame = 125
                self._frame_count = 0


        def on_message(self,client, userdata, msg):
            data  = msg.payload.decode('utf-8').split('/')
            value = data[1]
            addr  = data[0]
            if addr == AUSSEN_SENSOR_ADDR:
                number_color.h += 1.7
                self._color_beat.value = 1.0
                fvalue = (float(value))
                self._value = math.floor(fvalue)
                self._fraction = math.floor((fvalue - self._value) * 100)
                self._frame_count = 0


        def paint_number(self, number):
            x_zehner = 0
            x_einer  = 4
            y = 1

            if number < 10:
                ziffern_sprites[0].paint(self.display,x_zehner,y)
                ziffern_sprites[number].paint(self.display,x_einer,y)
            else:
                s = str(number)
                z = int(s[len(s)-2])
                e = int(s[len(s)-1])
                ziffern_sprites[z].paint(self.display,x_zehner,y)
                ziffern_sprites[e].paint(self.display,x_einer,y)

        def paint(self):
                self.display.fill((0,0,0))
                self.display.set_pixel(3,6,self._color_beat)
                self.paint_number(self._value if self._frame_count < self._trigger_frame else self._fraction)
                if self._color_beat.value > 0.01:
                    self._color_beat.value += 0.99

                self._frame_count += 1


app = AnimClass()
app.start_loop()
