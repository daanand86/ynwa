#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import re
from subprocess import Popen, PIPE,STDOUT
#print "argument is ", sys.argv[1]
p=sys.argv[1]
P=p.lower()
filename=P+'vserverlist'
print filename
file = open(filename)
lines = file.readlines()
for i in lines:
        #print i
        if "NAS" in i or "SAN" in i:
                site=i[:7]
                p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % site),stdout=PIPE,stderr=STDOUT)
        #       output=p.communicate()[0].strip('\n')
                output=p.communicate()[0]
                if "status=Normal" in output:
                        m = re.search("customerName(.*)",output)
                #       print("Vserver is %s %s" %(i,m.group()))
                        print('Vserver is ' +i +' ' +m.group())




