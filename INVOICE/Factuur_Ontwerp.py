from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
import json
import os
import shutil
import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Factuur_Broski(
                klanten TEXT,
                Factuur INTEGER,
                Factuurregels INTEGER
)""")

max_lengte = 15
btw_6 = 0
btw_9 = 0
btw_21 = 0

input_folder = 'C:/School/Code/leren_programmeren/project-factuur/JSON_IN'
output_folder = 'C:/School/Code/leren_programmeren/project-factuur/JSON_PROCESSED'
pdf_folder = 'C:/School/Code/leren_programmeren/project-factuur/INVOICE'

for filename in os.listdir(input_folder):
    input_file_path = os.path.join(input_folder, filename)

    with open(input_file_path, 'r') as f:
        data = json.load(f)

    ordernummer = data.get('order', {}).get('ordernummer', 'niet gevonden')
    output_pdf_path = os.path.join(pdf_folder, f'Factuur_{ordernummer}.pdf')
    output_json_path = os.path.join(pdf_folder, f'Factuur_{ordernummer}.json')
    
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
    kvk = klant.get('KVK-nummer', 'Niet gevonden')

    pdffile = Canvas(output_pdf_path)

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
    pdffile.drawString(380, 605, kvk)  

    y = 700
    x = 80
    pdffile.line(x, y, x + 400, y)
    y = 500
    x = 80
    pdffile.line(x, y, x + 400, y)
    pdffile.setFont('Helvetica-Bold', 15)
    pdffile.drawString(100, 475, 'Item')
    pdffile.drawString(200, 475, 'Aantal')
    pdffile.drawString(300, 475, 'Prijs')
    pdffile.drawString(400, 475, 'Totaal')
    y = 455
    x = 80
    pdffile.line(x, y, x + 400, y)
    pdffile.setFont('Helvetica', 13 )
    y = 430

    prijs_zonder_btw = 0  

    for product in producten:
        productnaam = product['productnaam']
        aantal = int(product['aantal'])
        prijs_excl_btw = float(product['prijs_per_stuk_excl_btw'])
        btw_percentage = product['btw_percentage']

        totaal_zonder_btw = round(prijs_excl_btw * aantal, 2)
        prijs_zonder_btw += totaal_zonder_btw  

        if len(productnaam) > max_lengte:
                productnaam = productnaam[:max_lengte-3] + "..." 

        if btw_percentage == 6:
            btw_6 = totaal_zonder_btw / 100 * 106
            btw_6 = btw_6 - totaal_zonder_btw

        elif btw_percentage == 9:
            btw_9 = totaal_zonder_btw / 100 * 109
            btw_9 = btw_9 - totaal_zonder_btw

        else:
            btw_21 = totaal_zonder_btw / 100 * 121
            btw_21 = btw_21 - totaal_zonder_btw

        
        pdffile.drawString(95, y, productnaam)
        pdffile.drawString(220, y, str(aantal))
        pdffile.drawString(303, y, str(prijs_excl_btw))
        pdffile.drawString(403, y, str(totaal_zonder_btw))
        y -= 25


    totaal_btw = round(btw_6 + btw_9 + btw_21, 2) 


    totaal = round(prijs_zonder_btw + totaal_btw, 2)

    y = y  
    x = 80
    pdffile.line(x, y, x + 400, y)
    y = y - 45
    x = 80
    pdffile.line(x, y, x + 400, y)
    y = y - 20
    pdffile.drawString(320, y, 'Totaal excl BTW: ' )
    pdffile.drawString(430, y, str(round(prijs_zonder_btw, 2)))
    y = y - 20
    pdffile.drawString(385, y, 'BTW: ' )
    pdffile.drawString(430, y, str(totaal_btw))
    y = y - 20
    pdffile.setFont('Helvetica-Bold', 13)
    pdffile.drawString(315, y, 'Totaal incl BTW: ' )
    pdffile.drawString(430, y, str(totaal) )
    pdffile.save()

    
    if not os.path.exists(output_json_path):
        factuur_data = {
            "ordernummer": ordernummer,
            "orderdatum": orderdatum,
            "betaaltermijn": betaaltermijn,
            "klant": {
                "naam": naam,
                "adres": adres,
                "postcode": postcode,
                "stad": stad,
                "KVK-nummer": kvk
            },
            "bedrijf": {
                "Naam": "F Fitskie & Y. Bron",
                "Adres": "Rooseveltstraat 9",
                "Postcode": "3772 BK Barneveld",
                "Land": "Nederland"    
            },
            "producten": producten
        }

        with open(output_json_path, 'w') as json_file:
            json.dump(factuur_data, json_file, indent=4)


    shutil.move(input_file_path, os.path.join(output_folder, filename))


    cursor.execute("INSERT INTO Factuur_Broski VALUES (?, ?, ?)", (naam, ordernummer, len(producten)))
    connection.commit()

connection.close()
