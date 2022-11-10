import wget
import csv
import yaml
from os import remove

def gather_scopes():
  output_directory = 'ccap_scopes.csv'
  url = 'http://ftsltools.int.fibertel.com.ar/.test/INTRAWAY/scopes-domine.php'

  try:
    remove("ccap_scopes.csv")
  except FileNotFoundError:
    print("No hay archivo con informacion de scopes preexistente. Se inicia la descarga del mismo....")
  filename = wget.download(url, out=output_directory)

  dict_ccap_scopes = {}
  list_ccap_scopes = list()

  with open('ccap_scopes.csv') as ccap_scopes_file:
    ccap_scopes_reader = csv.reader(ccap_scopes_file, delimiter=';')
    for row in ccap_scopes_reader:
      list_ccap_scopes.append(row)

  del list_ccap_scopes[0]

  for row in list_ccap_scopes:
    if row[0] not in dict_ccap_scopes.keys():
      dict_ccap_scopes[row[0]] = {"IP": row[1]}
      dict_ccap_scopes[row[0]]["CM"] = list()
      dict_ccap_scopes[row[0]]["MTA"] = list()
      dict_ccap_scopes[row[0]]["DSG"] = list()
      dict_ccap_scopes[row[0]]["PROV"] = list()
      dict_ccap_scopes[row[0]]["PRIVATE"] = list()
      dict_ccap_scopes[row[0]]["PRI-NAT44"] = list()
      dict_ccap_scopes[row[0]]["SIP"] = list()
      dict_ccap_scopes[row[0]]["FIBERTEL"] = list()

  for row in list_ccap_scopes:
    scope = row[2] + "/" + row[3]
    if row[5] == "63":
      dict_ccap_scopes[row[0]]["CM"].append(scope)
    elif row[5] == "81":
      dict_ccap_scopes[row[0]]["MTA"].append(scope)
    elif row[5] == "65":
      dict_ccap_scopes[row[0]]["DSG"].append(scope)
    elif row[5] == "67":
      dict_ccap_scopes[row[0]]["PROV"].append(scope)
    elif row[5] == "68":
      dict_ccap_scopes[row[0]]["PRIVATE"].append(scope)
    elif row[5] == "69":
      dict_ccap_scopes[row[0]]["FIBERTEL"].append(scope)
    elif row[5] == "129":
      dict_ccap_scopes[row[0]]["PRI-NAT44"].append(scope)
    elif row[5] == "229":
      dict_ccap_scopes[row[0]]["SIP"].append(scope)

  print(dict_ccap_scopes)

  with open("ccap_scopes.yml", 'w') as file:
    yaml.dump(dict_ccap_scopes, file)
  
gather_scopes()