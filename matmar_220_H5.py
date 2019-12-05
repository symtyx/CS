
def extract_min(xs):
	min_val = min(xs)
	for num in xs:
		if num == min_val:
			xs.remove(num)
			return num
			break
def insert_ordered(xs,v):
	id = 0
	if len(xs) != 0:  
		while id < len(xs):
			if xs[id] < v:
				id += 1
			else:
				xs.insert(id,v)
				break
		while xs[-1] < v:
			xs.append(v)
			break
	if len(xs) == 0:
		xs.append(v)

def pop_sorted(xs):
	answer = []
	sample = xs[:]
	while len(sample) != 0:
		extract = extract_min(sample)
		answer.append(extract)
	return answer

def pop_sort(xs):
	sample = xs[:]
	xs.clear()
	while len(sample) != 0:
		extract = extract_min(sample)
		xs.append(extract)
	
def inc_all(grid, amount=1):
	for i in (range(len(grid))):
		for j in (range(len(grid[i]))):
			grid[i][j] += amount
		

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

def remove_many(xs, v, limit=None):
    sample = xs[:]
    if limit == None:
        for val in xs:
            if v in xs:
                xs.remove(xs[val])
        
def oddify(xs, evens=[]):
	sample = xs[:]
	for i in sample:
		if i % 2 == 0:
			evens.append(i)
			xs.remove(i)
	return evens

def my_range(start, stop=None, step=1):
	empty = []
	i = start
	
	if stop == None:
		i = 0
		while i < start:
			empty.append(i)
			i += 1
		return empty

	if stop != None:
		if stop == step:
			return empty
		elif start < stop:
			empty.append(start)
			i += step
			while i < stop:
				empty.append(i)
				i += step
			return empty
		elif start > stop:
			empty.append(start)
			i += step
			while i > stop:
				empty.append(i)
				i += step
			return empty


	



