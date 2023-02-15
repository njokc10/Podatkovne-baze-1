import cars

car = cars.get_car()
#print(car)

# make = set()
# for c in car:
#     if c["Identification"]["Make"] not in make:
#         make.add(c["Identification"]["Make"])
# print(make)

# ide = set()
# for c in car:
#     if c["Identification"]["ID"] not in make:
#         ide.add(c["Identification"]["ID"])
# print(ide)

podatki = []
znamke = set()
for c in car:
    sl = {}
    if c["Identification"]["ID"].split()[2] not in znamke:
        znamke.add(c["Identification"]["ID"].split()[2])
        sl["znamka"] = c["Identification"]["Make"]
        sl["model"] = c["Identification"]["ID"].split()[2]
        sl["menjalnik"] = c["Identification"]["Classification"].split()[0]
        sl["pogon"] = c["Engine Information"]["Driveline"].split()[0]
        sl["tip motorja"] = c["Engine Information"]["Engine Type"].split()[1]
        sl["hibrid"] = c["Engine Information"]["Hybrid"]
        sl["število prestav"] = c["Engine Information"]["Number of Forward Gears"]
        sl["poraba mestne vožnje"] = c["Fuel Information"]["City mpg"]
        sl["gorivo"] = c["Fuel Information"]["Fuel Type"]
        sl["poraba avtocestne vožje"] = c["Fuel Information"]["Highway mpg"]
        sl["moč motorja"] = c["Engine Information"]["Engine Statistics"]["Horsepower"]
        sl["navor"] = c["Engine Information"]["Engine Statistics"]["Torque"]
        sl["višina"] = c["Dimensions"]["Height"]
        sl["dolžina"] = c["Dimensions"]["Length"]
        sl["širina"] = c["Dimensions"]["Width"]
        podatki.append(sl)

print(podatki)


        
    

