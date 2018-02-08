#! /usr/bin/python
import shlex
import os
import subprocess
import sys
import re
import argparse
parser = argparse.ArgumentParser(description='3Par host & node details.')
parser.add_argument('integers', metavar='hostname', type=int, nargs='+',help='3Par host name')
#parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max,help='sum the integers (default: find the max)')
parser.add_argument('integers', metavar='node', type=int, nargs='+',help='node number')
args = parser.parse_args()
print args.accumulate(args.integers)
