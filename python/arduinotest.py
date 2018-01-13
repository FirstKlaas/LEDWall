from ledwall.util.arduino import convert_image_to_progmem_bitmask
from PIL import Image


img    = Image.open('../LEDWALL-FONT.png')
rgbimg = img.convert('RGB')

print "Breite: {:d}, Hoehe: {:d}".format(rgbimg.width, rgbimg.height)

print convert_image_to_progmem_bitmask('letter_a', rgbimg,0,0,11,15)
print convert_image_to_progmem_bitmask('letter_b', rgbimg,12,0,11,15)