#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import socket
import re
import argparse
if sys.argv[1] ==  '-h':
	parser = argparse.ArgumentParser(description='3Par host & node details.')
	parser.add_argument('integers', metavar='hostname', type=int, nargs='+',help='3Par host name')
	parser.add_argument('integers', metavar='node', type=int, nargs='+',help='node number')
	args = parser.parse_args()
	print args.accumulate(args.integers)
sites=[]
server=[]
paths=[]
from subprocess import Popen, PIPE,STDOUT
arg=sys.argv[1]
node=sys.argv[2] 
nodes=[]
p=socket.gethostbyname(arg)
#P=p.lower()
command="ssh svvsstat@%s showhost -pathsum" %arg
print "******svvsstat password****** \n"
file = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output= file.communicate()[0]
lines = output.splitlines()
print "\n"
for line in lines[1:]:
		columns=line.split()
		path=columns[3]
		nodes=columns[4]
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
print "Site ID for impacted servers are: \n"
for i in range(0,len(sites)):
		p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % sites[i]),stdout=PIPE,stderr=STDOUT)
		output=p.communicate()[0].strip('\n')
		if "status=Normal" in output:
			m = re.search("customerName(.*)",output)
			#print(m.group())
			print("%s %s" %(sites[i],m.group()))
print "\n"
print "Impacted Server list: \n"
for j in range(0,len(server)):
	print server[j] + " having paths from nodes:  " + paths[j]
print "\n"
print "Servers connected to node %s: \n" %node
for k in range(0,len(server)):
	if node in paths[k]:
		print server[k]
			


