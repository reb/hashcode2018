import util

def solve(problem):
    result = []

    r1 = 0
    r2 = problem['minimum_ingredient']-1

    while (r2 < problem['rows']):
        c1 = 0
        c2 = 1
        while (c2 < problem['columns']):
            potential_slice = [r1, c1, r2, c2]
            #print("trying potential slice: {}".format(potential_slice))
            if valid_slice(problem, potential_slice):
                result.append(potential_slice)
                c1 += 2
                c2 += 2
                continue

            c1 +=1 
            c2 +=1

        r1 += problem['minimum_ingredient']
        r2 += problem['minimum_ingredient']


    return result

def valid_slice(problem, slice_rectangle):
    r1 = slice_rectangle[0]
    c1 = slice_rectangle[1]
    r2 = slice_rectangle[2]
    c2 = slice_rectangle[3]


    tomatoes = 0
    mushrooms = 0
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            if problem['pizza'][r][c] == 'T':
                tomatoes += 1
            if problem['pizza'][r][c] == 'M':
                mushrooms += 1

    enough_tomatoes = tomatoes >= problem['minimum_ingredient']
    enough_mushrooms = mushrooms >= problem['minimum_ingredient']
    slice_not_too_big = (tomatoes + mushrooms) <= problem['max_cells']

    #print("found {} tomatoes and {} mushrooms".format(tomatoes, mushrooms))
    #print("enough tomatoes: {}".format(enough_tomatoes))
    #print("enough mushrooms: {}".format(enough_mushrooms))
    #print("slice not too big: {}".format(slice_not_too_big))

    if enough_tomatoes and enough_mushrooms and slice_not_too_big:
        return True

    return False
            

if __name__ == "__main__":
    datasets = ['example', 'small', 'medium', 'big']
    #datasets = ['example']

    for dataset in datasets:
        
        problem = util.load_file(dataset + '.in')
        solution = solve(problem)
        util.export(dataset, solution)

