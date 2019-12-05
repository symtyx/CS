for i in range(10):
	for j in range(10):
		if j==5:
			break
		print(i,j, sep='')

a = [4,9,-8,-87,32,5]

max_value(a)
for i in range(len(a)):
	v = max_value(a[i:])
	a[0] = v
	swap(a[i],v)