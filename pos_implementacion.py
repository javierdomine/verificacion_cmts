import yaml
import getpass
import csv

import textfsm
import threading
from gatheringInfo import *


def find_scopes(tag):
    net_scopes = ""
    if tag in dict_scopes[target].keys():
        if (dict_scopes[target][tag][0]) != "No tiene Redes asociadas":
            for address in (dict_scopes[target][tag]):
                octetos = (address.split("."))
                octetos = octetos[0] + "." + octetos[1]
                if octetos not in net_scopes:
                    net_scopes = net_scopes + octetos + '|'
            net_scopes = net_scopes[:-1]
            return net_scopes
    return "none"


with open(r'ccap_scopes.yml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    dict_scopes = yaml.load(file, Loader=yaml.FullLoader)

### INGRESAR USUARIO Y CONTRASEÑA ###
	
#user = input ("\nQuien es? ")
user = "u605930"

#### INGRESE USUARIO Y CONTRASEnA ####

print("Hola", user, "- Por favor ingrese su contrasena")
passw = "M414S0f14"



e6kTargets = list()
cbr8Targets = list()
c100gTargets = list()
dictTargets = {}


with open("ccaps-target.yml", "r") as f:
    dictTargets = (yaml.load(f, Loader=yaml.FullLoader))

#print(dictTargets["e6k"])
#print(dictTargets["cbr8"])
#print(dictTargets["c100g"])

if dictTargets["e6k"] != None:
    for item in dictTargets["e6k"]:
        e6kTargets.append(item["hostname"])

if dictTargets["cbr8"] != None:
    for item in dictTargets["cbr8"]:
        cbr8Targets.append(item["hostname"])

if dictTargets["c100g"] != None:
    for item in dictTargets["c100g"]:
        c100gTargets.append(item["hostname"])

ccapsTarget = e6kTargets + cbr8Targets + c100gTargets
print(ccapsTarget)


#print(e6kTargets)
#print(cbr8Targets)
#print(c100gTargets)

CCPAsNoEncontrados = list()

for i in range(len(e6kTargets)):
    if e6kTargets[i] not in dict_scopes.keys() or e6kTargets[i] == "":
        CCPAsNoEncontrados.append(e6kTargets[i])
if len(CCPAsNoEncontrados) > 0:
    print("\n### CCAPS NO ENCONTRADOS: ", CCPAsNoEncontrados)

for i in range(len(cbr8Targets)):
    if cbr8Targets[i] not in dict_scopes.keys() or cbr8Targets[i] == "":
        CCPAsNoEncontrados.append(cbr8Targets[i])
if len(CCPAsNoEncontrados) > 0:
    print("\n### CCAPS NO ENCONTRADOS: ", CCPAsNoEncontrados)

for i in range(len(c100gTargets)):
    if c100gTargets[i] not in dict_scopes.keys() or c100gTargets[i] == "":
        CCPAsNoEncontrados.append(c100gTargets[i])
if len(CCPAsNoEncontrados) > 0:
    print("\n### CCAPS NO ENCONTRADOS: ", CCPAsNoEncontrados)

csvfile = open('resume.csv', 'w', newline='')


for target in e6kTargets:
    ipManagement = dict_scopes[target]["IP"]
    print("Hostname: ", target)
    print("IP management: ", ipManagement)
    e6kCommands = {}
    e6kCommands["cm_online"] = ["show cable modem summary | include Total"]
    scopes = find_scopes("DSG")
    if scopes != "none":
        e6kCommands["deco_legacy"] = ["show cable modem column cpe-ip |  include " + scopes + " | count"]
    else:
        e6kCommands["deco_legacy"] = ["!"]
    scopes = find_scopes("PRI-NAT44")
    if scopes != "none":
        e6kCommands["deco_flow"] = ["show cable modem column cpe-ip |  include " + scopes + " | count"]
    else:
        e6kCommands["deco_flow"] = ["!"]
    scopes = find_scopes("MTA")
    if scopes != "none":
        e6kCommands["mta"] = ["show cable modem column cpe-ip |  include " + scopes + " | count"]
    else:
        e6kCommands["mta"] = ["!"]
    scopes = find_scopes("SIP")
    if scopes != "none":
        e6kCommands["sip"] = ["show cable modem column cpe-ip |  include " + scopes + " | count"]
    else:
        e6kCommands["sip"] = ["!"]

    e6kStatus = verifyE6kStatus(ipManagement, e6kCommands, target)

    file_name = "verifications\pos-" + target + ".txt"

    with open(file_name, 'w') as log_text:
        for comm in e6kStatus.keys():
            log_text.write(e6kStatus[comm][0] + "\n")
            log_text.write(e6kStatus[comm][1] + "\n")

    file_name = "verifications\pos-" + target + ".yml"
    with open(file_name, 'w') as file:
        yaml.dump(e6kStatus, file)

#### CBR8 VERIFYCATION
for target in cbr8Targets:
    ipManagement = dict_scopes[target]["IP"]
    print("Hostname: ", target)
    print("IP management: ", ipManagement)
    cbr8Commands = {}
    cbr8Commands["cm_online"] = ["show cable modem summary total | include Total"]
    scopes = find_scopes("DSG")
    if scopes != "none":
        cbr8Commands["deco_legacy"] = [ "show cable host access-group | count " + scopes ]
    else:
        cbr8Commands["deco_legacy"] = ["!"]
    scopes = find_scopes("PRI-NAT44")
    if scopes != "none":
        cbr8Commands["deco_flow"] = [ "show cable host access-group | count " + scopes ]
    else:
        cbr8Commands["deco_flow"] = ["!"]
    scopes = find_scopes("MTA")
    if scopes != "none":
        cbr8Commands["mta"] = [ "show cable host access-group | count " + scopes ]
    else:
        cbr8Commands["mta"] = ["!"]
    scopes = find_scopes("SIP")
    if scopes != "none":
        cbr8Commands["sip"] = ["show cable host access-group | count " + scopes ]
    else:
        cbr8Commands["sip"] = ["!"]

    cbr8Status = verifycbr8Status(ipManagement, cbr8Commands, target)

    file_name = "verifications\pos-" + target + ".txt"

    with open(file_name, 'w') as log_text:
        for comm in cbr8Status.keys():
            log_text.write(cbr8Status[comm][0] + "\n")
            log_text.write(cbr8Status[comm][1] + "\n")

    file_name = "verifications\pos-" + target + ".yml"
    with open(file_name, 'w') as file:
        yaml.dump(cbr8Status, file)



### C100G VERIFYCATION ###

for target in c100gTargets:
    ipManagement = dict_scopes[target]["IP"]
    print("Hostname: ", target)
    print("IP management: ", ipManagement)
    c100gCommands = {}
    c100gCommands["cm_online"] = ["show cable modem summary total | include Total"]
    scopes = find_scopes("DSG")
    if scopes != "none":
        c100gCommands["deco_legacy"] = ["show cable  modem  cpe | count-only " + scopes ]
    else:
        c100gCommands["deco_legacy"] = ["!"]
    scopes = find_scopes("PRI-NAT44")
    if scopes != "none":
        c100gCommands["deco_flow"] = ["show cable  modem  cpe | count-only " + scopes ]
    else:
        c100gCommands["deco_flow"] = ["!"]
    scopes = find_scopes("MTA")
    if scopes != "none":
        c100gCommands["mta"] = ["show cable  modem  cpe | count-only " + scopes ]
    else:
        c100gCommands["mta"] = ["!"]
    scopes = find_scopes("SIP")
    if scopes != "none":
        c100gCommands["sip"] = ["show cable  modem  cpe | count-only " + scopes ]
    else:
        c100gCommands["sip"] = ["!"]

  #  c100g = {
  #      'device_type': 'cisco_ios',
  #      'ip': ipManagement,
  #      'username': user,
  #      'password': passw,
  #      'port': 22,
  #      'timeout': 12 * 60
  #  }

    c100gStatus = verifyC100gStatus(ipManagement, c100gCommands, target)

    file_name = "verifications\pos-" + target + ".txt"

    with open(file_name, 'w') as log_text:
        for comm in c100gStatus.keys():
            log_text.write(c100gStatus[comm][0] + "\n")
            log_text.write(c100gStatus[comm][1] + "\n")

    file_name = "verifications\pos-" + target + ".yml"
    with open(file_name, 'w') as file:
        yaml.dump(c100gStatus, file)

### FILTER INFORMATION ###



writercsv = csv.writer(csvfile, delimiter=';')  # getting a csv.writer object

infoPre = {}
infoPos = {}
toWrite = list()
for target in e6kTargets:
    file_name = "verifications\pre-" + target + ".yml"
    infoPre[target] = (filterE6kInfo(target, file_name))

    file_name = "verifications\pos-" + target + ".yml"
    infoPos[target] = (filterE6kInfo(target, file_name))

for target in cbr8Targets:
    file_name = "verifications\pre-" + target + ".yml"
    infoPre[target] = (filterCbr8Info(target, file_name))

    file_name = "verifications\pos-" + target + ".yml"
    infoPos[target] = (filterCbr8Info(target, file_name))


for target in c100gTargets:
    file_name = "verifications\pre-" + target + ".yml"
    infoPre[target] = (filterC100gInfo(target, file_name))

    file_name = "verifications\pos-" + target + ".yml"
    infoPos[target] = (filterC100gInfo(target, file_name))



print("\nInfo PRE: ", infoPre)
print("\nInfo PRE: ", infoPos)

# ccapsTarget = list ()
# for vendor in dictTargets.keys():
#    for ccap in dictTargets[vendor]:
#        ccapsTarget.append (ccap["hostname"])


print(infoPre)
print(infoPos)

for ccap in ccapsTarget:
    print("\n", "-" * 150, "\n",
          " |             | CCAP    |     CM    | DECO-LEGACY  |  DECO-FLOW   |   MTA        |       SIP      |     PARTIAL    |    INIT     |   OFDM    |\n",
          "-" * 150)

    toWrite = [ccap]
    writercsv.writerow(toWrite)
    toWrite = ["  ", "CM", "VoD", "FLOW", "MTA", "SIP", "PARTIAL", "INIT", "OFDM"]
    writercsv.writerow(toWrite)

    toWrite = ["PREVIO"]
    print(" |", ccap.rjust(12), "| PREVIO      |", end="")
    for item in infoPre[ccap].keys():
        print(infoPre[ccap][item].rjust(12), end=" |")
        toWrite.append(infoPre[ccap][item])
    writercsv.writerow(toWrite)
    toWrite = ["POSTERIOR"]
    print("\n", "-" * 150)
    print(" |", ccap.rjust(12), "| POSTERIOR   |", end="")
    for item in infoPos[ccap].keys():
        print(infoPos[ccap][item].rjust(12), end=" |")
        toWrite.append(infoPos[ccap][item])
    writercsv.writerow(toWrite)
    print("\n", "-" * 150)
    print(" |", ccap.rjust(12), "| DELTA       |", end="")
    toWrite = ["DELTA"]
    for item in infoPre[ccap].keys():
        delta = str((int(infoPos[ccap][item]) - int(infoPre[ccap][item])))
        print(delta.rjust(12), end=" |")
        toWrite.append(delta)
    writercsv.writerow(toWrite)
    toWrite = ["DELTA %"]
    print("\n", "-" * 150)
    print(" |", ccap.rjust(12), "| DELTA       |", end="")
    for item in infoPre[ccap].keys():
        delta = (int(infoPos[ccap][item]) - int(infoPre[ccap][item]))
        if infoPos[ccap][item] != "0":
            print((str(round((delta / int(infoPos[ccap][item]) * 100), 0)) + "%").rjust(12), end=" |")
            toWrite.append((str(round((delta / int(infoPos[ccap][item]) * 100), 0)) + "%"))
        else:
            print((str(0) + "%").rjust(12), end=" |")
            toWrite.append("0%")
    writercsv.writerow(toWrite)
    writercsv.writerow("")
    print(" ")

totalesPre = {'cm_online': 0, 'deco_legacy': 0, 'deco_flow': 0, 'mta': 0, 'sip': 0, 'partial': 0, 'init': 0,
              'ofdm-dw': 0}
totalesPos = {'cm_online': 0, 'deco_legacy': 0, 'deco_flow': 0, 'mta': 0, 'sip': 0, 'partial': 0, 'init': 0,
              'ofdm-dw': 0}

for ccap in ccapsTarget:
    for item in infoPre[ccap].keys():
        totalesPre[item] = totalesPre[item] + int(infoPre[ccap][item])
        totalesPos[item] = totalesPos[item] + int(infoPos[ccap][item])

toWrite = ["TOTAL"]
writercsv.writerow(toWrite)
toWrite = ["  ", "CM", "VoD", "FLOW", "MTA", "SIP", "PARTIAL", "INIT", "OFDM"]
writercsv.writerow(toWrite)
toWrite = ["PREVIO"]

print("\n", "-" * 150, "\n",
      " |                       |     CM    | DECO-LEGACY  |  DECO-FLOW   |   MTA        |       SIP      |     PARTIAL    |    INIT     |   OFDM    |\n",
      "-" * 150)
print(" |", "TOTAL".rjust(12), "| PREVIO      |", end="")

for item in totalesPre.keys():
    print(str(totalesPre[item]).rjust(12), end=" |")
    toWrite.append(totalesPre[item])
writercsv.writerow(toWrite)
toWrite = ["POSTERIOR"]
print("\n", "-" * 150)
print(" |", "TOTAL".rjust(12), "| POSTERIOR  |", end="")
for item in totalesPre.keys():
    print(str(totalesPos[item]).rjust(12), end=" |")
    toWrite.append(totalesPos[item])
writercsv.writerow(toWrite)
print("\n", "-" * 150)
print(" |", "TOTAL".rjust(12), "| DELTA      |", end="")
toWrite = ["DELTA"]
for item in totalesPre.keys():
    print(str(totalesPos[item] - totalesPre[item]).rjust(12), end=" |")
    toWrite.append(str(totalesPos[item] - totalesPre[item]))
writercsv.writerow(toWrite)
print("\n", "-" * 150)
print(" |", "TOTAL".rjust(12), "| DELTA %    |", end="")
toWrite = ["DELTA %"]
for item in totalesPre.keys():
    if totalesPre[item] != 0:
        print((str(round(((totalesPos[item] - totalesPre[item]) / totalesPre[item] * 100), 0)) + "%").rjust(12), end=" |")
        toWrite.append((str(round(((totalesPos[item] - totalesPre[item]) / totalesPre[item] * 100), 0)) + "%"))
    else:
        print ("0".rjust(12))
        toWrite.append("0")
writercsv.writerow(toWrite)

print("\n", "-" * 150)

csvfile.close()














input("Pulse una tecla para finalizar")



