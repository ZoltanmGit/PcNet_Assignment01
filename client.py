import sys
from subprocess import PIPE, Popen
import time
import csv
import json

"""
Válasszuk ki az első és utolsó 10 nevet a listából, írjunk egy python programot, ami végig megy a leszűkített 20 elemű listán és minden címre lefuttatja a traceroute és ping toolokat, majd az eredményeket rendezett formában két fájlba írja!

Script paraméterezése: python3 client.py hosts.csv (NEM MILLIÓ SOROS ÉS EGY HOST TÖBBSZÖR IS SZEREPELHET!!!)

Traceroute paraméterek: max. 30 hopot vizsgáljunk

Ping paraméterek: 10 próba legyen
"""


csvdata = []
with open(sys.argv[1]) as file:
    reader = csv.reader(file)
    SomeList = list(reader)
    csvdata = csvdata + SomeList[:10] + SomeList[-10:]
#PING
ListOfProgramsPing = []
ListOfPings=[]
for site in csvdata:
    p = Popen(["ping", '-n', '10', site[1]], stdout = PIPE)
    temp = (site[1],p)
    ListOfProgramsPing.append(temp)
for Item in ListOfProgramsPing:
    output = Item[1].communicate()[0].decode("utf-8")
    output = output.replace('\n','')
    output = output.replace('\r','')
    Tempdict = {
        "target" : Item[0],
        "output" : output
    }
    ListOfPings.append(Tempdict)
pingdict = {
    "date" : "20190929",
    "system" : "windows",
    "pings" : ListOfPings
}
with open("ping.json", "w") as write_file:
    json.dump(pingdict, write_file)
#TRACE
ListOfProgramsTrace = []
ListOfTraces=[]
for site in csvdata:
    p = Popen(["tracert", '-h', '30', site[1]], stdout = PIPE) #Stars every Popen
    temp = (site[1],p)
    ListOfProgramsTrace.append(temp)
print("Traces Started")
for Item in ListOfProgramsTrace:
    output = Item[1].communicate()[0].decode("utf-8")
    output = output.replace('\n','')
    output = output.replace('\r','')
    Tempdict = {
        "target" : Item[0],
        "output" : output
    }
    ListOfTraces.append(Tempdict)
tracedict = {
    "date" : "20190929",
    "system" : "windows",
    "traces" : ListOfTraces
}
with open("traceroute.json", "w") as write_file:
    json.dump(tracedict, write_file)