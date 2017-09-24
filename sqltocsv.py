import sqlite3
from datetime import datetime
import csv

conn = sqlite3.connect('twitterprofiles.db')

c = conn.cursor()

targettwitterprofile = 'anytwitterusername'

c.execute('SELECT dbtweetdate, AVG(polarity) FROM '+targettwitterprofile+' GROUP BY dbtweetdate ORDER BY dbtweetdate')

newc = []

for row in c:
    newc.append((datetime.strptime(row[0],'%d-%m-%Y'), row[1]))

sortedrow = sorted(newc, key=lambda tup: tup[0])

with open(targettwitterprofile+'-results.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Date','Score'])
    for newrow in sortedrow:
        csvwriter.writerow([newrow[0].strftime('%d-%m-%Y'), newrow[1]])

c.close()
