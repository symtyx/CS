#Partners: Mohammed Zafir Rahman

def fill(grid, old_value, new_value, seed):
    points = []
    points.append(seed[0])
    points.append(seed[1])
    
    seed_x = seed[0]
    seed_y = seed[1]
    
    if grid[points[0]][points[1]] == old_value:
        grid[points[0]][points[1]] = new_value
        fill(grid, old_value, new_value, (points[0]+1,points[1]))
        fill(grid, old_value, new_value, (points[0]-1,points[1]))
        fill(grid, old_value, new_value, (points[0],points[1]+1))
        fill(grid, old_value, new_value, (points[0],points[1]-1))

       
def descendants(family_tree, name, distance):
    names = []
    final = []
    if name in family_tree:
        True
    else:
        return names
        
    while type(distance) == int:
        if distance > 1:
            for first in family_tree[name]:
                names.append(descendants(family_tree, first, distance-1))
        elif distance == 1 or distance < 1:
            return family_tree[name]
        break
    for first in names:
        for second in first:
            final.append(second)
    return final

