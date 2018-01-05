from ledwall.util import intersectRect

r1 = (0,0,10,10)
r2 = (11,11,12,12)

s = intersectRect(r1,r2)

if s:
	print 'Schnittmenge gefunden'
	if s == (0,0,5,5):
		print "Und das Ergbnis stimmt"
	else:
		print "Das ergebnis stimm nicht"
else:
	print "Es gibt keine Schnittmenge zwischen {} und {}".format(r1,r2)