def deep_copy(some_2d_list):
	output = []
	for x in range(len(some_2d_list)): 
		temp = [] 
		for elem in some_2d_list[x]: 
			temp.append(elem) 
			output.append(temp) 
		return output

#def transform(data, num_rows, num_cols):


def gravitate(nums, direction):
	if direction == "left":
		for list in range(len(nums)):
			id = 1
			for value in range(1, len(nums[list]),1):
				nums[list][0] = nums[list][0] + nums[list][id]
				nums[list][id] = 0
				id += 1
		return nums
	if direction == "right":
		for list in range(len(nums)):
			id = 1
			for value in range(1, len(nums[list]),1):
				nums[list][-1] = nums[list][-1] + nums[list][id]
				nums[list][id] = 0
				id -= 1
		return nums

'''def word_search(puzzle, words):
		ans = []
	for word in range(len(puzzle)):
		if '''



