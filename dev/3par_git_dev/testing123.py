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
node=sys.argv[1]
filename='/home/anair/3par_DC/lunlist12'
filename1='/home/anair/3par_DC/volmap1'
serverlist=[]
nodeserver=[]
nasvol=[]
i=0
file = open(filename)
lines = file.readlines()
for line in lines[2:-2]:
	columns=line.split()
	server=columns[2]
	actnode=columns[3]
	if columns[2] not in serverlist:
		serverlist.append(columns[2])
		nodeserver.append([])
        	nodeserver[i].append(columns[3])
        	i=i+1
	else:
		if columns[3] not in nodeserver[serverlist.index(columns[2])]:
			nodeserver[serverlist.index(columns[2])].append(columns[3])
if "NTAP" in node:
	print "\nServers connected to this node:\n"
	for k in range(0,len(serverlist)):
		if node in nodeserver[k]:
			print serverlist[k]
else:
	print "\nServer %s connected to node:\n" %node
	for k in range(0,len(serverlist)):
		if node in serverlist[k]:
			print nodeserver[k]
file1= open(filename1)
lines1=file1.readlines()
nasvol=[]
nasnode=[]
nasvserver=[]
nassecstyle=[]
cifs=[]
unix=[]
for line in lines1[2:-2]:
    columns=line.split()
    if "-" not in columns[3]:
            if "root" not in columns[1]:
                    if "ROOT" not in columns[1]:
                            if columns[0] not in nasvserver:
                                    nasvserver.append(columns[0])
                                    nasvol.append([])
                                    nasvol[nasvserver.index(columns[0])].append(columns[1])
                                    nasnode.append([])
                                    nasnode[nasvserver.index(columns[0])].append(columns[4])
		            	    nassecstyle.append([])
				    nassecstyle[nasvserver.index(columns[0])].append(columns[2])
print "\nNAS vservers are \n"
for k in range(0,len(nasvserver)):
	if node in nasnode[k]:
		for i in nassecstyle[k]:
			if i == "ntfs":
				cifs.append(nasvserver[k])
			elif i == "unix":
				unix.append(nasvserver[k])
print "CIFS\n"
print cifs
print "\nNFS"
print unix
				
		
		
