x = [1,2,2,2,3,-9,-7,908]

for i in range(len(x)):
    for j in range(len(x)-1,i,-1):
        if x[i] == x[j]:
            del x[j]

#without for
index = 0
while True:
	if x[index] in x[index+1:]:
		del x[index]
	else:
		if (index+1)  >= len(x):
			break
		index += 1

#for an item
index = 0
while True:
	if x[index]:
		#found = False -to find something
		for item in x[index+1:]:
			if item == x[index]:
				del x[index]
				#found = True
				break
	#if found:
		#del x[index]
	else:
		if (index+1)  >= len(x):
			break
		index += 1