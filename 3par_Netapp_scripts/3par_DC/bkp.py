#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import socket
import re
sites=[]
server=[]
paths=[]
from subprocess import Popen, PIPE,STDOUT
arg=sys.argv[1]
p=socket.gethostbyname(arg)
#P=p.lower()
command="ssh svvsstat@%s showhost -pathsum" %arg
file = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print arg
#file = subprocess.check_output(['ssh','svvsstat@',p,' showhost',' -pathsum'])
#p = subprocess.Popen('ssh svvsstat@'p' showhost -pathsum', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#lines = pipe.splitlines()
output=file.communicate()[0]
print output
