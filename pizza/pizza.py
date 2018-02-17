import util

def solve(problem):
    return [[0,1,2,3], [1,2,3,4]]




def valid_slice(problem, slice_rectangle):
    r1 = slice_rectangle[0]
    c1 = slice_rectangle[1]
    r2 = slice_rectangle[2]
    c2 = slice_rectangle[3]

    tomatoes = 0
    mushrooms = 0
    for r in range(r1, r2):
        for c in range(c1, c2):
            if problem['pizza'][r][c] == 'T':
                tomatoes += 1
            if problem['pizza'][r][c] == 'M':
                mushrooms += 1

    enough_tomatoes = tomatoes >= problem['minimum_ingredient']
    enough_mushrooms = mushrooms >= problem['minimum_ingredient']
    slice_not_too_big = (tomatoes + mushrooms) <= problem['max_cells']

    if enough_tomatoes and enough_mushrooms and slice_not_too_big:
        return True

    return False
            

if __name__ == "__main__":
    datasets = ['example', 'small', 'medium', 'big']

    for dataset in datasets:
        
        problem = util.load_file(dataset + '.in')
        solution = solve(problem)
        util.export(dataset, solution)

