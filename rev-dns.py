#!/usr/bin/env python

# Python reverse dns script
# Goes through a list of ip addresses and tries to do a reverse lookup
import sys
import dns.resolver,dns.reversename
#import re
from netaddr import *
from time import sleep

if len(sys.argv) < 3:
    print "Usage: ./rev.py iplist.txt dnsserver"
    exit()
else:
    pass

# Setup delay so that we have the option of not sending a ton of queries in a short span of time...completely optional
delay = raw_input("Delay in seconds (default = 0): ")
if delay == "" or delay == "0":
    delay = 0
else:
    delay = int(delay)
ipfile = open(sys.argv[1],"r").readlines()
dnsserver = sys.argv[2]
resolver = dns.resolver.Resolver()
# Set DNS Server
resolver.namerservers = [dnsserver]
for i in ipfile:
    try:
        # Match if the IP address is a range using CIDR
        #if re.match('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$',i):
        if "/" in i:
            ip_list = list(IPNetwork(i))
            for e in sorted(ip_list):
                # Convert IPNetwork value to standard str type. Isolates the ip.
                e = str(e)
                # Format the ip in reverse
                ip = '.'.join(reversed(e.split("."))) + ".in-addr.arpa"
                # Try to resolve the IP address
                try:
                    answer = resolver.query(ip, "PTR")
                # If the query fails, go to next iteration of the loop
                except:
                    continue
                # Set answered to 1 because python is linear and will set it to 1 after the try.
                answered = 1
                if answered == 1:
                    for a in answer:
                        print e, " - ",a
                else:
                    # If for some reason answered does not equal 1, continue
                    continue
                # Sleep for specified amount of time
                sleep(delay)
        # If it's not a CIDR range, proceed with resolving
        else:
            i = i.rstrip()
            # Format the ip in reverse
            ip = '.'.join(reversed(i.split("."))) + ".in-addr.arpa"
            answer = resolver.query(ip, "PTR")
            for a in answer:
                print i, " - ",a
            # Sleep for specified amount of time
            sleep(delay)
    except Exception, e:
        # IF the entire think pukes, print the output and try to continue the loop.
        print e
        continue
    