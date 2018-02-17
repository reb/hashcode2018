import datetime

DEBUG = False

def solve(problem):
    slices = []
    overlap_grid  = [[False for c in range(problem['columns'])] for r in range(problem['rows'])]

    r1 = 0
    r2 = problem['minimum_ingredient']-1

    while (r2 < problem['rows']):
        c1 = 0
        c2 = 1
        while (c2 < problem['columns']):
            potential_slice = [r1, c1, r2, c2]
            if DEBUG:
                print("trying potential slice: {}".format(potential_slice)) 
            if valid_slice(problem, overlap_grid, potential_slice):
                slices.append(potential_slice)
                overlap_grid = update_overlap_grid(problem, overlap_grid, potential_slice)
                c1 += 2
                c2 += 2
                continue

            c1 +=1 
            c2 +=1

        r1 += problem['minimum_ingredient']
        r2 += problem['minimum_ingredient']

    c1 = 0
    c2 = problem['minimum_ingredient']-1

    while (c2 < problem['columns']):
        r1 = 0
        r2 = 1
        while (r2 < problem['rows']):
            potential_slice = [r1, c1, r2, c2]
            if DEBUG:
                print("trying potential slice: {}".format(potential_slice))
            if valid_slice(problem, overlap_grid, potential_slice):
                slices.append(potential_slice)
                overlap_grid = update_overlap_grid(problem, overlap_grid, potential_slice)
                r1 += 2
                r2 += 2
                continue

            r1 +=1 
            r2 +=1

        c1 += problem['minimum_ingredient']
        c2 += problem['minimum_ingredient']


    return slices

def valid_slice(problem, overlap_grid, slice_rectangle):
    [r1, c1, r2, c2] = slice_rectangle

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
    
    if DEBUG:
        print("found {} tomatoes and {} mushrooms".format(tomatoes, mushrooms))
        print("enough tomatoes: {}".format(enough_tomatoes))
        print("enough mushrooms: {}".format(enough_mushrooms))
        print("slice not too big: {}".format(slice_not_too_big))

    if enough_tomatoes and enough_mushrooms and slice_not_too_big:
        does_not_overlap = not does_overlap(overlap_grid, slice_rectangle)
        if DEBUG:
            print("does not overlap: {}".format(does_not_overlap))
        if does_not_overlap:
            return True

    return False

def update_overlap_grid(problem, grid, slice):
    [r1, c1, r2, c2] = slice
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            grid[r][c] = True
            if DEBUG:
                print("Filling overlap grid for r: {}, c: {}".format(r, c))

    return grid

def does_overlap(overlap_grid, potential_slice):
    [r1, c1, r2, c2] = potential_slice
    if DEBUG:
        print(overlap_grid)

    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            if overlap_grid[r][c] == True:
                return True

    return False

def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        config = lines[0].split(' ')
        result["rows"] = int(config[0])
        result["columns"] = int(config[1])
        result["minimum_ingredient"] = int(config[2])
        result["max_cells"] = int(config[3])

        pizza = []
        for line in lines[1:]:
            pizza.append(list(line))

        result["pizza"] = pizza

    return result

def export(name, data) :
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = './output/'
    filename = timestamp + '_' + name + '_output_pizza.txt'

    with open(output_dir + filename, 'w') as file:
        file.write(str(len(data)) + '\n')
        for row in data:
            file.write(format(row))

        print('file was written in directory: ' + output_dir + filename)

def format(row) :
    line = ''
    for element in row:
        line += str(element) + ' '
    return line + '\n'

def points(slices) :
    return sum(list(map(lambda slice: len(slice), slices)))

if __name__ == "__main__":
    if DEBUG:
        datasets = ['example']
    else:
        datasets = ['example', 'small', 'medium', 'big']

    for dataset in datasets:
        
        problem = load_file(dataset + '.in')
        solution = solve(problem)
        export(dataset, solution)

