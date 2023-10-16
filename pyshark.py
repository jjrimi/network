import sys
from scapy.all import *
print(conf.ifaces)
while True:
    sniff(prn = lambda x:x.show())