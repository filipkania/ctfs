from scapy.all import *
from scapy.layers.dns import DNSRR, DNS, DNSQR
import base64

reader = rdpcap("./otd.pcap")
for p in reader:
    if p.haslayer(DNS):
        if isinstance(p.qd, DNSQR):
            name = p.qd.qname
        elif isinstance(p.an, DNSRR):
            name = p.an.rdata
        else:
            continue

        if len(parts := name[:-1].split(b".")) > 2:
            print(base64.b64decode(parts[0]))
