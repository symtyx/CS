def sum_list(xs):
    sum = 0
    for val in xs:
        if type(val) == int:
            sum += val
        else:
            sum += sum_list(val)
    return sum