import datetime

DEBUG = True

def format_row(row):
    #     TODO to implement
    pass


def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        [rows, columns, vehicles, rides, bonus, steps] = lines[0].split(' ')

        result["rows"] = int(rows)
        result["columns"] = int(columns)
        result["vehicles"] = int(vehicles)
        result["rides"] = int(rides)
        result["bonus"] = int(bonus)
        result["steps"] = int(steps)

        rides = []
        for line in lines[1:]:
            [start_row, start_column, finish_row, finish_column, start_after, finish_before] = line.split(' ')

            ride = {}
            ride["start_row"] = int(start_row)
            ride["start_column"] = int(start_column)
            ride["finish_row"] = int(finish_row)
            ride["finish_column"] = int(finish_column)
            ride["start_after"] = int(start_after)
            ride["finish_before"] = int(finish_before)
            rides.append(ride)

        result["rides"] = rides

    return result

def export(name, data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = './output/'
    filename = timestamp + '_' + name + '.txt'

    with open(output_dir + filename, 'w') as file:
        file.write(str(len(data)) + '\n')
        for row in data:
            file.write(format_row(row))
        # TODO to implement

        print('file was written in directory: ' + output_dir + filename)


if __name__ == "__main__":
    if DEBUG:
        datasets = ['a_example']
    else:
        datasets = ['example', 'small', 'medium', 'big']

    for dataset in datasets:
        problem = load_file(dataset + '.in')
        print(problem)
