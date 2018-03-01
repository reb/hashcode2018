import datetime

DEBUG = False


def solve(problem):
    return [[0]]


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
            [start_row, start_column, finish_row, finish_column,
             start_after, finish_before] = line.split(' ')

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
        for vehicle, rides in enumerate(data):
            file.write(str(vehicle) + " ".join(str(ride) for ride in rides))

        print('file was written in directory: ' + output_dir + filename)


if __name__ == "__main__":
    if DEBUG:
        datasets = ['a_example']
    else:
        datasets = ['a_example', 'b_should_be_easy', 'c_no_hurry',
                    'd_metropolis', 'e_high_bonus']

    for dataset in datasets:
        problem = load_file(dataset + '.in')
        solution = solve(problem)
        export(dataset, solution)
