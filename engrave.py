from grammar import *
from abjad import *

'''
set beaming within each measure according to remaining boundaries
annotate beginning/end of each projection with lexical category

'''

def engrave(scaffold, boundary_indices):

	# group notes into bars using syntactic boundaries; todo: beams
	boundaries = get_boundaries(boundary_indices)
	bars = get_bars(boundaries)
	print 'boundaries', boundaries
	print 'bars', bars

	# convert to lilypond markup using abjad API
	phrase = Container()
	for voice in xrange(0,voice_count):
		caret = 0
		staff = Staff()
		staff_index = 0
		for i, bar in enumerate(bars):
			if bar%2 == 0:
				time_signature = TimeSignature((bar/2, 4))
			else:
				time_signature = TimeSignature((bar, 8))
			pointer = Duration(0,8)
			measure = Measure(time_signature)
			while pointer < time_signature.duration:
				# print 'caret', caret,
				# print 'len(scaffold[', voice, '])', len(scaffold[voice])
				one = scaffold[voice]
				two = scaffold[voice][caret]
				pitch = scaffold[voice][caret][0]
				duration = scaffold[voice][caret][1]

				# chop higher prime durations
				subdurations = []
				assignable = duration.equal_or_lesser_assignable
				subdurations.append(assignable)
				assigned = assignable
				while assigned < duration:
					# print 'assigned', assigned, 'duration', duration
					remainder = duration - assigned
					assignable = remainder.equal_or_lesser_assignable
					subdurations.append(assignable)
					assigned += assignable
				# if len(subdurations) > 1:
				# 	print 'subdurations', subdurations
				for index, subduration in enumerate(subdurations):
					if pitch == 'R':
						measure.append(Rest(subduration))
					else:
						measure.append(Note(pitch, subduration))

				# tie chopped notes
				if pitch != 'R' and len(subdurations) > 1:
					attach(Tie(), measure[-len(subdurations):])

				# update loop
				pointer += duration
				caret += 1

				# kludge: bug omits final rests in voice[0]...?
				if pointer != time_signature.duration and len(scaffold[voice]) == caret:
					print 'kludge!'
					# print 'time_signature.duration - pointer', time_signature.duration - pointer, 'time_signature.duration', time_signature.duration, 'pointer', pointer
					measure.append(Rest(time_signature.duration - pointer))
					pointer = time_signature.duration
			# print '--- voice', voice, 'bar', i, 'done ---'
			# print 'time_signature.duration', time_signature.duration, 'pointer', pointer
			# print 'time_signature.duration', time_signature.duration, 'pointer', pointer
			staff.append(measure)
		phrase.append(staff)
	return phrase


def get_boundaries(boundary_indices):
	# make sorted list of boundaries
	boundaries = []
	for boundary_index in boundary_indices:
		boundaries.append(boundary_index[1])
		boundaries.append(boundary_index[2])
	boundaries = list(set(boundaries))
	sorted(boundaries, key=int)
	return boundaries


def get_bars(boundaries):
	# merge short durations between boundaries to get bars
	spans = [t - s for s, t in zip(boundaries, boundaries[1:])]
	beat_count = sum(spans)
	bars = []
	while len(spans) > 1:
		bar = spans.pop(0)
		while bar < 5:
			remaining = sum(spans)
			if remaining < 5:
				bar += remaining   # or make stunted bar
				break
			else:
				bar += spans.pop(0)
		if sum(bars) != beat_count:
			bars.append(bar)

	return bars


'''
# scaffolding
[
 [('R', Duration(1, 8)), (-6, Duration(1, 4)), (-5, Duration(1, 8)), (0, Duration(1, 8)), (-3, Duration(1, 8)), (-4, Duration(1, 8)), (1, Duration(1, 8)), (4, Duration(1, 8)), (7, Duration(1, 8)), (6, Duration(1, 8)), (5, Duration(1, 8)), (10, Duration(1, 8)), (16, Duration(1, 8))],
 [(-7, Duration(1, 8)), (-6, Duration(1, 8)), (-3, Duration(3, 8)), (-4, Duration(1, 8)), (-8, Duration(1, 8)), (-6, Duration(1, 8)), (0, Duration(1, 8)), (3, Duration(1, 4)), (-3, Duration(1, 8)), (-7, Duration(1, 8)), (-5, Duration(1, 8)), (0, Duration(1, 8))]
]
# boundary_indices
[('C', 0, 15), ('T', 3, 15), ('V', 5, 15), ('N', 11, 15), ('D', 11, 14), ('N', 5, 9), ('D', 5, 8)]
'''