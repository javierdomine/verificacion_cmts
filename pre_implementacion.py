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

gather_scopes()

with open(r'ccap_scopes.yml') as file:
    dict_scopes = yaml.load(file, Loader=yaml.FullLoader)		# abrir el archivo ccap_scopes.yml y lo carga en el diccionario dict_scopes

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

    file_name = "verifications\pre-" + target + ".txt"

    with open(file_name, 'w') as log_text:
        for comm in e6kStatus.keys():
            log_text.write(e6kStatus[comm][0] + "\n")
            log_text.write(e6kStatus[comm][1] + "\n")

    file_name = "verifications\pre-" + target + ".yml"
    with open(file_name, 'w') as file:
        yaml.dump(e6kStatus, file)




#### CBR8 VERIFYCATION ###
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


    file_name = "verifications\pre-" + target + ".txt"

    with open(file_name, 'w') as log_text:
        for comm in cbr8Status.keys():
            log_text.write(cbr8Status[comm][0] + "\n")
            log_text.write(cbr8Status[comm][1] + "\n")

    file_name = "verifications\pre-" + target + ".yml"
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

#    c100g = {
#        'device_type': 'cisco_ios',
#        'ip': ipManagement,
#        'username': user,
#        'password': passw,
#        'port': 22,
#        'timeout': 12 * 60
#    }




    c100gStatus = verifyC100gStatus(ipManagement, c100gCommands, target)

    file_name = "verifications\pre-" + target + ".txt"

    with open(file_name, 'w') as log_text:
        for comm in c100gStatus.keys():
            log_text.write(c100gStatus[comm][0] + "\n")
            log_text.write(c100gStatus[comm][1] + "\n")

    file_name = "verifications\pre-" + target + ".yml"
    with open(file_name, 'w') as file:
        yaml.dump(c100gStatus, file)





### FILTER INFORMATION ###

infoPre = {}
for target in e6kTargets:
    file_name = "verifications\pre-" + target + ".yml"
    infoPre[target] = (filterE6kInfo(target, file_name))
#    print (infoPre)
    print("\n ",  "-" * 125, "\n", " |           CCAP            |     CM    |DECO-LEGACY| DECO-FLOW |   MTA     |    SIP    |  PARTIAL  |   INIT    |   OFDM    |\n ",  "-" * 125)
    print("  |", target.rjust(16), "| PREVIO |", end="")
    for item in infoPre[target].keys():
        print(infoPre[target][item].rjust(10), end=" |")
    print ("\n ", "-" * 125)
for target in cbr8Targets:
    file_name = "verifications\pre-" + target  + ".yml"
    infoPre[target] = (filterCbr8Info(target, file_name))
#    print (infoPre)
    print("\n ", "-" * 125, "\n", " |           CCAP            |     CM    |DECO-LEGACY| DECO-FLOW |   MTA     |    SIP    |  PARTIAL  |   INIT    |   OFDM    |\n ",  "-" * 125)
    print("  |", target.rjust(16), "| PREVIO |", end="")
    for item in infoPre[target].keys():
        print(infoPre[target][item].rjust(10), end=" |")
    print ("\n ", "-" * 125)


for target in c100gTargets:
    file_name = "verifications\pre-" + target  + ".yml"
    infoPre[target] = (filterC100gInfo(target, file_name))
#    print (infoPre)
    print("\n ", "-" * 125, "\n", " |           CCAP            |     CM    |DECO-LEGACY| DECO-FLOW |   MTA     |    SIP    |  PARTIAL  |   INIT    |   OFDM    |\n ",  "-" * 125)
    print("  |", target.rjust(16), "| PREVIO |", end="")
    for item in infoPre[target].keys():
        print(infoPre[target][item].rjust(10), end=" |")
    print ("\n ", "-" * 125)




input ("\n*** pulse una tecla para finalizar ***")