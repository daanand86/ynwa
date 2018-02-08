#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import socket
import re
import argparse
if sys.argv[1] == '-h' or sys.argv[1] == 'h':
	command1="ls -l /data01/home/svmso/mso-disk/hostsid2/ | awk '{if ($5 != 0)print $9;}'"
	file1 = subprocess.Popen(command1,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	listoutput = file1.communicate()[0]
	print listoutput
	parser = argparse.ArgumentParser(description='3Par host & site ID  Info.')
	parser.add_argument('characters', metavar='hostname', type=int, nargs='+',help='3Par host name')
	parser.add_argument('integers', metavar='node', type=int, nargs='+',help='node number')
	parser.add_argument('characters', metavar='config', type=int, nargs='+',help='Active or Backup Config')
	args = parser.parse_args()
	print args.accumulate(args.characters)
	sys.exit(0)
if len(sys.argv) < 4:
        print """Script need 4 parameters \n\nUsage: ./3parsid.py 3Par-hostname node# active|backup"""
        sys.exit(0)
sites=[]
sitesimp=[]
server=[]
paths=[]
from subprocess import Popen, PIPE,STDOUT
arg=sys.argv[1]
node=sys.argv[2] 
nodes=[]
if sys.argv[3] == 'active' or sys.argv[3] == 'Active':
	command="ssh svvsstat@%s showhost -pathsum" %arg
	#print "\n******svvsstat password****** \n"
	cmd = ['ping', '-c2','-W 5',arg]
	response = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	stdout, stderr = response.communicate()
	if response.returncode == 0:
		print "\n******svvsstat password****** \n"
		file = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output= file.communicate()[0]
		lines = output.splitlines()
	else:
		print "%s is down" %arg
		sys.exit(0)
elif sys.argv[3] == 'backup' or  sys.argv[3] == 'Backup':
	filename='/data01/home/svmso/mso-disk/hostsid2/'+arg+''	
	file = open(filename)
	lines = file.readlines()
print "\n"
#print len(sys.argv)
for line in lines[1:]:
		columns=line.split()
		path=columns[3]
		if "--" not in columns[0]:
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
	
print "\nSite ID for Servers connected to %s : \n" %arg
for i in range(0,len(sites)):
		p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % sites[i]),stdout=PIPE,stderr=STDOUT)
		output=p.communicate()[0].strip('\n')
		if "status=Normal" in output:
			m = re.search("customerName(.*)",output)
			#print(m.group())
			print("%s %s" %(sites[i],m.group()))
print "\nImpacted Server list: \n"
for j in range(0,len(server)):
	print server[j] + " having paths from nodes:  " + paths[j]
print "\nServers connected to node %s: \n" %node
for k in range(0,len(server)):
	if node in paths[k]:
		print server[k]
		if re.match("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",server[k][:7]):
			siteimp=re.search("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",server[k][:7])
			if siteimp.group() not in sitesimp:
				sitesimp.append(siteimp.group())
print "\nSite ID for servers connected to node %s:\n" %node
for m in range(0,len(sitesimp)):
		p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % sites[m]),stdout=PIPE,stderr=STDOUT)
                output=p.communicate()[0].strip('\n')
                if "status=Normal" in output:
                        q = re.search("customerName(.*)",output)
                        #print(m.group())
                        print("%s %s" %(sitesimp[m],q.group()))
		
print "\n"

