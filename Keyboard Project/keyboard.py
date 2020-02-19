#####################################################################
# Created by Mostafa Atmar
'''
A program that contains the entire range of piano notes, and can do some useful 
musical calculations, such as generate_durations, which creates the correct beat count
given a base tempo, and generate_frequencies, which can give the frequency from 
a note that differs from the base tempo.

Examples:
generate_durations(60) --> {'Whole': 4.0, 'Half': 2.0, 'Quarter': 1.0, 'Eighth': 0.5, 'Sixteenth': 0.25}

generate_frequencies(440) -> {'A0': 27.5, [...more notes...] 'A4': 440.0, [...more notes...]
                                       'C8': 4186.009044809578}
'''
#####################################################################
def keyboard(): #helper function for outputting keyboard
	scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B','H'] 
	#scale to append notes
	keyboard_list = [] #appends values before putting in dict here
	ranged = ['0', '1', '2', '3', '4', '5', '6', '7', '8'] #determines octave notes
	index_word = 0 #starts incrementing at "C"
	index_num = 1 #starting at index 1, because only three notes are at octave 0

	temp = '' #note and octave number are added here
	while index_word != 'H': #H is placeholder for last index
		if index_num == 8: #stops incrementing octave here
			break
		if scale[index_word] == scale[-1]: #octave  and note change occurs here
			index_num += 1 #increases octave
			index_word = 0 #new octave starts back at "C"
		temp+=scale[index_word] #adds note letter
		temp+=ranged[index_num] #adds octave number
		keyboard_list.append(temp) #appends to list
		temp = "" #empties temp list
		index_word += 1 

	third = "B0"  #manually add these first keys, as they are only used for octave 0
	second = "A#0"
	first = "A0"
	keyboard_list.insert(0,third)
	keyboard_list.insert(0,second)
	keyboard_list.insert(0,first)
	return keyboard_list

def generate_durations(base_tempo):
	tempo = {}  #initialize dict
	
	quarter = 60 / base_tempo #all values derived from quarter note
	half = quarter * 2
	whole = quarter * 4
	eighth = quarter / 2
	sixteenth = quarter / 4
	
	tempo['Whole'] = whole  #appened to dict individually
	tempo['Half'] = half
	tempo['Quarter'] = quarter
	tempo['Eighth'] = eighth
	tempo['Sixteenth'] = sixteenth
	return tempo

def generate_frequencies(base_freq):
	tempo = {} #dict created here
	steps = keyboard().index("A4") #distance from this index is number of half steps
	for val in keyboard(): #frequency math done here
		tempo[val] = base_freq * 2**((keyboard().index(val)-steps)/12) 
	return tempo

def find_note(filename,highest_or_lowest):
	filename1 = open(filename) #reads here
	everything = filename1.read() #pulls whole text
	
	sorter = [] #seperates notes and beat names
	extracted_notes = [] #where the extracted notes will be appended to
	n = [] #notes sorted into here
	readed = everything.split('\n') #splits lines
	for line in readed: 
		values = line.split(",") #by comma to seperate note and beat
		sorter.append(values) 
	
	for thing in sorter:
		if thing[0] in keyboard(): #checks if the note is in keyboard list
			val = thing[0] 
			extracted_notes.append(val) #appends only the note, discards beat
	
	for searcher in keyboard(): #looks through keyboard
		if searcher in extracted_notes: #if keyboard note in extracted notes, 
			n.append(searcher) #appends it as it comes


	if highest_or_lowest == True: 
		return n[-1] #returns end of list for highest
	if highest_or_lowest == False:
		return n[0] #returns beginning of list for lowest

	filename.close()

#def random_song(filename, tempo, tuning, num_measures):

def change_notes(filename,changes,shift):
	filename1 = open(filename) #reads here
	everything = filename1.read() #appends to text block

	cut = filename.split('.') #split name from .song
	file = open(cut[0]+'_changed.song','w') #append name to _changed.song


	sorter = []
	stripped = everything.strip('\n')
	splited = stripped.split('\n')
	for line in splited: #splits text by line
		values = line.split(",") #seperates by comma 
		sorter.append(values)
	bpm = ''
	frequency = ''
	for i in sorter[0][0]: #goes letter by letter in first line
		bpm += i
	for i in sorter[1][0]: #goes letter by letter in second line
		frequency += i
	file.write(bpm +'\n') #writes BPM and frequency
	file.write(frequency +'\n')


	for other in sorter:
		if other[0] not in keyboard(): #removes the frequency and BPM
			other.pop(0)
			continue
		name = keyboard().index(other[0])
		if other[0] in changes: #checks if value in dictionary
			other.insert(0,changes[other[0]]) #puts it in index 0
			other.pop(1) #removes old value
			text='' #takes list and puts it in string
			text+= other[0]+','+other[1]+'\n' #combines note and beat with comma
			file.write(text)
			continue
		if name+shift > keyboard().index(keyboard()[-1]): #if value + shift is over index
			text=''
			text+= other[0]+','+other[1]+'\n' #no change
			file.write(text)
			continue
		if name+shift < keyboard().index(keyboard()[0]): #if value + shift is before index
			text=''
			text+= other[0]+','+other[1]+'\n'
			file.write(text)
			continue
		other.insert(0,keyboard()[name + shift]) #shift applied here
		other.pop(1) #remove old value
		text=''
		text+= other[0]+','+other[1]+'\n' #appended and written
		file.write(text)

	file.close()
	filename1.close()


def song_as_dict(filename):
	filename1 = open(filename) #reads here
	everything = filename1.read() #pulls whole text
	final = {} #main dictionary
	dir_notes = {} #dir for notes
	dir_types = {} #dir for notes
	sorter = [] #holder list
	
	stripped = everything.strip('\n')
	splited = stripped.split('\n')
	for line in splited: #splits text by line
		values = line.split(",") #seperates by comma 
		sorter.append(values)

	final['tempo'] = int(sorter[0][0])
	final['tuning'] = float(sorter[1][0])
	final['notes'] = dir_notes
	final['types'] = dir_types

	copy = sorter[:]
	line1 = copy[0][0]
	line2 = copy[1][0]

	for other in sorter:
		if other[0] == line1: #avoids re-reading tempo
			other.pop(0)
			continue
		if other[0] == line2: #avoids re-reading tuning
	   		other.pop(0)
		for i in other: 
			if i == other[0]: #if i is the note, like [A4],Quarter
				text = '' #made a string to slice through
				for k in i:    
					text+=k #append to text
					if text == other[0]: #once the built up text equals the note name
						if text[:-1] in dir_notes: #checks if it exists
							if int(text[-1]) in dir_notes[text[:-1]]: #if yes, check octave number
								integer = int(text[-1]) #shorthand conversion              
								for x in dir_notes[text[:-1]]: #check keys until it matches note
									if integer == x:
										final["notes"][text[:-1]][integer] +=1 #increment value in entry
							else:
								octave = {} #if note exists, but not octave number, make new dict
								dir_notes[text[:-1]][int(text[-1])] = octave[int(text[-1])] = 1 
								#in that space, add the octave number and equal to 1
								
						if text[:-1] not in dir_notes:
							octave = {}
							dir_notes[text[:-1]] = octave
							if text[-1] not in octave:
								octave[int(text[-1])] = 1
			if i == other[1]: #if i is the type, like A4,[Quarter]
				if i in dir_types: #if in dir, adds 1 to values
					dir_types[i] += 1
				if i not in dir_types: #if not in dir, creates new entry
					dir_types[i] = 1
	return final

	filename1.close()