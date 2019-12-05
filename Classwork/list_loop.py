a = [1,2,3,4,5,6]

answer = int(input('give input:\n'))
while answer != 'stop':
	while answer in a:
		a.remove(answer)
	while answer not in a:
		a.append(answer)
	print(a)
	answer = int(input('give another:\n'))
