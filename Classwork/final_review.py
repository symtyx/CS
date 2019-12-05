def index_2d(matrix, val):
    for i in range(len(matrix)):
        for j in range(len(i)):
            if matrix[i][j] == val:
                coordinate = (i,j)
                return coordinate

def flattened_odds(xs):
    flat = []
    for i in range(len(xs)):
        for j in range(len(xs[i])):
            if xs[i][j] % 2 == 1:
                flat.append(xs[i][j])
    print(flat)
    return flat

def sum3d(xs):
    sum = 0
    for row in xss:
        for col in row:
            for something in col:
                sum += something
    return sum

def min2d(xs):
    min = xs[0][0]
    for row in xs:
        for col in row:
            if col < min:
                min = col
    return min