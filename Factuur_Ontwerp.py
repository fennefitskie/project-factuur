from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
import json

with open('2006-379.json', 'r') as f:
    data = json.load(f)
    
order = data.get('order', {})
klant = order.get('klant', {})
producten = order.get('producten', {})

ordernummer = order.get('ordernummer', 'Niet gevonden')
orderdatum = order.get('orderdatum', 'Niet gevonden')
betaaltermijn = order.get('betaaltermijn', 'Niet gevonden')

naam = klant.get('naam', 'Niet gevonden')
adres = klant.get('adres', 'Niet gevonden')
postcode = klant.get('postcode', 'Niet gevonden')
stad = klant.get('stad', 'Niet gevonden')

pdffile = Canvas('Factuur Broski.pdf')

fonts = pdffile.getAvailableFonts()

pdffile.setFont('Times-Italic', 35)
pdffile.drawString(240, 750, 'Factuur')

pdffile.setFont('Helvetica-Bold', 25)
pdffile.drawString(205, 715, ' B  R  O  S  K  I ')

pdffile.setFont('Helvetica-Bold', 13)
pdffile.drawString(80, 680, 'Factuur Broski')
pdffile.drawString(380, 680, 'Gegevens klant')

pdffile.setFont('Helvetica', 13 )
pdffile.drawString(80, 665, 'F Fitskie & Y. Bron')
pdffile.drawString(80, 650, 'Rooseveltstraat 9')
pdffile.drawString(80, 635, '3772 BK Barneveld')
pdffile.drawString(80, 620, 'Nederland')

pdffile.drawString(80, 590, 'BTW nummer: NL-843219765B45')
pdffile.drawString(80, 575, 'KVK nummer: 874302619481 ')


pdffile.drawString(80, 545, 'Ordernummer: ') 
pdffile.drawString(80, 530, 'Orderdatum: ') 
pdffile.drawString(80, 515, 'Betaaltermijn: ') 

pdffile.drawString(170, 545, ordernummer) 
pdffile.drawString(170, 530, orderdatum) 
pdffile.drawString(170, 515, betaaltermijn) 


pdffile.setFont('Helvetica-Bold', 13)
pdffile.drawString(380, 680, 'Gegevens klant')


pdffile.setFont('Helvetica', 13)
pdffile.drawString(380, 665, naam )
pdffile.drawString(380, 650, adres)
pdffile.drawString(380, 635, postcode)
pdffile.drawString(380, 620, stad )

y = 700
x = 80
pdffile.line(x, y, x + 400, y)

y = 505
x = 80
pdffile.line(x, y, x + 400, y)

pdffile.setFont('Helvetica-Bold', 15)
pdffile.drawString(100, 480, 'Item')
pdffile.drawString(200, 480, 'Aantal')
pdffile.drawString(300, 480, 'Prijs')
pdffile.drawString(400, 480, 'Totaal')

y = 460
x = 80
pdffile.line(x, y, x + 400, y)


pdffile.setFont('Helvetica', 13 )
y = 435

max_lengte = 15
prijs_zonder_btw = 0
for product in producten:
    productnaam = product['productnaam']
    aantal = str(product['aantal'])
    prijs_excl_btw = str(product['prijs_per_stuk_excl_btw'])
    btw_percentage = product['btw_percentage']
    totaal = round(float(prijs_excl_btw) * int(aantal),2)
    prijs_zonder_btw += totaal


    if len(productnaam) > max_lengte:
            productnaam = productnaam[:max_lengte-3] + "..." 

    if btw_percentage == 6:
        btw_6 = totaal / 100 * 106
        btw_6 = btw_6 - totaal
        print(btw_6)

    elif btw_percentage == 9:
         btw_9 = totaal / 100 * 109
         btw_9 = btw_9 - totaal
         print(btw_9)
         
    else:
         btw_21 = totaal / 100 * 121
         btw_21 = btw_21 - totaal
         print(btw_21)


    pdffile.drawString(95, y, productnaam)
    pdffile.drawString(220, y, aantal)
    pdffile.drawString(303, y, prijs_excl_btw)
    pdffile.drawString(403, y, str(totaal))
    y -= 25

y = y  
x = 80
pdffile.line(x, y, x + 400, y)

y = y - 45
x = 80
pdffile.line(x, y, x + 400, y)

y = y - 20
pdffile.drawString(320, y, 'Totaal excl BTW: ' )
pdffile.drawString(430, y, str(prijs_zonder_btw))

y = y - 20


pdffile.drawString(385, y, 'BTW: ' )
pdffile.drawString(450, y, 'Prijs' )

y = y - 20
pdffile.setFont('Helvetica-Bold', 13)
pdffile.drawString(315, y, 'Totaal incl BTW: ' )
pdffile.drawString(450, y, 'Prijs' )








pdffile.save()