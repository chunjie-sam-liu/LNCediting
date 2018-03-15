#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by Poison on 2010-06-19.
Copyright (c) 2010 2Alien. All rights reserved.
"""
import os
import re
import math

MIRNA_WORK_DIR = os.path.dirname(os.path.abspath(__file__)) + "/" # working path
RNAFOLD_PATH = './RNAfold' # RNAfold binary path
MAGICK_CONVERT_PATH = '/usr/bin/convert' # MAGICK tools path



def RNAfold(seq, probability = False, outfile = None, cons = None):
	os.chdir(MIRNA_WORK_DIR)
	query = 'echo "' + seq + '" | ' + RNAFOLD_PATH + ' -noLP -d2'
	if cons:
		query = 'echo "' + seq + '\n' + cons + '" | ' + RNAFOLD_PATH + ' -noLP -C -d2'
	if probability:
		query += ' -p'
	pipe = os.popen(query)
	lines = pipe.readlines()
	pipe.close()
	try:
		res = {}
		m = re.match(r'^(?P<struct>[\(\)\.]+)\s+\(\s*(?P<mfe>[-\d\.]+)\).*$', lines[1])
		res['struct'] = m.group('struct')
		res['mfe'] = float(m.group('mfe'))
		try:
			ps = open('rna.ps', 'r')
		except IOError:
			raise IOError, os.getcwd()
		process = False
		pairs = []
		for line in ps.readlines():
			if line.startswith('/pairs ['):
				process = True
				continue
			if line.startswith('] def') and process:
				break
			if process:
				m = re.match(r'\[(?P<i>\d+) (?P<j>\d+)\]', line)
				pairs.append([int(m.group('i')) - 1, int(m.group('j')) - 1])
		ps.close()
		if outfile:
			os.rename('rna.ps', outfile)
		else:
			os.remove('rna.ps')
		res['pairs'] = pairs
		if not probability:
			return res
		m = re.match(r'^(?P<struct>[\(\)\.\,\{\}\|\:]+)\s+\[\s*(?P<fe>[-\d\.]+)\].*$', lines[2])
		n = lines[4].split()
		ensemble = {}
		ensemble['struct'] = m.group('struct')
		ensemble['fe'] = float(m.group('fe'))
		res['ensemble'] = ensemble
		res['frequency'] = float(n[6][:-1])
		res['diversity'] = float(n[9])
		ps = open('dot.ps', 'r')
		length = len(seq)
		pp = [-1 for i in range(length)]
		pi = [0 for i in range(length)]
		sp = [0 for i in range(length)]
		for line in ps.readlines():
			m = re.match(r'(?P<i>\d+) (?P<j>\d+) (?P<p>[-\d\.]+) (?P<id>.box)', line)
			if not m:
				continue
			i = int(m.group('i')) - 1
			j = int(m.group('j')) - 1
			p = float(m.group('p'))
			if m.group('id') == 'ubox':
				p *= p
				pi[i] += p
				pi[j] += p
				if [i, j] in pairs:
					pp[i] = p
					pp[j] = p
				ss = 0
				if p > 0:
					ss = p * math.log(p)
				sp[i] += ss
				sp[j] += ss
		log2 = math.log(2)
		for i in range(length):
			sp[i] += (1 - pi[i]) * math.log(1 - pi[i])
			sp[i] = -sp[i] / log2
			if pp[i] == -1:
				pp[i] = 1 - pi[i]
		ps.close()
		os.remove('dot.ps')
		res['probabilitis']  = pp
		res['entropies'] = sp
		return res
	except IndexError, AttributeError:
		print('Please specify a correct RNAfold path, exit...')
		exit()
		return

# RNA color plotting fuction in postscript
RNA_score_header = '''
/range 0.8 def
/drawreliability {
  /Smax 1 def
  0
  coor {
    aload pop
    S 3 index get
    Smax div range mul
    invert {range exch sub} if
    1 1 sethsbcolor
    newpath
    fsize 2 div 0 360 arc
    fill
    1 add
  } forall
} bind def
/colorbar { % xloc yloc colorbar -> []
  /STR 8 string def
  gsave
    xmin xmax add size sub 2 div
    ymin ymax add size sub 2 div translate
    size dup scale
    translate
    0.015 dup scale
    /tics 64 def
    gsave
      10 tics div 1 scale
      0 1 tics
      {
	  dup 0 moveto 0.5 add
	  tics div range mul
	  invert {range exch sub} if
	  1 1 sethsbcolor
	  1 0 rlineto 0 1 rlineto -1 0 rlineto closepath fill
      } for
    grestore
    0 setgray
    -0.1 1.01 moveto (0) gsave 0.1 dup scale show grestore
    10 1.01 moveto Smax STR cvs
    gsave 0.1 dup scale dup stringwidth pop -2 div 0 rmoveto show grestore
  grestore
} bind def
'''

# RNA commenting fuction in postscript
RNA_comm_header = '''
/drawcomment {
  outlinecolor
  1 setlinewidth
  newpath
  comm {aload pop
     /msg exch def
     /msgl msg length def
     /idx exch 1 sub def
     /myoff coor idx get def
     /offa myoff 0 get def
     /offb myoff 1 get def
     offa offb moveto
     idx 1500 gt

     {offa -50 add offb 0 add lineto
0 0 rlineto
-100 0   rmoveto}
     {offa 0  sub offb -50 add lineto
  	0 0 rlineto
-50 -8 rmoveto}

     ifelse
	
     msg show
}
forall



  stroke
} bind def
'''

RNA_score_footer = '''

/invert true def
drawreliability
'''

RNA_comm_footer = '''
drawcomment
'''

def plotRNA(filename, src = None, scores = None, seq = None, comm = None, cons = None):
	os.chdir(MIRNA_WORK_DIR)
	ps_file = 'rna.ps'
	if src:
		ps_file = src
	else: # if scr not defined, call rnafold to generate a base ps file
		query = 'echo "' + seq + '" | ' + RNAFOLD_PATH + ' -noLP -d2'
		if cons:
			query = 'echo "' + seq + '\n' + cons + '" | ' + RNAFOLD_PATH + ' -noLP -C -d2'
		pipe = os.popen(query)
		pipe.close()
	if scores: # generate postscript style scores list
		scores_list = '/S [\n'
		for s in scores:
			scores_list += '  %7.5f\n' % s
		scores_list += '] def\n'
	if comm: # generate postscript style comment list
		comm_list = '/comm [\n'
		for item in comm:
			comm_list += '[%d (%s)]\n' % (item[0], item[1])
		comm_list += '] def\n'
	if scores or comm: # insert the needed postscript function and data to ps file
		ps = open(ps_file, 'r')
		lines = ps.readlines()
		ps.close()
		#os.remove(ps_file)
		index = 0
		for i, line in enumerate(lines):
			if line == 'drawoutline\n':
				index = i
				break
		content = ''
		if scores:
			content += RNA_score_header + scores_list + RNA_score_footer
		if comm:
			content += RNA_comm_header + comm_list + RNA_comm_footer
		lines.insert(index, content)
		ps_file = filename + '.eps'
		eps = open(ps_file, 'w')
		eps.write(''.join(lines))
		eps.close()
	else:
		os.rename(ps_file, filename + '.eps')
	if os.path.exists(MAGICK_CONVERT_PATH):
		os.system(MAGICK_CONVERT_PATH + ' ' + filename + '.eps ' + filename + '.png')
		os.system(MAGICK_CONVERT_PATH + ' ' + filename + '.eps ' + filename + '.pdf')
