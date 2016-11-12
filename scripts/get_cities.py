import csv
citiesAndSizes = {}
with open('worldcitiespop.txt', 'rb') as citiesfile:
    reader = csv.reader(citiesfile, delimiter=',')
    for row in reader:
        if row[2] not in citiesAndSizes or row[4] > (citiesAndSizes[row[2]])[0]
            citiesAndSizes[row[2]] = (row[4], row[5], row[6])
with open('cities.txt', 'w') as f:
    for city, coords in citiesAndSizes.items:
        f.write(city + ’,’ + coords[1] + ’,’ + coords[2] + ‘\n’)
