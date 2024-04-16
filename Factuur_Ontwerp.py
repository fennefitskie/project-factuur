from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

# Times-Italic voor de factuur titel
# Helvetica-Bold voor de broski titel 
# Helvetica voor de tekst

pdffile = Canvas('Factuur Broski.pdf')

naam_klant = input('Wat is uw naam? ')
adres_klant = input('Wat is uw adres? ')
postcode_klant = input('Wat is uw postcode en plaats? ')
land_klant = input('Wat is het land waarin u woont? ')

fonts = pdffile.getAvailableFonts()

pdffile.setFont('Times-Italic', 35)
pdffile.drawString(240, 750, 'Factuur')

pdffile.setFont('Helvetica-Bold', 25)
pdffile.drawString(205, 715, ' B  R  O  S  K  I ')

pdffile.setFont('Helvetica-Bold', 13)
pdffile.drawString(80, 680, 'Factuur Broski')

pdffile.setFont('Helvetica', 13 )
pdffile.drawString(80, 665, 'F Fitskie & Y. Bron')
pdffile.drawString(80, 650, 'Rooseveltstraat 9')
pdffile.drawString(80, 635, '3772 BK Barneveld')
pdffile.drawString(80, 620, 'Nederland')

pdffile.drawString(80, 590, 'BTW nummer: NL-843219765B45')
pdffile.drawString(80, 575, 'KVK nummer: 874302619481 ')

pdffile.drawString(80, 545, 'Factuurnummer: F2024-01') # Nog dynamisch maken
pdffile.drawString(80, 530, '15-04-24') # Nog dynamisch maken

pdffile.setFont('Helvetica-Bold', 13)
pdffile.drawString(380, 680, 'Gegevens klant')

pdffile.setFont('Helvetica', 13 )
pdffile.drawString(380, 665, naam_klant)
pdffile.drawString(380, 650, adres_klant)
pdffile.drawString(380, 635, postcode_klant )
pdffile.drawString(380, 620, land_klant)

y = 700
x = 80
pdffile.line(x, y, x + 400, y)

y = 510
x = 80
pdffile.line(x, y, x + 400, y)


# Voor de tabel een for loop gebruiken met max aantal regels.


pdffile.save()