from genome import *
from agree import *


# Ligature = namedtuple('Ligature', ['pre', 'on', 'off'])
# note = Ligature(e, 1, e)
# rest = Ligature(e, 1, e)
# ..

_ = '_'
e = None
comp = 'comp'
spec = 'spec'

# seed(9016)

voice_count = 2

templates = {
	'C': [
	{
		'rhythm': [
				 (0,1,0),
				 (1,0,0),
		         ],
		'figure': [
					'L',
					'H%',
		           ],
		'complement': {
			'category': 'T',
			'criterion': 'harmony',
			'receiver': 'harmony',
			'agree': harmony,
		},
	},
	],
	'T': [
	{
		'rhythm': [
				 (e,1,1),
				 (e,0,0),
		         ],
		'figure': [
					'HL%',
					'LH%',
		           ],
		'complement': {
			'category': 'V',
			'criterion': 'rhythm',
			'receiver': 'rhythm',
			'agree': None
		},
	},
	],
	'V': [
	{	# transitive
		'rhythm': [
				 (e,1,_),
				 (e,1,1),
		         ],
		'figure': [
					'L',
					'L',
		           ],
		'specifier': {
			'category': 'N',
			'criterion': 'rhythm',
			'receiver': 'rhythm',
			'agree': notes,
		},
		'complement': {
			'category': 'N',
			'criterion': 'figure',
			'receiver': 'figure',
			'agree': None
		},
	},
	{	# intransitive
		'rhythm': [
				 (1,_,e),
				 (1,1,e)				 
		         ],
		'figure': [
					'H%',
					'H%',
		           ],
		'specifier': {
			'category': 'N',
			'criterion': 'rhythm',
			'receiver': 'rhythm',
			'agree': None
		},
	},
	],
	'D': [
	{
		'rhythm': [
		         (1,1,1),
		         (1,1,1),
		         ],
	},
	{
		'rhythm': [
		         (e,1,e), 
		         (e,1,e),
		         ],
	},
	],
	'N': [
	{
		'rhythm': [
		         (e,1,e), 
		         (e,1,e),
		         ],
		'figure': [
					'HH%',
					'L%',
				   ],
		'specifier': {
			'category': 'D',
			'criterion': 'rhythm',
			'receiver': 'suffix',
			'agree': None
		},
	},
	],
}



lexicon = {}

for category, subcategories in templates.iteritems():
	for template in subcategories:
		lexicon[category] = make_category(2,2,template)


# for root in roots:
# 	score = addRoot(score,root)

# time_signature = indicatortools.TimeSignature((3, 8))
# meter = metertools.Meter(time_signature)
# for staff in score[:]:
#     attach(time_signature, staff)
#     # mutate(staff[:]).rewrite_meter(meter)
# 	# leaves = staff[:]
# 	# mutate(leaves).rewrite_meter(metertools.Meter((3, 8)))

# show(score)