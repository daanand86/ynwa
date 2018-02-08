#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import socket
import re
import argparse
from subprocess import Popen, PIPE,STDOUT
#arg=sys.argv[1]
sites=[]
server=[]
serverlist=[]
nodeserver=[]
#command="ssh admin@%s lun mapping show -fields node,reporting-nodes" %arg
#file = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#output= file.communicate()[0]
filename='/home/anair/3par_DC/lunlist123'
file = open(filename)
lines = file.readlines()
for line in lines[2:]:
	columns=line.split()
#	actnode=columns[3]
	server=columns[2]
	if columns[2] not in serverlist:
		serverlist.append(columns[2])
x=len(serverlist)
for line in lines[1:]:
        columns=line.split()
	for i in x:
		if serverlist[i] == columns[2]:
			if columns[3] not in nodeserver[i]:
				nodeserver[i].append(columns[3])
for j in x:
	print ("server %s having path from nodes %s",(serverlist[j],nodeserver[j]))
