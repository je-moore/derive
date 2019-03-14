#!/usr/bin/python
# -*- coding: latin-1 -*-

import datetime
from copy import deepcopy
from random import random
from random import randint
from random import choice
from random import seed
from pitch import *

_ = '_'
e = None

def make_base():
	return choice([ (e,_,e), (_,_,e), (e,_,_), (_,_,_) ])

def make_figure():
	return choice([ 'L%', 'H%', 'L', 'H', 'LL%', 'LH%', 'HL%', 'HH%' ])

def make_note():
	return randint(0,1)

def make_harmony():
	return (choice(levels), randint(0,5081))

def make_lexeme(voice_count = 1):
	lexeme = {
		'rhythm': [],
		'figure': [],
		'harmony': []
	}
	base = make_base()
	for voice in xrange(0,voice_count):
		rhythm = []
		for unit in base:
			if unit == None:
				rhythm.append( None )
			if unit != None:
				rhythm.append( make_note() )
		lexeme['rhythm'].append( tuple(rhythm) )
		lexeme['figure'].append( make_figure() )
		lexeme['harmony'].append( make_harmony() )
	return lexeme


def fill_lexeme(template, voice_count):
	lexeme = deepcopy(template)
	if 'rhythm' in lexeme:
		base = make_base()
		for voice in xrange(0,voice_count):
			if type(lexeme['rhythm'][voice]) is tuple:
				null_indices = tuple([i for i, x in enumerate(lexeme['rhythm'][voice]) if x == None])
				# 'lexeme[\'rhythm\'][voice] (', lexeme['rhythm'][voice], ') null_indices:', null_indices
				if null_indices == ():
					base = (_,_,_)
				if null_indices == (0,):
					base = (e,_,_)
				if null_indices == (2,):
					base = (_,_,e)
				if null_indices == (0,2):
					base = (e,_,e)
				break
		for voice in xrange(0,voice_count):
			rhythm = []
			if type(lexeme['rhythm'][voice]) is tuple:
				model = lexeme['rhythm'][voice]
			else:
				model = base
			for unit in model:
				if unit == None:
					rhythm.append( None )
				if unit == '_':
					rhythm.append( make_note() )
				if isinstance(unit, int):
					rhythm.append( unit )
			lexeme['rhythm'][voice] = tuple(rhythm)

	else:
		lexeme['rhythm'] = []
		base = make_base()
		for voice in xrange(0,voice_count):
			rhythm = []
			for unit in base:
				if unit == None:
					rhythm.append( None )
				if unit == None:
					rhythm.append( make_note() )
			lexeme['rhythm'].append( tuple(rhythm) )

	if 'figure' in lexeme:
		for voice in xrange(0,voice_count):
			if lexeme['figure'][voice] == '_':
				lexeme['figure'][voice] = make_figure()
	else:
		lexeme['figure'] = []
		for voice in xrange(0,voice_count):
			lexeme['figure'].append( make_figure() )

	if 'harmony' in lexeme:
		for voice in xrange(0,voice_count):
			if type(lexeme['harmony'][voice]) is tuple:
				layer = lexeme['harmony'][voice][0]
				position = lexeme['harmony'][voice][1]
				if not layer in levels:
					layer = choice(levels)
				if not position in range(0,5082):
					position = randint(0,5081)
				lexeme['harmony'][voice] = layer, position
			else:
				lexeme['harmony'][voice] = make_harmony()
	else:
		lexeme['harmony'] = []
		for voice in xrange(0,voice_count):
			lexeme['harmony'].append( make_harmony() )

	return lexeme


def make_category(size=1, voice_count=1, template=None):
	collection = []
	print 'template', template
	for x in xrange(0,size):
		lexeme = None
		if template is None:
			lexeme = make_lexeme(voice_count)
			print 'whoa!!!'
		else:
			lexeme = fill_lexeme(template, voice_count)
			print 'lexeme', lexeme
		print ''
		collection.append(lexeme)
	return collection


# 
# example_lexeme = {		# lexeme length (1-3)			 --> number of beats; not implemented yet
# 	'rhythm': [0,1],	# [pickup, afterbeat] 		 --> Is there a pickup or afterbeat event attached to each beat?
# 	'notes': [ 			# [voice1, voice2, ... ]
# 		[0,0,1],		# [ pickup, down, ricochet ] --> note: 0, rest: 1
# 		[0,0,1],
# 		[0,0,1]
# 	],
# 	'figure': [		# [voice1, voice2, ... ]
# 		[0,0,1],   		# [ pickup, down, ricochet ] --> same: 0, step: ±1, skip: ±2
# 		[1,2,0],
# 		[-1,-1,-1]
# 	],
# 	'harmony': [		# [voice1, voice2, ... ]
# 		'A1',			# intervallic address
# 		'A3',
# 		'C3',
# 	]
# }
#
# example_template = {
# 	'rhythm': [1, 0],
# 	'notes': [['_', 0, '_'], ['_', 1, '_']],
# 	'figure': [[0, '_', '_'], [0, '_', '_']],
# 	'harmony': ['A1', '_']
# }
# print make_category(5,2,template)
#
