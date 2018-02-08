#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import socket
import time
import re
import argparse
from subprocess import Popen, PIPE,STDOUT
arg=sys.argv[1]
arg1=sys.argv[2]
sites=[]
server=[]
serverlist=[]
nodeserver=[]
#filename='/home/anair/3par_DC/lunlist12'
#filename1='/home/anair/3par_DC/volmap1'
if sys.argv[1] == '-h' or sys.argv[1] == 'h':
        command1="cat /data01/home/svmso/mso-disk/unified/UniList | awk '{print $1}'"
        file1 = subprocess.Popen(command1,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        listoutput = file1.communicate()[0]
        print listoutput
	sys.exit(0)
node=sys.argv[2].upper()
if sys.argv[3] == 'active' or sys.argv[3] == 'Active':
        luncmd="ssh admin@%s lun mapping show -fields node,reporting-nodes" %arg
	volcmd="ssh admin@%s vol show -fields junction-path,node,security-style" %arg
        cmd = ['ping', '-c2','-W 5',arg]
        response = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        stdout, stderr = response.communicate()
        if response.returncode == 0:
                print "\n******admin password****** \n"
                file = subprocess.Popen(luncmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(10)
		file1 = subprocess.Popen(volcmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output= file.communicate()[0]
		output1= file1.communicate()[0]
                lines = output.splitlines()
		lines1 = output1.splitlines()
        else:
                print "%s is down" %arg
                sys.exit(0)
elif sys.argv[3] == 'backup' or  sys.argv[3] == 'Backup':
        filename='/data01/home/svmso/mso-disk/unified/ntaplun/'+arg+''
	filename1='/data01/home/svmso/mso-disk/unified/ntapvol/'+arg+''
        file = open(filename)
	lines = file.readlines()
	file1 = open(filename1)
	lines1 = file1.readlines()
serverlist=[]
nodeserver=[]
nasvol=[]
i=0
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
	print "\nServers connected to %s:\n" %node
	for k in range(0,len(serverlist)):
		if node in nodeserver[k]:
			print serverlist[k]
else:
	print "\nServer %s connected to node:\n" %node
	for k in range(0,len(serverlist)):
		if node in serverlist[k]:
			print nodeserver[k]
#file1= open(filename1)
#lines1=file1.readlines()
nasvol=[]
nasnode=[]
nasvserver=[]
nassecstyle=[]
cifs=[]
unix=[]
sites=[]
server=[]
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

print "CIFS \n"
for i in range(0,len(cifs)):
	print cifs[i]
	print "\n"
print "NFS\n"
for i in range(0,len(unix)):
        print unix[i]
        print "\n"
for i in nasvserver:
	server.append(i)
	if re.match("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",i[:7]):
		site=re.search("^[a-zA-Z][0-9][0-9][0-9][0-9][0-9][0-9]",i[:7])	
		if site.group() not in sites:
			sites.append(site.group())
	else:
			print "Internal server: %s" %(i)
print "\nSite ID for Servers connected to %s :\n" %arg1
for i in range(0,len(sites)):
                p=subprocess.Popen(shlex.split('/data01/mso/atlascli/GetSiteDetailsBySiteId.sh -s %s' % sites[i]),stdout=PIPE,stderr=STDOUT)
                output=p.communicate()[0].strip('\n')
                if "status=Normal" in output:
                        m = re.search("customerName(.*)",output)
                        #print(m.group())
                        print("%s %s" %(sites[i],m.group()))

