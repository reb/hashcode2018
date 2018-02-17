import datetime

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


if __name__ == '__main__':
    test = [[0, 0, 2, 1], [0, 0, 5, 6]]
    export(test)