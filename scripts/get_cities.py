import csv
cities = set()
with open('worldcitiespop.txt', 'rb') as citiesfile:
    reader = csv.reader(citiesfile, delimiter=',')
    for row in reader:
        cities.add(row[2])
with open('cities.txt', 'w') as f:
    for city in cities:
        f.write(city+'\n')
