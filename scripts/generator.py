import random, os, os.path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-language', default='en')
parser.add_argument('-characters', type=str, default='all')
parser.add_argument('-chars', default='')
parser.add_argument('-kern', default='none')
parser.add_argument('-kernchars', default='')
parser.add_argument('-kernlevel', default='0')
parser.add_argument('-lettervariety', default='0')
parser.add_argument('-pairvariety', default='0')
parser.add_argument('-generate')
parser.add_argument('-case', default='normal')
parser.add_argument('-frequencies', default='none')
args = parser.parse_args()

text_length = 3000

uppercase = 'AÁÀÂÄĂĀÃÅĄǺẠÆǼBCĆĊĈČÇDĎĐÐEÉÈĖÊËĚĔĒĘFGĠĜĞĢHĤĦIÍÌÎÏĬĪĨĮJĴKĶLĹĿĽĻŁMNŃŇÑŅŊOÓÒÔÖŎŌÕŐØǾƠŒPQRŔŘŖSŚŜŠŞTŤŢÞŦUÚÙÛÜŬŪŨŮŲŰƯVWẂẀŴẄXYÝŶŸZŹŻŽΑΆΒΓΔΕΈΖΗΉΘΙΊΪΚΛΜΝΞΟΌΠΡΣΤΥΎΫΦΧΨΩΏАБВГҐЃДЂЕЁЄЖЗЅИІЇЙЈКЌЛЉМНЊОПРСТЋУЎФХЦЧЏШЩЪЫЬЭЮЯ'
lowercase = 'aáàâäăāãåąǻạæǽbcćċĉčçdďđðeéèėêëěĕēęfgġĝğģhĥħiíìîïĭīĩįjĵkĸķlĺŀľļłmnńňñņŉŋoóòôöŏōõőøǿơœpqrŕřŗsśŝšştťţþŧuúùûüŭūũůųűưvwẃẁŵẅxyýŷÿzźżžαάβγδεέζηήθιίϊκλμνξοόπρςστυύϋΰφχψωώабвгґѓдђеёєжзѕиіїйјќлљмнњопрстћуўфхцчџшщъыьэюяßıк'
arabic = 'ءآأؤإئابةتثجحخدذرزسشصضطظعغػؼؽؾؿـفقكلمنهوى'
letters = uppercase + lowercase + arabic
uppercase_set = set(uppercase)
lowercase_and_arabic_set = set(lowercase + arabic)
letters_set = set(letters)

casedict = {}
# Establish lowercase to uppercase character mapping
for char in lowercase:
	uc = char.upper()
	if len(uc) == 1 and uc != char:
		casedict[char] = uc
casedict['\u0131'] = 'I'

########################################################################################################################
########################################################################################################################

print('''
<!doctype html>
<html>
<head>
	<title>Just Another Test Text Generator</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<style type="text/css">
		html { overflow-y: auto; background: #eee; font-family:monospace; }
	</style>
</head>
<body>
	<p id="content">
''')

print("languages: ")
input_languages = args.language.split('+')
for lang in input_languages:
		print(lang)

print("&nbsp;&nbsp;&nbsp;characters: ")
if args.characters == "all":
		print("all characters")
		characters = ''
else:
		temp = args.chars
		characters = ''
		for i in range(len(temp)):
				if args.case == "allcaps" and str(temp[i]) in casedict:
						characters += casedict[temp[i]]
				else:
						if (temp[i] != '\xdf'):
							characters += temp[i]
		print(characters)

print("<br/>kerning: ")
if args.kernlevel != "0":
	if args.kern == "typ":
			print("typical pairs")
	else:
			print(args.kernchars)
else: print("not affected")

kernglobal = 0
if args.kernlevel == "s3":
	kernglobal = -1.0
	print("suppress at -3")
elif args.kernlevel == "s2":
	kernglobal = -0.6
	print("suppress at -2")
elif args.kernlevel == "s1":
	kernglobal = -0.3
	print("suppress at -1")
elif args.kernlevel == "0":
	kernglobal = 0
elif args.kernlevel == "b1":
	kernglobal = 0.3
	print("boost at 1")
elif args.kernlevel == "b2":
	kernglobal = 0.6
	print("boost at 2")
elif args.kernlevel == "b3":
	kernglobal = 0.9
	print("boost at 3")

print("&nbsp;&nbsp;&nbsp;letter variety: ")
equalisation = 0.007 * int(args.lettervariety)
print(" ", args.lettervariety)

print("&nbsp;&nbsp;&nbsp;pair variety: ")
equalis_pair = 0.01 * int(args.pairvariety)
print(" ", args.pairvariety)

print("<br><br>")

########################################################################################################################
########################################################################################################################

triplets_filename = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'languages', 'triplets' )
for lang in input_languages:
		triplets_filename += "_" + lang
triplets_filename += ".txt"

if not os.path.isfile(triplets_filename):
	triplets_filename = triplets_filename.replace( 'languages', 'cache' )

file_output_merged = None
if not os.path.isfile(triplets_filename):
	threshold = 4
	file_output_merged = "combined from"
	
	# these are the two values used for the average (median-ish)
	n = len(input_languages)
	averg1 = n/3
	averg2 = (n+2)/3
	
	# load all files/lists
	triplets = []
	inputs = []
	for i in range(n):
		f=open( os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'languages', 'triplets_'+input_languages[i]+'.txt'), 'r' )
		file_output_merged += " " + input_languages[i]
		triplets.append({})
		inputs = f.readlines()
		f.close()
		del inputs[0]
		for t in inputs:
			triplets[i][t.split()[1]] = t.split()[0]
	
	# build main array
	combi = {}
	for i in range(n):
		for tri in triplets[i]:
			if tri in combi:
				combi[tri].append(int(triplets[i][tri]))
			else:
				combi[tri] = [ int(triplets[i][tri]) ]
	
	# build the averages array
	averages = {}
	for t in combi:
	
		lct = len(combi[t])
		for i in range( n - lct ):
			combi[t].append(0)
	
		sum_v = 0
		for i in combi[t]:
			sum_v += i
		
		if len(t) == 3:  # if it is a triplet
			# this is the arithmetic average of the averg1-th most frequent and the averg2-th most frequent (most frequent: n - 1)
			averages[t] = 0.5 * ( combi[t][int(averg1)] + combi[t][int(averg2)] )
		else:   # if it is not a triplet, i.e. word length
			averages[t] = int( sum_v/n )
	
	fom = [ ]
	
	# build output strings
	for t in averages:
		if len(t) == 3:
			if averages[t] > threshold:
				fom.append("\n" + str( int(averages[t]) ) + "\t" + t )
		else:
			fom.append("\n" + str( averages[t] ).rjust(20) + "\t" + t )
	
	fom.sort()
	for m in fom:
		file_output_merged += m
	
	# write output file
	try:
		f=open(triplets_filename, 'w')
		f.write(file_output_merged)
		f.close()
	except IOError:
		# no writing permissions
		pass
		
########################################################################################################################
########################################################################################################################


# initial bits and stuff
wordlen_in  = [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ]
wordlen_out = [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ]
wordmax = 6
wordsum_in  = wordmax
wordsum_out = wordmax-2
tweaklimit = 30.0
tweak_upto = 15
text_length += 10
random.seed()
file_output = ("")
if characters != "":
	characters = "_" + characters
frequencymeter = {}
frequencytotal = 1
numberofletters = 0

frequencymeterUC = {}
frequencytotalUC = 1
numberoflettersUC = 0

pairmeter = {}
pairtotal = 1
numberofpairs = 0

# import kerning file
if kernglobal != 0:
	if args.kern == "typ":
		kern_filename = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'kerning.txt' )
		f=open(kern_filename, 'r')
		inputs = f.readlines()
		f.close()
		del inputs[0]
		kerntweaks = {}
		for inp in inputs:
			kerntweaks[inp.split()[1]] = 1.0 * int(inp.split()[0])**kernglobal
	else:
		kerntweaks = {}
		for inp in args.kernchars.split():
			kerntweaks[inp] = 100.0 ** kernglobal
	 
# import file
if file_output_merged:
	inputs = file_output_merged.split( '\n' )
else:
	f=open(triplets_filename, 'r')
	inputs = f.readlines()
	f.close()
del inputs[0]

# build wordlen_in
while inputs:
	line = inputs[0].strip()
	if not line:
		del inputs[0]
		continue
	parts = line.split()
	if len(parts) < 2:
		break
	count_str, key = parts[0], parts[1]
	if key.startswith('word'):
		try:
			idx = int(key[4:7])
			if idx < len(wordlen_in):
				wordlen_in[idx] += int(count_str)
				wordsum_in += int(count_str)
		except (ValueError, IndexError):
			pass
		del inputs[0]
	else:
		break

# build duplets
duplets = {}
for inp in inputs:
	temp = inp.split()[1]
	t = ''
	for i in range(len(temp)):
		if args.case == "allcaps" and str(temp[i]) in casedict:
				t += casedict[temp[i]]
		else:
				t += temp[i]
	if args.case == "capitalized":
		if t[0] == '_' and t[1] in casedict:
			continue
		if t[1] == '_' and t[2] in casedict:
			continue

	v = int(inp.split()[0])
	# ignore all triplets that contain the wrong characters
	if characters != "":
		if not t[0] in characters : continue
		if not t[1] in characters : continue
		if not t[2] in characters : continue
	if t[0:2] in duplets:
		if t[2] in duplets[t[0:2]]:
			duplets[t[0:2]][ t[2] ] += v
		else:
			duplets[t[0:2]][ t[2] ] = v
	else:
		duplets[t[0:2]] = { t[2] : v }

# clean dead ends
for step in range(2):
	dead_duplets = []
	for d in duplets:
		dead_letters = []
		for v in duplets[d]:
			if d[1]+v not in duplets:
				dead_letters.append(v)
		for v in dead_letters:
			del duplets[d][v]
		if len(duplets[d]) == 0:
			dead_duplets.append(d)
	for d in dead_duplets:
		del duplets[d]

duplets_sorted = {d: sorted(duplets[d].items()) for d in duplets}

# pre-calculate multipliers
char_multipliers = {}
if characters != "":
	for c in set(characters):
		char_multipliers[c] = 2 ** (characters.count(c) - 1)

# build text
if characters != "" and not "." in characters:
	current = random.choice(characters) + "_"
else: current = "._"
wordtmp = 0

for i in range(text_length):
	
	# check for end of word
	if current[1] in letters_set:
		wordtmp += 1
	else:
		if current[0] in letters_set:
			if wordtmp > wordmax: wordtmp = wordmax
			wordlen_out[wordtmp] += 1
			wordsum_out += 1
		wordtmp = 0
	
	# set tweakblank factor
	if wordtmp >= wordmax:
		tweakblank = ( wordtmp - wordmax + 1 ) * 60
	elif wordtmp != 0:
		tweakblank = (1.0 * (wordlen_in[wordtmp]*wordsum_out) / (wordlen_out[wordtmp]*wordsum_in))**4
		if wordtmp > tweak_upto and tweakblank < equalisation*50:
			tweakblank = equalisation * 50 + 2
		elif tweakblank > tweaklimit:
			tweakblank = tweaklimit
		elif tweakblank < 0.25:
			tweakblank = 0.25
	else:
		tweakblank = 1
		
	if current in duplets_sorted:
		cumulative = []
		sum = 1
		lastone = i
		options = duplets_sorted[current]
		for char_j, count in options:
			# set multiplier
			multiplier = char_multipliers.get(char_j, 1)

			# set tweakletter
			if char_j in lowercase_and_arabic_set:
				count_j = frequencymeter.get(char_j, 1)
				eff_num_l = numberofletters + (0 if char_j in frequencymeter else 1)
				tweakletter = 1.0 + equalisation * ( (frequencytotal/count_j/eff_num_l)*5 - 1)
			elif char_j in uppercase_set:
				count_j = frequencymeterUC.get(char_j, 1)
				eff_num_l_uc = numberoflettersUC + (0 if char_j in frequencymeterUC else 1)
				tweakletter = 1.0 + equalisation * ( (frequencytotalUC/count_j/eff_num_l_uc)*5 - 1)
			else:
				tweakletter = tweakblank

			# set tweakpair
			currentpair = current[1]+char_j
			tweakpair = 1.0
			if '_' not in currentpair:
				count_p = pairmeter.get(currentpair, 4)
				eff_num_pairs = numberofpairs + (0 if currentpair in pairmeter else 1)
				tweakpair = 1.0 + equalis_pair * ( (pairtotal/count_p/eff_num_pairs)*5 - 1)

			# set tweakkernpair
			if kernglobal != 0 and currentpair in kerntweaks:
				tweakkernpair = kerntweaks[currentpair]
			else:
				tweakkernpair = 1

			sum += 1.0 * count * tweakletter * tweakpair * tweakkernpair * multiplier
			cumulative.append(sum)
		correction = 55000.0 / sum
		for idx in range(len(cumulative)):
				cumulative[idx] = int(cumulative[idx] * correction)
		randm = random.randrange(55000)
		for idx in range(len(cumulative)):
			if randm < cumulative[idx]:
				# new character is chosen
				chosen_next, _ = options[idx]

				# update frequencies
				if chosen_next in lowercase_and_arabic_set:
					if chosen_next not in frequencymeter:
						frequencymeter[chosen_next] = 1
						numberofletters += 1
					frequencymeter[chosen_next] += 1
					frequencytotal += 1
				elif chosen_next in uppercase_set:
					if chosen_next not in frequencymeterUC:
						frequencymeterUC[chosen_next] = 1
						numberoflettersUC += 1
					frequencymeterUC[chosen_next] += 1
					frequencytotalUC += 1

				current = current[1] + chosen_next
				file_output += chosen_next.replace("_"," ")

				if current not in pairmeter:
					pairmeter[current] = 4
					numberofpairs += 1
				pairmeter[current] += 1
				pairtotal += 1
				break
	else:
		if characters != "":
			current = current[1] + random.choice("____"+characters)
		else:
			current = current[1] + random.choice("____.....,,,,!?")
		file_output += current[1].replace("_"," ")  # replace with string.join

file_output += ".</bdo>&nbsp;&#150;&nbsp;generated by the <a href='https://justanotherfoundry.com'>JAF</a> Test Text Generator [https://justanotherfoundry.com]"

if args.frequencies == "output":
		# add character frequencies lowercase
		file_output += """<br><br><br>character frequencies:<br><br>
		<table border='0'><tr><td align='right'>"""
		tobesorted = []
		for c in frequencymeter:
				if frequencymeter[c] != 1:
					line = str(frequencymeter[c]-1).rjust(6) + "&nbsp;&nbsp;</td><td align='center'>"
					if "ar" in input_languages or "he" in input_languages or "fa" in input_languages:
						line += "<bdo dir='rtl'>"
					line += c + "</bdo>"
					tobesorted.append( line )
		tobesorted.sort()
		tobesorted.reverse()
		for c in tobesorted:
				file_output += c + "</td></tr><tr><td align='right'>"
		
		file_output += "&nbsp;</td></tr><tr><td align='right'>"

		# add character frequencies uppercase
		tobesorted = []
		for c in frequencymeterUC:
				if frequencymeterUC[c] != 1:
					line = str(frequencymeterUC[c]-1).rjust(6) + "&nbsp;&nbsp;</td><td align='center'>"
					if "ar" in input_languages or "he" in input_languages or "fa" in input_languages:
						line += "<bdo dir='rtl'>"
					line += c + "</bdo>"
					tobesorted.append( line )
		tobesorted.sort()
		tobesorted.reverse()
		for c in tobesorted:
				file_output += c + "</td></tr><tr><td align='right'>"

		file_output += "</td></tr></table>"
		file_output += """<br><br>pair frequencies:<br><br>
		<table border='0'><tr><td align='right'>"""

		# add pair frequencies
		tobesorted = []
		for c in pairmeter:
				if pairmeter[c] != 4:
					line = str(pairmeter[c]-4).rjust(6) + "&nbsp;&nbsp;</td><td align='center'>"
					if "ar" in input_languages or "he" in input_languages or "fa" in input_languages:
						line += "<bdo dir='rtl'>"
					line += c + "</bdo>"
					tobesorted.append( line )
		tobesorted.sort()
		tobesorted.reverse()
		for c in tobesorted:
				file_output += c + "</td></tr><tr><td align='right'>"
		file_output += "</td></tr></table>"

# write output file
if "ar" in input_languages or "he" in input_languages or "fa" in input_languages:
	print("<bdo dir='rtl'><p align='right'>")
print(file_output)

print('</p>')
print('</body></html>')
