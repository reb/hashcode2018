import datetime

DEBUG = False



def format_row(row):
#     TODO to implement


def load_file(filename):
    result = {}

    with open(filename) as f:
        print(f)
#       TODO to implement


def export(name, data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = './output/'
    filename = timestamp + '_' + name + '_output.txt'

    with open(output_dir + filename, 'w') as file:
        file.write(str(len(data)) + '\n')
        for row in data:
            file.write(format_row(row))
#       TODO to implement

        print('file was written in directory: ' + output_dir + filename)


if __name__ == "__main__":
    if DEBUG:
        datasets = ['example']
    else:
        datasets = ['example', 'small', 'medium', 'big']

    for dataset in datasets:
        problem = load_file(dataset + '.in')
#       TODO to implement
