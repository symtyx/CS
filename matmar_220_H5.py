
def extract_min(xs):
	min_val = min(xs)
	for num in xs:
		if num == min_val:
			xs.remove(num)
			return num
			break
def insert_ordered(xs,v):
	id = 0
	if len(xs) == 0:
		xs.append(v)
	while id < len(xs):
		if xs[id] < v:
			id += 1
		else:
			xs.insert(id,v)
			break
	while xs[-1] < v:
		xs.insert(-1,v)
		break

def max_few(a, b=None, c=None):
	if a != None and b != None and c != None:
		if a >= b and a >= c:
			return a	
		if b >= c:		
			return b	
		return c
	if a != None and b != None:
		if a >= b:
			return a
		return b
	if a != None and c != None:
		if a >= c:
			return a
		return c
	if b != None and c != None:
		if b >= c:
			return b
		return c
	return a