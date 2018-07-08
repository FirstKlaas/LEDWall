from ledwall.components import *

cornflowerblue = ColorTable.CornflowerBlue

print "CornflowerBlue %r" % cornflowerblue

rgb = cornflowerblue.rgbColor
print "%r , %r" % (rgb, rgb.intValues)

hsv = cornflowerblue.hsvColor
print "%r , %r" % (hsv, hsv.intValues)

print "Now create two new colors"
c1 = Color.fromRGBColor(rgb)
c2 = Color.fromHSVColor(hsv)

print "From RGB %r" % c1
print "From HSV %r" % c2	

print hsv.rgb

