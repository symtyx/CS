
def histogram(image): #excuse the mess
	flatten = []
	checker = []
	counter = 0
	id = 0 # this variable keeps track of count of numbers 0-255
	index = 0

	#break image values here
	for first in range(len(image)):   #takes the values that need to be counted
		for second in range(len(image[first])):
			flatten.append(image[first][second])
	flatten.sort()  #sorts values that need to be counted
	

	#fills gap before first value in image with zero
	while id != 255: #counts to 255
		if id not in flatten: #if that value doesnt exist in image, it becomes zero
			checker.append(0)
			counter = 0
			id += 1 #moves to next number	

		if flatten[index] == id: #if a number in image is found
			if flatten[index] == flatten[-1]: #checks for last number in image
				while len(checker) != 255:
					checker.append(1) #manually appended
					break
					if len(checker) == 255: #stops here if this is index 255
						break
				if flatten[index] == flatten[-1]:
					while id < 256:
						checker.append(0) #after the last number in image is found
						id += 1  #i fill the rest of the list with 0, because no more values to check
						if id == 255:
							return checker #returns here if the 255th number is not a value
							break
					
					
			#counter section for values					
			if id != 255:   
				if flatten[index+1] == id: #checks consecutive values, counts them
					counter += 1 
					index += 1 #no id increment because checks for same number
			if id != 255:
				if flatten[index+1] != id: #after all consecutive values found for that id,
					counter += 1
					checker.append(counter) #that number is appended for that id
					counter = 0
					index += 1
					id += 1  #moves on after finding value
					if id == 255:
						return checker #second break
	
def flip(image, orientation):
    if orientation ==  'horizontal': #checks orientation
        for i in range(len(image)):
            image[i] = image[i][::-1] #changes index to reverse slice
    
		


def rotate(image):
	new = image[:] #pulls slices from here
	del image[0:len(image)] #clears out image to append
	templist=[]  
	for j in range(0,len(new)):
		for i in range(len(new)-1,-1,-1): #pulls out value from end of list
			templist.append(new[i][j]) #appends it here
		image.append(templist)
		templist=[]

#def crop(image, origin, height, width):

def color2gray(image):
	final = []  #appends all average values
	for values in image:  #checks for each row
		new = []
		for x in values:   #in each list...
			new.append(sum(x)//len(x)) #calculates average
		final.append(new) #appends that list into here
	return final  


def extract_layer(image, color):
	final = []		#sub-lists appended here
	for values in image: #for each row...
		new = [] #sublist for values
		for x in values: #in each list
			if color == 'red':  #color indexing done here, pulls number out
				new.append(x[0])      
			if color == 'green':
				new.append(x[1])
			if color == 'blue':
				new.append(x[2])
		final.append(new) 
	return final


