#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import re
sites=[]
server=[]
from subprocess import Popen, PIPE,STDOUT
file = subprocess.check_output(['cat','3parhostname'])
lines = file.splitlines()
def server_site_list(lines):
	for line in lines[1:]:
		columns=line.split()
		path=columns[3]
		server.append()
		if "--" not in path:
			if int(path) >=1:
				if re.match("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",columns[1][:7]):
					site=re.search("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",columns[1][:7])
					if site.group() not in x:
						x.append(site.group())
				else:
					print "Internal server %s" %(columns[1])
	return x;
def siteid(x):
	for i in range(0,len(x)-1):
		p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % x[i]),stdout=PIPE,stderr=STDOUT)
		output=p.communicate()[0].strip('\n')
		if "status=Normal" in output:
			m = re.search("customerName(.*)",output)
			print('Customer is ' +i +' ' +m.group())
	return;
for j in range(0,len(server)-1):
	print server[j]
		


