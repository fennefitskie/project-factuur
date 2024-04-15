from reportlab.pdfgen.canvas import Canvas

canvas = Canvas('Factuur Broski.pdf')

text = input('Welke text moet er in de PDF staan: ')

canvas.drawString(0, 830, text) # hoogte 830 is de max, Eerste getal is lengte en tweede getal is hoogte

canvas.save()