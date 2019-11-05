
def histogram(image):
	new = image[:]
	flatten = []
	checker = []
	counter = 0
	id = 0
	index = 0

	for first in range(len(new)):
		for second in range(len(new[first])):
			flatten.append(new[first][second])
			flatten.sort()
			
	while id != 256:
		if id not in flatten:
			checker.append(0)
			counter = 0
			id += 1
			
		if flatten[index] == id:
			if flatten[index] == flatten[-1]:
				while len(checker) != 256:
					checker.append(1)
					break
					if len(checker) == 256:
						break
				if flatten[index-1] == flatten[index]:
					counter += 1
					checker.append(counter)
				if flatten[index] == flatten[-1]:
					while id < 256:
						checker.append(0)
						id += 1
						if id == 255:
							break
					
				#else:
				#    checker.append(1)
			if flatten[index+1] == id: #put break
				counter += 1
				index += 1
			if flatten[index+1] != id: #put break
				counter += 1
				checker.append(counter)
				counter = 0
				index += 1
				id += 1
	return checker
	

		
		


def rotate(image):
	new = image[:] #pulls slices from here
	del image[0:len(image)] #clears out image to append
	templist=[]  
	for j in range(0,len(new)):
		for i in range(len(new)-1,-1,-1): #pulls out value from end of list
			tlist.append(new[i][j]) #appends it here
		image.append(tlist)
		tlist=[]

#def crop(image, origin, height, width):

'''
def flip(image, orientation):
	templist = []

	if orientation == 'horizontal':

		for i in image:
			store.append(i[::-1])
		image = store
	if orientation == 'vertical':
		image = image[::-1]
	   
	return image

'''
def color2gray(image):
	new = image[:]
			
	for row in new:
		for row2 in row:
			summed = sum(row2)//len(row2)
			del(row2[0:len(row2)])
			row2.append(summed)
	return new
