from random import choice
from pitch import *
from genome import *
from copy import copy

'''correlate probe features to goal features'''

# select previous position in same level
def harmony(probe,goal,criterion):
	source = copy(goal[criterion])
	# destination = copy(probe[feature])
	destination = []
	for address in source:
		destination.append( ( address[0], address[1]-1 ) )
	return destination


def notes(probe,goal,criterion):
	source = copy(goal[criterion])
	destination = copy(probe['notes'])
	# print destination
	for voice, notes in enumerate(source):
		decremented_unit = destination[voice][-1] - 1
		destination[voice][-1] = max( decremented_unit, -2 )
	# print destination
	return destination

def figure(probe,goal,criterion):
	source = copy(goal[criterion])
	destination = copy(probe['figure'])
	# print destination
	for voice, figure in enumerate(source):
		decremented_unit = destination[voice][-1] - 1
		destination[voice][-1] = max( decremented_unit, -2 )
	# print destination
	return destination


