import datetime

def solve(problem):
    slices = []

    r1 = 0
    r2 = problem['minimum_ingredient']-1

    while (r2 < problem['rows']):
        c1 = 0
        c2 = 1
        while (c2 < problem['columns']):
            potential_slice = [r1, c1, r2, c2]
            #print("trying potential slice: {}".format(potential_slice))
            if valid_slice(problem, slices, potential_slice):
                result.append(potential_slice)
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
            #print("trying potential slice: {}".format(potential_slice))
            if valid_slice(problem, slices, potential_slice):
                result.append(potential_slice)
                r1 += 2
                r2 += 2
                continue

            r1 +=1 
            r2 +=1

        c1 += problem['minimum_ingredient']
        c2 += problem['minimum_ingredient']


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
    does_not_overlap = !does_overlap(slices, slice_rectangle)

    #print("found {} tomatoes and {} mushrooms".format(tomatoes, mushrooms))
    #print("enough tomatoes: {}".format(enough_tomatoes))
    #print("enough mushrooms: {}".format(enough_mushrooms))
    #print("slice not too big: {}".format(slice_not_too_big))

    if enough_tomatoes and enough_mushrooms and slice_not_too_big and does_not_overlap:
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
    datasets = ['example', 'small', 'medium', 'big']
    #datasets = ['example']

    for dataset in datasets:
        
        problem = load_file(dataset + '.in')
        solution = solve(problem)
        export(dataset, solution)

