# -*- coding: utf-8 -*-
import wget
import yaml
from netmiko import ConnectHandler
import textfsm
from os import remove
import csv
import time


def verifyE6kStatus(ccapAddress, commands, ccapName):    # Recibe diccionario del dispositivo, comandos ad-hoc y nombre del host

    ip_addr = "10.247.2.149"
    passw = "Javier2021"
    linux = {
        'device_type': 'linux',
        'ip': ip_addr,
        'username': "root",
        'password': passw,
        'port': 22,
        'timeout': 30 * 60,
    }

    net_connect = ConnectHandler(**linux)
    print(net_connect.find_prompt())
    output = net_connect.send_command("uname -a")
    print(output)

    e6kComms = commands.copy()
    e6kComms["partial"] = ["show cable modem bonded-impaired count"]
    e6kComms["init"] = ["show cable modem | exclude Operational|Offline | count"]
    e6kComms["ofdm-dw"] = ["show cable modem ofdm-downstream bonded | count"]
    e6kComms["linecard"] = ["show linecard status"]
    e6kComms["interface-cable"] = ["show interface cable-mac"]
    e6kComms["summary"] = ["show cable modem summary"]
    e6kComms["summary-port"] = ["show cable modem summary port"]
    e6kComms["stb-total"] = ["show cable modem cpe-type stb count"]
    e6kComms["mta-total"] = ["show cable modem cpe-type mta count "]
    e6kComms["ertr"] = ["show cable modem cpe-type ertr count"]
    e6kComms["ertr"] = ["show cable modem cpe-type ertr count"]
    e6kComms["environ"] = ["show environment"]
    e6kComms["default"] = ["show ip route 0.0.0.0"]
    e6kComms["bgp-nei"] = ["show ip bgp neighbor"]
    e6kComms["bgp-summ"] = ["show ip bgp summary"]
    e6kComms["lacp"] = ["show lacp summary"]
    e6kComms["pim-inter"] = ["show ip pim interface"]
    e6kComms["pim-nei"] = ["show ip pim neighbor"]
    e6kComms["version"] = ["show version"]
    e6kComms["running"] = ["show running-config verbose"]

    print("#" * 6, "COMANDOS A EJECUTAR EN: ", ccapName, "#" * 6)
    for line in e6kComms.keys():
        print(e6kComms[line][0])
    host_loging = "ssh u605930@"+ccapAddress
    print (host_loging)


    #output = net_connect.send_command(host_loging, expect_string="password:")
    output = net_connect.send_command_timing(host_loging)
    time.sleep(13)  # retardo para evitar falla de TACACS
    if "(yes/no)" in output:
        output = net_connect.send_command_timing("yes")
        print (output)
    output = net_connect.send_command_timing("V4l3nt1n02")
    print(output)
    time.sleep(14)
    if "password:" in output:
        output = net_connect.send_command_timing("V4l3nt1n02")
    time.sleep(30)
    if "password:" in output:
        output = net_connect.send_command_timing("V4l3nt1n02")
    time.sleep(30)
    if "password:" in output:
        output = net_connect.send_command_timing("V4l3nt1n02")


    hostname = net_connect.find_prompt()
    hostname = hostname[:-1]
    print("\n***** E6K objetivo: ", hostname, "*****")

    print (net_connect.send_command("configure no pagination"))

    e6kComms["linecard"].append(net_connect.send_command(e6kComms["linecard"][0]))
    print('\n', '#' * 20, hostname, "  - LINECARD STATUS - ", '#' * 20)
    print(" >>> ", (e6kComms["linecard"][0]))
    print(e6kComms["linecard"][1])

    e6kComms["cm_online"].append(net_connect.send_command(e6kComms["cm_online"][0]))
    print('\n', '#' * 20, hostname, "  - CM online  - ", '#' * 20)
    print(" >>> ", e6kComms["cm_online"][0])
    print(e6kComms["cm_online"][1])
    e6kComms["deco_legacy"].append(net_connect.send_command(e6kComms["deco_legacy"][0]))
    print('\n', '#' * 20, hostname, "  - DECO LEGACY - ", '#' * 20)
    print(" >>> ", (e6kComms["deco_legacy"][0]))
    print(e6kComms["deco_legacy"][1])
    e6kComms["deco_flow"].append(net_connect.send_command(e6kComms["deco_flow"][0]))
    print('\n', '#' * 20, hostname, "  - DECO FLOW - ", '#' * 20)
    print(" >>> ", (e6kComms["deco_flow"][0]))
    print(e6kComms["deco_flow"][1])
    e6kComms["mta"].append(net_connect.send_command(e6kComms["mta"][0]))
    print('\n', '#' * 20, hostname, "  - MTA - ", '#' * 20)
    print(" >>> ", (e6kComms["mta"][0]))
    print(e6kComms["mta"][1])
    e6kComms["sip"].append(net_connect.send_command(e6kComms["sip"][0]))
    print('\n', '#' * 20, hostname, "  - SIP - ", '#' * 20)
    print(" >>> ", (e6kComms["sip"][0]))
    print(e6kComms["sip"][1])
    e6kComms["partial"].append(net_connect.send_command(e6kComms["partial"][0]))
    print('\n', '#' * 20, hostname, "  - PARTIAL - ", '#' * 20)
    print(" >>> ", (e6kComms["partial"][0]))
    print(e6kComms["partial"][1])
    e6kComms["init"].append(net_connect.send_command(e6kComms["init"][0]))
    print('\n', '#' * 20, hostname, "  - INIT - ", '#' * 20)
    print(" >>> ", (e6kComms["init"][0]))
    print(e6kComms["init"][1])

    e6kComms["ofdm-dw"].append(net_connect.send_command(e6kComms["ofdm-dw"][0]))
    print('\n', '#' * 20, hostname, "  - OFDM - ", '#' * 20)
    print(" >>> ", (e6kComms["ofdm-dw"][0]))
    print(e6kComms["ofdm-dw"][1])



    e6kComms["interface-cable"].append(net_connect.send_command(e6kComms["interface-cable"][0]))
    print('\n', '#' * 20, hostname, "  - INTERFACES - ", '#' * 20)
    print(" >>> ", (e6kComms["interface-cable"][0]))
    print(e6kComms["interface-cable"][1])
    e6kComms["summary"].append(net_connect.send_command(e6kComms["summary"][0]))
    print('\n', '#' * 20, hostname, "  - CM SUMMARY - ", '#' * 20)
    print(" >>> ", (e6kComms["summary"][0]))
    print(e6kComms["summary"][1])
    e6kComms["summary-port"].append(net_connect.send_command(e6kComms["summary-port"][0]))
    print('\n', '#' * 20, hostname, "  - CM SUMMARY PORT  - ", '#' * 20)
    print(" >>> ", (e6kComms["summary-port"][0]))
    print(e6kComms["summary-port"][1])
    e6kComms["stb-total"].append(net_connect.send_command(e6kComms["stb-total"][0]))
    print('\n', '#' * 20, hostname, "  - STB TOTAL  - ", '#' * 20)
    print(" >>> ", (e6kComms["stb-total"][0]))
    print(e6kComms["stb-total"][1])
    e6kComms["mta-total"].append(net_connect.send_command(e6kComms["mta-total"][0]))
    print('\n', '#' * 20, hostname, "  - MTA TOTAL  - ", '#' * 20)
    print(" >>> ", (e6kComms["mta-total"][0]))
    print(e6kComms["mta-total"][1])

    e6kComms["ertr"].append(net_connect.send_command(e6kComms["ertr"][0]))
    print('\n', '#' * 20, hostname, "  - CPE ERTR TOTAL  - ", '#' * 20)
    print(" >>> ", (e6kComms["ertr"][0]))
    print(e6kComms["ertr"][1])
    e6kComms["environ"].append(net_connect.send_command(e6kComms["environ"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW ENVIROMENT  - ", '#' * 20)
    print(" >>> ", (e6kComms["environ"][0]))
    print(e6kComms["environ"][1])
    e6kComms["default"].append(net_connect.send_command(e6kComms["default"][0]))
    print('\n', '#' * 20, hostname, "  - ROUTE DEFAULT  - ", '#' * 20)
    print(" >>> ", (e6kComms["default"][0]))
    print(e6kComms["default"][1])
    e6kComms["bgp-nei"].append(net_connect.send_command(e6kComms["bgp-nei"][0]))
    print('\n', '#' * 20, hostname, "  - BGP NEIGHBOR  - ", '#' * 20)
    print(" >>> ", (e6kComms["bgp-nei"][0]))
    print(e6kComms["bgp-nei"][1])
    e6kComms["bgp-summ"].append(net_connect.send_command(e6kComms["bgp-summ"][0]))
    print('\n', '#' * 20, hostname, "  - BGP INTERFACE  - ", '#' * 20)
    print(" >>> ", (e6kComms["bgp-summ"][0]))
    print(e6kComms["bgp-summ"][1])
    e6kComms["lacp"].append(net_connect.send_command(e6kComms["lacp"][0]))
    print('\n', '#' * 20, hostname, "  - LACP SUMMARY  - ", '#' * 20)
    print(" >>> ", (e6kComms["lacp"][0]))
    print(e6kComms["lacp"][1])
    e6kComms["pim-inter"].append(net_connect.send_command(e6kComms["pim-inter"][0]))
    print('\n', '#' * 20, hostname, "  - PIM INTERFACE  - ", '#' * 20)
    print(" >>> ", (e6kComms["pim-inter"][0]))
    print(e6kComms["pim-inter"][1])
    e6kComms["pim-nei"].append(net_connect.send_command(e6kComms["pim-nei"][0]))
    print('\n', '#' * 20, hostname, "  - PIM NEIGHBOR  - ", '#' * 20)
    print(" >>> ", (e6kComms["pim-nei"][0]))
    print(e6kComms["pim-nei"][1])

    e6kComms["version"].append(net_connect.send_command(e6kComms["version"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW VERSION  - ", '#' * 20)
    print(" >>> ", (e6kComms["version"][0]))
    print(e6kComms["version"][1])

    e6kComms["running"].append(net_connect.send_command(e6kComms["running"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW RUNNING  - ", '#' * 20)
    print(" >>> ", (e6kComms["running"][0]))
    print(e6kComms["running"][1])

    output = net_connect.send_command_timing("exit")
    print (output)

    net_connect.disconnect()
    return  e6kComms
    
def verifycbr8Status(ccapAddress, commands, ccapName):    # Recibe diccionario del dispositivo, comandos ad-hoc y nombre del host

    ip_addr = "10.247.2.149"
    passw = "Javier2021"
    linux = {
        'device_type': 'linux',
        'ip': ip_addr,
        'username': "root",
        'password': passw,
        'port': 22,
        'timeout': 30 * 60,

    }


    net_connect = ConnectHandler(**linux)
    print(net_connect.find_prompt())
    output = net_connect.send_command("uname -a")
    print(output)

    cbr8Comms = commands.copy()
    cbr8Comms["cpu-sorted"] = ["show processes cpu sorted"]
    cbr8Comms["cpu-history"] = ["show processes cpu history "]


    cbr8Comms["partial"] = ["show cable modem partial-mode | count online"]
    cbr8Comms["init"] = ["show cable modem | count  init"]
    cbr8Comms["ofdm-dw"] = ["show cable modem wideband | count online"]

    cbr8Comms["linecard"] = ["show platform"]
    cbr8Comms["power"] = ["show environment power"]
    cbr8Comms["environ-alarms"] = ["show environment | include alarms"]
    cbr8Comms["alarms"] = ["show facility-alarm status "]

    cbr8Comms["redundancy"] = ["show redundancy"]
    cbr8Comms["redundancy-lc"] = ["show redundancy linecard all"]
    cbr8Comms["cgd-associations"] = ["show cable cgd-associations "]
    cbr8Comms["summary"] = ["show cable modem summary total"]
    cbr8Comms["device-summary"] = ["show cable modem  docsis device-class summary total"]
    cbr8Comms["wideband"] = ["show cable modem wideband | count online"]
    cbr8Comms["dsg-cfr"] = ["show cable dsg cfr"]

    cbr8Comms["default"] = ["show ip route 0.0.0.0"]
    cbr8Comms["bgp-nei"] = ["show ip bgp neighbor"]
    cbr8Comms["bgp-summ"] = ["show ip bgp summary"]
    cbr8Comms["lacp"] = ["show lacp neighbor"]
    cbr8Comms["pim-inter"] = ["show ip pim interface"]
    cbr8Comms["pim-nei"] = ["show ip pim neighbor"]
    cbr8Comms["version"] = ["show version"]
    cbr8Comms["fiber-node"] = ["show cable fiber-node | include MDD|Fiber-Node"]
    cbr8Comms["running"] = ["show running-config"]

    print("#" * 6, "COMANDOS A EJECUTAR EN: ", ccapName, "#" * 6)
    for line in cbr8Comms.keys():
        print(cbr8Comms[line][0])

    host_loging = "ssh u605930@"+ccapAddress
    print (host_loging)

    output = net_connect.send_command_timing(host_loging)
    # output = net_connect.send_command_timing("ssh u605930@CMT1.CBS1-E6K")
    print(output)
    time.sleep(5)  # retardo para evitar falla de TACACS
    if "(yes/no)? " in output:
        output = net_connect.send_command_timing("yes")
        print (output)
    output = net_connect.send_command_timing("V4l3nt1n02")
    print(output)
    time.sleep(20)
    if "Password:" in output or "password:" in output:
        output = net_connect.send_command_timing("V4l3nt1n02")
    time.sleep(10)
    if "Password:" in output:
        output = net_connect.send_command_timing("V4l3nt1n02")
    time.sleep(12)
    if "Password:" in output:
        output = net_connect.send_command_timing("D4nt3S0f14")


    hostname = net_connect.find_prompt()
    hostname = hostname[:-1]
    print("\n***** CBR8 objetivo: ", hostname, "*****")

    print ( net_connect.send_command("terminal leng 0"))

    cbr8Comms["cpu-sorted"] = ["show processes cpu sorted"]
    cbr8Comms["cpu-history"] = ["show processes cpu history "]

    cbr8Comms["cpu-sorted"].append(net_connect.send_command(cbr8Comms["cpu-sorted"][0]))
    print('\n', '#' * 20, hostname, "  - CPU SORTED  - ", '#' * 20)
    print(" >>> ", cbr8Comms["cpu-sorted"][0])
    print(cbr8Comms["cpu-sorted"][1])

    cbr8Comms["cpu-history"].append(net_connect.send_command(cbr8Comms["cpu-history"][0]))
    print('\n', '#' * 20, hostname, "  - CPU HISTORY - ", '#' * 20)
    print(" >>> ", cbr8Comms["cpu-history"][0])
    print(cbr8Comms["cpu-history"][1])


    cbr8Comms["cm_online"].append(net_connect.send_command(cbr8Comms["cm_online"][0]))
    print('\n', '#' * 20, hostname, "  - CM online  - ", '#' * 20)
    print(" >>> ", cbr8Comms["cm_online"][0])
    print(cbr8Comms["cm_online"][1])
    cbr8Comms["deco_legacy"].append(net_connect.send_command(cbr8Comms["deco_legacy"][0]))
    print('\n', '#' * 20, hostname, "  - DECO LEGACY - ", '#' * 20)
    print(" >>> ", (cbr8Comms["deco_legacy"][0]))
    print(cbr8Comms["deco_legacy"][1])
    cbr8Comms["deco_flow"].append(net_connect.send_command(cbr8Comms["deco_flow"][0]))
    print('\n', '#' * 20, hostname, "  - DECO FLOW - ", '#' * 20)
    print(" >>> ", (cbr8Comms["deco_flow"][0]))
    print(cbr8Comms["deco_flow"][1])
    cbr8Comms["mta"].append(net_connect.send_command(cbr8Comms["mta"][0]))
    print('\n', '#' * 20, hostname, "  - MTA - ", '#' * 20)
    print(" >>> ", (cbr8Comms["mta"][0]))
    print(cbr8Comms["mta"][1])
    cbr8Comms["sip"].append(net_connect.send_command(cbr8Comms["sip"][0]))
    print('\n', '#' * 20, hostname, "  - SIP - ", '#' * 20)
    print(" >>> ", (cbr8Comms["sip"][0]))
    print(cbr8Comms["sip"][1])
    cbr8Comms["partial"].append(net_connect.send_command(cbr8Comms["partial"][0]))
    print('\n', '#' * 20, hostname, "  - PARTIAL - ", '#' * 20)
    print(" >>> ", (cbr8Comms["partial"][0]))
    print(cbr8Comms["partial"][1])

    cbr8Comms["init"].append(net_connect.send_command(cbr8Comms["init"][0]))
    print('\n', '#' * 20, hostname, "  - INIT - ", '#' * 20)
    print(" >>> ", (cbr8Comms["init"][0]))
    print(cbr8Comms["init"][1])

    cbr8Comms["ofdm-dw"].append(net_connect.send_command(cbr8Comms["ofdm-dw"][0]))
    print('\n', '#' * 20, hostname, "  - OFDM - ", '#' * 20)
    print(" >>> ", (cbr8Comms["ofdm-dw"][0]))
    print(cbr8Comms["ofdm-dw"][1])

    cbr8Comms["linecard"].append(net_connect.send_command(cbr8Comms["linecard"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW PLATAFORM - ", '#' * 20)
    print(" >>> ", (cbr8Comms["linecard"][0]))
    print(cbr8Comms["linecard"][1])

    cbr8Comms["power"].append(net_connect.send_command(cbr8Comms["power"][0]))
    print('\n', '#' * 20, hostname, "  - ENVIROMENT POWER - ", '#' * 20)
    print(" >>> ", (cbr8Comms["power"][0]))
    print(cbr8Comms["power"][1])

    cbr8Comms["environ-alarms"].append(net_connect.send_command(cbr8Comms["environ-alarms"][0]))
    print('\n', '#' * 20, hostname, "  - ENVIROMENT ALARMS - ", '#' * 20)
    print(" >>> ", (cbr8Comms["environ-alarms"][0]))
    print(cbr8Comms["environ-alarms"][1])

    cbr8Comms["alarms"].append(net_connect.send_command(cbr8Comms["alarms"][0]))
    print('\n', '#' * 20, hostname, "  - FACILITY ALARMS  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["alarms"][0]))
    print(cbr8Comms["alarms"][1])

    cbr8Comms["redundancy"].append(net_connect.send_command(cbr8Comms["redundancy"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW REDUNDANCY  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["redundancy"][0]))
    print(cbr8Comms["redundancy"][1])

    cbr8Comms["redundancy-lc"].append(net_connect.send_command(cbr8Comms["redundancy-lc"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW REDUNDANCY LINECARD - ", '#' * 20)
    print(" >>> ", (cbr8Comms["redundancy-lc"][0]))
    print(cbr8Comms["redundancy-lc"][1])

    cbr8Comms["cgd-associations"].append(net_connect.send_command(cbr8Comms["cgd-associations"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW CGD-ASSOCIATIONS - ", '#' * 20)
    print(" >>> ", (cbr8Comms["cgd-associations"][0]))
    print(cbr8Comms["cgd-associations"][1])

    cbr8Comms["summary"].append(net_connect.send_command(cbr8Comms["summary"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW CABLE MODEM SUMMARY - ", '#' * 20)
    print(" >>> ", (cbr8Comms["summary"][0]))
    print(cbr8Comms["summary"][1])

    cbr8Comms["device-summary"].append(net_connect.send_command(cbr8Comms["device-summary"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW DEVICE SUMMARY - ", '#' * 20)
    print(" >>> ", (cbr8Comms["device-summary"][0]))
    print(cbr8Comms["device-summary"][1])

    cbr8Comms["wideband"].append(net_connect.send_command(cbr8Comms["wideband"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW CABLE MODEM WIDEBAND - ", '#' * 20)
    print(" >>> ", (cbr8Comms["wideband"][0]))
    print(cbr8Comms["wideband"][1])

    cbr8Comms["dsg-cfr"].append(net_connect.send_command(cbr8Comms["dsg-cfr"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW DSG CONFIGURATION - ", '#' * 20)
    print(" >>> ", (cbr8Comms["dsg-cfr"][0]))
    print(cbr8Comms["dsg-cfr"][1])

    cbr8Comms["default"].append(net_connect.send_command(cbr8Comms["default"][0]))
    print('\n', '#' * 20, hostname, "  - ROUTE DEFAULT  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["default"][0]))
    print(cbr8Comms["default"][1])

    cbr8Comms["bgp-nei"].append(net_connect.send_command(cbr8Comms["bgp-nei"][0]))
    print('\n', '#' * 20, hostname, "  - BGP NEIGHBOR  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["bgp-nei"][0]))
    print(cbr8Comms["bgp-nei"][1])

    cbr8Comms["bgp-summ"].append(net_connect.send_command(cbr8Comms["bgp-summ"][0]))
    print('\n', '#' * 20, hostname, "  - BGP INTERFACE  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["bgp-summ"][0]))
    print(cbr8Comms["bgp-summ"][1])

    cbr8Comms["lacp"].append(net_connect.send_command(cbr8Comms["lacp"][0]))
    print('\n', '#' * 20, hostname, "  - LACP SUMMARY  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["lacp"][0]))
    print(cbr8Comms["lacp"][1])

    cbr8Comms["pim-inter"].append(net_connect.send_command(cbr8Comms["pim-inter"][0]))
    print('\n', '#' * 20, hostname, "  - PIM INTERFACE  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["pim-inter"][0]))
    print(cbr8Comms["pim-inter"][1])

    cbr8Comms["pim-nei"].append(net_connect.send_command(cbr8Comms["pim-nei"][0]))
    print('\n', '#' * 20, hostname, "  - PIM NEIGHBOR  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["pim-nei"][0]))
    print(cbr8Comms["pim-nei"][1])

    cbr8Comms["version"].append(net_connect.send_command(cbr8Comms["version"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW VERSION  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["version"][0]))
    print(cbr8Comms["version"][1])

    cbr8Comms["fiber-node"].append(net_connect.send_command(cbr8Comms["fiber-node"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW FIBER-NODE - ", '#' * 20)
    print(" >>> ", (cbr8Comms["fiber-node"][0]))
    print(cbr8Comms["fiber-node"][1])

    cbr8Comms["running"].append(net_connect.send_command(cbr8Comms["running"][0]))
    print('\n', '#' * 20, hostname, "  - SHOW RUNNING  - ", '#' * 20)
    print(" >>> ", (cbr8Comms["running"][0]))
    print(cbr8Comms["running"][1])

    output = net_connect.send_command_timing("exit")
    print (output)

    net_connect.disconnect()
    return  cbr8Comms



def verifyC100gStatus(ccapAddress, commands, ccapName):    # Recibe diccionario del dispositivo, comandos ad-hoc y nombre del host


    ip_addr = "10.247.2.149"
    passw = "Javier2021"
    linux = {
        'device_type': 'linux',
        'ip': ip_addr,
        'username': "root",
        'password': passw,
        'port': 22,
        'timeout': 30 * 60,

    }


    net_connect = ConnectHandler(**linux)
    print(net_connect.find_prompt())
    output = net_connect.send_command("uname -a")
    print(output)

    c100gComms = commands.copy()
    c100gComms["partial"] = ["show cable modem partial-service | count-only /"]
    c100gComms["init"] = ["show cable modem init | count-only /"]
    c100gComms["ofdm-dw"] = ["show cable modem bonding | count-only 33)"]

#    c100gComms["linecard"] = ["show linecard status"]
#    c100gComms["interface-cable"] = ["show interface cable-mac"]
#    c100gComms["summary"] = ["show cable modem summary"]
#    c100gComms["summary-port"] = ["show cable modem summary port"]
#    c100gComms["stb-total"] = ["show cable modem cpe-type stb count"]
#    c100gComms["mta-total"] = ["show cable modem cpe-type mta count "]
#    c100gComms["ertr"] = ["show cable modem cpe-type ertr count"]
#    c100gComms["ertr"] = ["show cable modem cpe-type ertr count"]
#    c100gComms["environ"] = ["show environment"]
#    c100gComms["default"] = ["show ip route 0.0.0.0"]
#    c100gComms["bgp-nei"] = ["show ip bgp neighbor"]
#    c100gComms["bgp-summ"] = ["show ip bgp summary"]
#    c100gComms["lacp"] = ["show lacp summary"]
#    c100gComms["pim-inter"] = ["show ip pim interface"]
#    c100gComms["pim-nei"] = ["show ip pim neighbor"]
#    c100gComms["version"] = ["show version"]
#    c100gComms["running"] = ["show running-config verbose"]
#
    print("#" * 6, "COMANDOS A EJECUTAR EN: ", ccapName, "#" * 6)
    for line in c100gComms.keys():
        print(c100gComms[line][0])

    host_loging = "ssh u605930@"+ccapAddress
    print (host_loging)

    #output = net_connect.send_command(host_loging, expect_string="password:")
    output = net_connect.send_command_timing(host_loging)
    time.sleep(3)  # retardo para evitar falla de TACACS
    if "(yes/no)" in output:
        output = net_connect.send_command_timing("yes")
        print (output)
    output = net_connect.send_command_timing("V4l3nt1n02")
    print(output)
    if "Permission denied" in output:
        time.sleep(4)
        output = net_connect.send_command_timing("V4l3nt1n02")
    if "Permission denied" in output:
        time.sleep(5)
        output = net_connect.send_command_timing("V4l3nt1n02")




    hostname = net_connect.find_prompt()
    hostname = hostname[:-1]
    print("\n***** C100G objetivo: ", hostname, "*****")
    net_connect.send_command("page off")
    c100gComms["cm_online"].append(net_connect.send_command(c100gComms["cm_online"][0]))
    print('\n', '#' * 20, hostname, "  - CM online  - ", '#' * 20)
    print(" >>> ", c100gComms["cm_online"][0])
    print(c100gComms["cm_online"][1])
    c100gComms["deco_legacy"].append(net_connect.send_command(c100gComms["deco_legacy"][0]))
    print('\n', '#' * 20, hostname, "  - DECO LEGACY - ", '#' * 20)
    print(" >>> ", (c100gComms["deco_legacy"][0]))
    print(c100gComms["deco_legacy"][1])
    c100gComms["deco_flow"].append(net_connect.send_command(c100gComms["deco_flow"][0]))
    print('\n', '#' * 20, hostname, "  - DECO FLOW - ", '#' * 20)
    print(" >>> ", (c100gComms["deco_flow"][0]))
    print(c100gComms["deco_flow"][1])
    c100gComms["mta"].append(net_connect.send_command(c100gComms["mta"][0]))
    print('\n', '#' * 20, hostname, "  - MTA - ", '#' * 20)
    print(" >>> ", (c100gComms["mta"][0]))
    print(c100gComms["mta"][1])
    c100gComms["sip"].append(net_connect.send_command(c100gComms["sip"][0]))
    print('\n', '#' * 20, hostname, "  - SIP - ", '#' * 20)
    print(" >>> ", (c100gComms["sip"][0]))
    print(c100gComms["sip"][1])
    c100gComms["partial"].append(net_connect.send_command(c100gComms["partial"][0]))
    print('\n', '#' * 20, hostname, "  - PARTIAL - ", '#' * 20)
    print(" >>> ", (c100gComms["partial"][0]))
    print(c100gComms["partial"][1])
    c100gComms["init"].append(net_connect.send_command(c100gComms["init"][0]))
    print('\n', '#' * 20, hostname, "  - INIT - ", '#' * 20)
    print(" >>> ", (c100gComms["init"][0]))
    print(c100gComms["init"][1])

    c100gComms["ofdm-dw"].append(net_connect.send_command(c100gComms["ofdm-dw"][0]))
    print('\n', '#' * 20, hostname, "  - OFDM - ", '#' * 20)
    print(" >>> ", (c100gComms["ofdm-dw"][0]))
    print(c100gComms["ofdm-dw"][1])



    output = net_connect.send_command_timing("exit")
    print (output)

    net_connect.disconnect()
    return c100gComms




def filterE6kInfo(target, file_name):
    info = {}
    full_dict = {}

    with open(file_name) as file:

        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format

        full_dict = (yaml.load(file, Loader=yaml.FullLoader))

        info = {}
        with open('cable-modem-e6k.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cm = template.ParseText(full_dict["cm_online"][1])
        info["cm_online"] = cm[0][0]

        if full_dict["deco_legacy"][0] != "!":
            with open('cpe-count-e6k.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["deco_legacy"][1])
            info["deco_legacy"] = cpe[0][0]
        else:
            info["deco_legacy"] = "0"
        if full_dict["deco_flow"][0] != "!":
            with open('cpe-count-e6k.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["deco_flow"][1])
            info["deco_flow"] = cpe[0][0]
        else:
            info["deco_flow"] = "0"
        if full_dict["mta"][0] != "!":
            with open('cpe-count-e6k.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["mta"][1])
            info["mta"] = cpe[0][0]
        else:
            info["mta"] = "0"
        if full_dict["sip"][0] != "!":
            with open('cpe-count-e6k.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["sip"][1])
            info["sip"] = cpe[0][0]
        else:
            info["sip"] = "0"
        with open('cpe_found-e6k.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["partial"][1])
        info["partial"] = cpe[0][0]

        with open('cpe-count-e6k.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["init"][1])
        cpe = template.ParseText(full_dict["ofdm-dw"][1])
        info["init"] = cpe[0][0]

        with open('cpe-count-e6k.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["ofdm-dw"][1])
        info["ofdm-dw"] = cpe[0][0]

    return (info)

def filterCbr8Info(target, file_name):
    info = {}
    full_dict = {}

    with open(file_name) as file:

        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format

        full_dict = (yaml.load(file, Loader=yaml.FullLoader))

        info = {}
        with open('cable-modem-cbr8.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cm = template.ParseText(full_dict["cm_online"][1])
        info["cm_online"] = cm[0][0]

        if full_dict["deco_legacy"][0] != "!":
            with open('cpe-count-cbr8.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["deco_legacy"][1])
            info["deco_legacy"] = cpe[0][0]
        else:
            info["deco_legacy"] = "0"
        if full_dict["deco_flow"][0] != "!":
            with open('cpe-count-cbr8.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["deco_flow"][1])
            info["deco_flow"] = cpe[0][0]
        else:
            info["deco_flow"] = "0"
        if full_dict["mta"][0] != "!":
            with open('cpe-count-cbr8.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["mta"][1])
            info["mta"] = cpe[0][0]
        else:
            info["mta"] = "0"
        if full_dict["sip"][0] != "!":
            with open('cpe-count-cbr8.fsm', 'r') as f:
                template = textfsm.TextFSM(f)
            cpe = template.ParseText(full_dict["sip"][1])
            info["sip"] = cpe[0][0]
        else:
            info["sip"] = "0"
        with open('cpe-count-cbr8.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["partial"][1])
        info["partial"] = cpe[0][0]

        with open('cpe-count-cbr8.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["init"][1])
        info["init"] = cpe[0][0]

        with open('cpe-count-cbr8.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["ofdm-dw"][1])
        info["ofdm-dw"] = cpe[0][0]

    return (info)


def filterC100gInfo (target, file_name):
    info = {}
    full_dict = {}

    with open(file_name) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        full_dict = (yaml.load(file, Loader=yaml.FullLoader))

    info = {}
    with open('cable-modem-c100g.fsm', 'r') as f:
        template = textfsm.TextFSM(f)
    cm = template.ParseText(full_dict["cm_online"][1])
    info["cm_online"] = cm[0][0]

    if full_dict["deco_legacy"][0] != "!":
        with open('cpe-count-c100g.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["deco_legacy"][1])
        info["deco_legacy"] = cpe[0][0]
    else:
        info["deco_legacy"] = "0"
    if full_dict["deco_flow"][0] != "!":
        with open('cpe-count-c100g.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["deco_flow"][1])
        info["deco_flow"] = cpe[0][0]
    else:
        info["deco_flow"] = "0"
    if full_dict["mta"][0] != "!":
        with open('cpe-count-c100g.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["mta"][1])
        info["mta"] = cpe[0][0]
    else:
        info["mta"] = "0"
    if full_dict["sip"][0] != "!":
        with open('cpe-count-c100g.fsm', 'r') as f:
            template = textfsm.TextFSM(f)
        cpe = template.ParseText(full_dict["sip"][1])
        info["sip"] = cpe[0][0]
    else:
        info["sip"] = "0"
    with open('cpe-count-c100g.fsm', 'r') as f:
        template = textfsm.TextFSM(f)
    cpe = template.ParseText(full_dict["partial"][1])
    info["partial"] = cpe[0][0]

    with open('cpe-count-c100g.fsm', 'r') as f:
        template = textfsm.TextFSM(f)
    cpe = template.ParseText(full_dict["init"][1])
    info["init"] = cpe[0][0]

    with open('cpe-count-c100g.fsm', 'r') as f:
        template = textfsm.TextFSM(f)
    cpe = template.ParseText(full_dict["ofdm-dw"][1])
    info["ofdm-dw"] = cpe[0][0]

    return (info)


### BUSCAR SCOPES DE CCAPs en INTRAWAY

def gather_scopes():
  output_directory = 'ccap_scopes.csv'
#  url = 'http://ftsltools.int.fibertel.com.ar/.test/INTRAWAY/scopes-domine.php'
#
  url = 'http://10.200.100.124/ftsltools/.test/INTRAWAY/scopes-domine.php'

#  try:
#    remove("ccap_scopes.csv")
#  except FileNotFoundError:
#    print("No hay archivo con informacion de scopes preexistente. Se inicia la descarga del mismo....")
#  filename = wget.download(url, out=output_directory)

  dict_ccap_scopes = {}
  list_ccap_scopes = list()

  with open('ccap_scopes.csv') as ccap_scopes_file:
    ccap_scopes_reader = csv.reader(ccap_scopes_file, delimiter=';')
    for row in ccap_scopes_reader:
      list_ccap_scopes.append(row)

  del list_ccap_scopes[0]

  for row in range(len(list_ccap_scopes)):
      for column in range(len(list_ccap_scopes[row])):
          list_ccap_scopes[row][column] = list_ccap_scopes[row][column].strip()

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



  for ccap in dict_ccap_scopes.keys():
  #    print(dict_ccap_scopes)
      for tag in dict_ccap_scopes[ccap].keys():
          if len(dict_ccap_scopes[ccap][tag]) == 0:

              dict_ccap_scopes[ccap][tag].append("No tiene Redes asociadas")

 # for ccap in dict_ccap_scopes.keys():
#      print(ccap, "-", dict_ccap_scopes[ccap])

  with open("ccap_scopes.yml", 'w') as file:
      yaml.dump(dict_ccap_scopes, file)

#gather_scopes()