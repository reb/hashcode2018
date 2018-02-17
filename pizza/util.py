import datetime

def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        config = lines[0]
        result["rows"] = config[0]
        result["columns"] = config[1]
        result["minimum_ingredient"] = config[2]
        result["max_cells"] = config[3]

        pizza = []
        for line in lines[1:]:
            pizza.append(list(line))

        result["pizza"] = pizza

    return result

def export(data) :
    timetstamp = datetime.datetime.now().strftime("%Y%M%d-%H%M")
    output_dir = './output/'
    filename = timetstamp + '_output_pizza.txt'

    with open(output_dir + filename, 'w') as file:
        file.write(str(len(data)) + '\n')
        for row in data:
            file.write(format(row))

        print 'file was written in directory: ' + output_dir + filename

def format(row) :
    line = ''
    for element in row:
        line += str(element) + ' '
    return line + '\n'