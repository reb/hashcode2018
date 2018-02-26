import datetime

DEBUG = False


def solve(problem):
    return [[0, 0, 1, 1]]


def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        [rows, columns, minimum_ingredients, max_cells] = lines[0].split(' ')

        result["rows"] = int(rows)
        result["columns"] = int(columns)
        result["minimum_ingredient"] = int(minimum_ingredients)
        result["max_cells"] = int(max_cells)

        pizza = []
        for line in lines[1:]:
            pizza.append(list(line))

        result["pizza"] = pizza

    return result


def export(name, data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = './output/'
    filename = timestamp + '_' + name + '.txt'

    with open(output_dir + filename, 'w') as file:
        file.write(str(len(data)) + '\n')
        for row in data:
            file.write(format(row))

        print('file was written in directory: ' + output_dir + filename)


def format(row):
    line = ''
    for element in row:
        line += str(element) + ' '
    return line + '\n'


if __name__ == "__main__":
    if DEBUG:
        datasets = ['example']
    else:
        datasets = ['example', 'small', 'medium', 'big']

    for dataset in datasets:

        problem = load_file(dataset + '.in')
        solution = solve(problem)
        export(dataset, solution)
