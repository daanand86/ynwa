#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import re
sites=[]
server=[]
paths=[]
from subprocess import Popen, PIPE,STDOUT
p=sys.argv[1]
P=p.lower()
file = subprocess.check_output(['cat',P])
lines = file.splitlines()
#def server_site_list(lines):
print "\n"
for line in lines[1:]:
		columns=line.split()
		path=columns[3]
	#	paths.append(columns[4])
#		server.append(columns[1])
		if "--" not in path:
			if int(path) >=1:
				server.append(columns[1])
				paths.append(columns[4])
				if re.match("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",columns[1][:7]):
					site=re.search("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",columns[1][:7])
					if site.group() not in sites:
						sites.append(site.group())
				else:
					print "Internal server: %s" %(columns[1])
	
print "\n"
print "Site ID's for impacted servers are: \n"
for i in range(0,len(sites)-1):
		p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % sites[i]),stdout=PIPE,stderr=STDOUT)
		output=p.communicate()[0].strip('\n')
		if "status=Normal" in output:
			m = re.search("customerName(.*)",output)
			#print(m.group())
			print("%s %s" %(sites[i],m.group()))
print "\n"
print "Impacted Server list is: \n"
for j in range(0,len(server)-1):
	print server[j] + " having paths from node:  " + paths[j]
#	print paths[j]
		


