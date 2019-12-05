def how_odd(n):
	counter = []
	if n % 2 == 0:
		counter = n % 2
		return counter
	else:
		while n % 2 != 0:
			n // 2
			counter += 1
		return counter
