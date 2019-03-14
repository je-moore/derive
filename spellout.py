from pitch import *
from derive import *
from agree import *
from grammar import *
from engrave import *

'''
flatten derivation into list of notes and rests

'''

duration = Duration(1,8)

# record where projections begin and end linearly (for barlines and annotation)
# (category, start_index, stop_index)
boundary_indices = []
# position cursor
cursor = 0

pitch_cursor = []		# per voice
previous_pitch = []		# per voice
for voice in xrange(0,voice_count):
	pitch_cursor.append(0)
	previous_pitch.append(0)

def pad(notes):
	notes_count = len(notes)
	for x in xrange(1, notes_count):
		index = notes_count-x
		if notes[index][0] == 'R':
			supplement = notes[index][1]
			notes.pop( index )
			notes[index-1] = ( notes[index-1][0], notes[index-1][1] + supplement )
	return notes


def reset_cursors():
	# reset global cursors
	global boundary_indices
	boundary_indices = []
	global cursor
	cursor = 0
	global pitch_cursor
	pitch_cursor = []		# per voice
	global previous_pitch
	previous_pitch = []		# per voice
	for voice in xrange(0,voice_count):
		pitch_cursor.append(0)
		previous_pitch.append(0)


def render(start_symbol, lexicon):
	global boundary_indices
	global cursor
	global pitch_cursor

	# create tree representation of a sentence
	derivation = derive(start_symbol,lexicon)

	# reduce derivation to pitch, rhythm, annotation data
	# initialize scaffold with one staff for each voice
	voice_count = len(lexicon[start_symbol][0]['rhythm'])
	scaffold = []
	for x in xrange(0,voice_count):
		voice = []
		scaffold.append(voice)

	reset_cursors()

	scaffold = spellout(derivation, start_symbol, scaffold)

	# print scaffold
	# flatten each voice, extend notes into subsequent rests
	for index, staff in enumerate(scaffold):
		notes = [item for sublist in staff for item in sublist]
		notes = pad(notes)
		scaffold[index] = notes
	print scaffold
	print boundary_indices
	
	phrase = engrave(scaffold, boundary_indices)
	return phrase	


def spellout(derivation, category, scaffold):

	# global cursor
	start_index = cursor
	if 'specifier' in derivation:
		scaffold = spellout(derivation['specifier']['projection'], derivation['specifier']['category'], scaffold)

	# print category
	scaffold = realize(derivation, scaffold)

	if 'complement' in derivation:
		scaffold = spellout(derivation['complement']['projection'], derivation['complement']['category'], scaffold)

	stop_index = cursor

	boundary_indices.insert( 0, (category, start_index, stop_index) )
	return scaffold


def realize(lexeme, scaffold):
	global cursor
	global pitch_cursor
	global previous_pitch
	for voice in xrange(0, voice_count):
		pitches = get_pitches(lexeme['harmony'][voice], pitch_cursor[voice])
		ligature = get_ligature(pitches, lexeme['rhythm'][voice])
		curve = get_curve(ligature, lexeme['figure'][voice], previous_pitch[voice])
		previous_pitch[voice] = pitch_cursor[voice]
		pitch_cursor[voice] = pitches[-1]
		realization = []
		for position in xrange(0, len(curve)):
			note = curve[position]
			if note:
				realization.append( (note, duration) )
			if voice == 0:
				cursor += 1
		scaffold[voice].append( realization )
	return scaffold


score = Score()
for x in xrange(0,voice_count):
	score.append(Staff())


for x in xrange(1,10):
	phrase = render('C', lexicon)
	for i in xrange(0,voice_count):
		# score[i] = Staff(score[i][:]
		score[i].extend(phrase[i])
		score[i].append(Measure(TimeSignature((2, 4)), "R2"))

show(score)

