def zigzag(text):
	zig = ""
	for i in range(len(text)):
		if len(text) == len(zig):
			continue
		else:
			zig += text[i]
			if len(text) == len(zig):
				break
			else:
				zig += text[len(text) - (i+1)]
	return zig

def sum_gt_avg(num_list):
	greater_avg = 0
	for i in range(len(num_list)):
		avg_num = sum(num_list)/len(num_list)
		if num_list[i] > avg_num:
			greater_avg += num_list[i]
	return greater_avg