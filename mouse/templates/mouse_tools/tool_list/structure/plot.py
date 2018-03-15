#!/usr/bin/env python
# encoding: utf-8
"""
plot.py

Created by Poison on 2010-06-19.
Copyright (c) 2010 2Alien. All rights reserved.
"""

import sys
import getopt
from utils import *


help_message = '''
-i, --input	input ps file
-s, --score	positional color scores
-m, --comm	positional comment list file
			use tab to divide position number and comment for each records
			for example:
			4	point 4
			65	point 65
-a, --autocl	auto color type, 0: disable, 1: pair pobability, 2: entropy [default 0]
-o, --output	output file base name, without suffix
example:
python plot.py -s 0.9,0.9,0.8,0.8,0.5,0.6,0.9,0.9,0.8,0.8,0.5,0.6 aaauuucuugaa
python plot.py -i mir-1-1.ps -a 1 -m mir-1-1_comm.txt
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:i:s:m:a:", ["help", "output=", "input=", "score=", "comm=", "autocl="])
		except getopt.error, msg:
			raise Usage(msg)
		output = 'rnaplot'
		seq = None
		ps_file = None
		scores = None
		comm = None
		atype = 0
		for option, value in opts:
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
			if option in ("-i", "--input"):
				ps_file = value
			if option in ("-s", "--score"):
				scores = [float(i) for i in value.split(',')]
			if option in ("-m", "--comm"):
				comm = []
				fd = open(value, 'r')
				for line in fd.readlines():
					if line.startswith('#'):
						continue
					record = line.strip().split('\t')
					comm.append([int(record[0]), record[1]])
				fd.close()
			if option in ("-a", "--autocl"):
				atype = int(value)
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
		
	# processing
	if not ps_file:
		seq = argv[-1]
	if not ps_file and atype > 0:
		ps_file = output
		result = RNAfold(seq, probability = True, outfile = ps_file, cons = None)
		if atype == 1:
			scores = result['probabilitis']
		elif atype == 2:
			scores = result['entropies']
	plotRNA(output, src = ps_file, scores = scores, seq = seq, comm = comm, cons = None)


if __name__ == "__main__":
	sys.exit(main())
