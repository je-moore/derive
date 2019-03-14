#!/usr/bin/python
# -*- coding: latin-1 -*-

from random import *
from agree import *

'''
(externally) merge two constituents:
take two roots:
	head (unsaturated feature structure)
	comp (saturated feature structure)
look for unvalued feature in head
	search for feature value in comp
	fill in head value: using agree/translation function for that feature
	place comp in head (comp is attribute of head)
'''

def derive(category, lexicon):
	lexeme = choice(lexicon[category])
	return project(lexeme, lexicon)

def project(lexeme, lexicon):

	if 'specifier' in lexeme:
		# select a specifier from lexicon
		specifier = choice(lexicon[lexeme['specifier']['category']])

		# embed specifier in lexeme (spec is attribute of head)
		lexeme['specifier']['projection'] = project(specifier, lexicon)

		# assign head feature value to matching spec feature via agree function
		if 'receiver' in lexeme['specifier']:
			probe = lexeme
			goal = lexeme['specifier']
			criterion = lexeme['specifier']['criterion']
			receiver = lexeme['specifier']['receiver']

			lexeme[ receiver ] = inflect( probe, goal, criterion )

	if 'complement' in lexeme:
		# select a complement from lexicon
		complement = choice(lexicon[lexeme['complement']['category']])

		# embed complement in lexeme (comp is attribute of head)
		lexeme['complement']['projection'] = project(complement, lexicon)

		# assign head feature value to matching comp feature via agree function
		if 'receiver' in lexeme['complement']:
			probe = lexeme
			goal = lexeme['complement']
			criterion = lexeme['complement']['criterion']
			receiver = lexeme['complement']['receiver']

			lexeme[ receiver ] = inflect( probe, goal, criterion )

	if 'adjuncts' in lexeme:
		# todo: select, project 0 or more adjuncts, embed in lexeme
		lexeme = adjoin(lexeme, lexicon)

	return lexeme


def inflect( probe, goal, criterion ):
	if 'agree' in goal:
		if callable(goal['agree']):
			value = goal['agree']( probe, goal['projection'], criterion )
		else:
			value = probe[criterion]
	else:
		value = probe[criterion]
	return value


def adjoin(lexeme):
	return lexeme
	# linear insertion points can be chosen during spellout


'''

Example Derivation

   start_symbol  =  specify(C)
     specify(C)  =  ( ø, complement(C) )
  complement(C)	 =  ( C, specify(T) )
     specify(T)	 =  ( ø, complement(T) )
  complement(T)	 =  ( T, specify(V) )
     specify(V)	 =  ( specify(N), complement(V) )
     specify(N)	 =  ( D, complement(N) )
  complement(N)	 =  ( N, ø )
	  adjoin(N)	 =  ( N, ø, specify(P) )
     specify(P)	 =  ( ø, complement(P) )
  complement(P)	 =  ( P, specify(N) )
     specify(N)	 =  ( D, complement(N) )
  complement(N)	 =  ( N, ø )
  complement(V)	 =  ( V, specify(N) )
     specify(N)	 =  ( D, complement(N) )
  complement(N)	 =  ( N, ø )

( ø, ( C, ( ø, ( T, ( ( Det, ( N, ø, ( P, ( Det, ( N, ø ) ) ) ) ), ( V, ( Det, ( N, ø ) ) ) ) ) ) ) )


'''