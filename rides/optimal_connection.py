import datetime

DEBUG = False


def solve(problem):
    result = []

    rides = problem["rides"]
    while(True):
        if len(rides) < 2:
            break

        ride = rides.pop(0)
        best_connection = closest_connected_ride(ride, rides)
        rides.remove(best_connection)
        result.append([ride["number"], best_connection["number"]])

        if DEBUG:
            message = "Found that {} connects best to {}"
            print(message.format(best_connection["number"], ride["number"]))

    if len(rides) == 1:
        result.append([rides[0]["number"]])

    return result


def closest_connected_ride(ride_to_check, rides):
    r1 = ride_to_check["finish_row"]
    c1 = ride_to_check["finish_column"]

    minimum_ride = {}
    minimum_distance = -1
    for ride in rides:
        r2 = ride["start_row"]
        c2 = ride["finish_column"]
        distance = ride_distance(r1, c1, r2, c2)

        if minimum_distance > distance or minimum_distance == -1:
            minimum_distance = distance
            minimum_ride = ride

    return minimum_ride


def ride_distance(start_row, start_column, finish_row, finish_column):
    return abs(start_row - finish_row) + abs(start_column - finish_column)


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
        for ride_number, line in enumerate(lines[1:]):
            [start_row, start_column, finish_row, finish_column,
             start_after, finish_before] = line.split(' ')

            ride = {}
            ride["number"] = ride_number
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
        for rides in data:
            formatted_rides = " ".join(str(ride) for ride in rides)
            line = "{} {}\n".format(str(len(rides)), formatted_rides)
            file.write(line)

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
        if DEBUG:
            print(solution)
        export(dataset, solution)
