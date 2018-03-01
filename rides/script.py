import datetime

DEBUG = True


def solve(problem):
    result = []
    rides = iter(problem["rides"])
    for nr_vehicle in range(problem["vehicles"]):
        vehicle = {"current_position": {"x": 0, "y": 0}, "rides": []}
        for (idx, ride) in enumerate(rides):
            distance_to_start = start_distance(ride, vehicle)
            if distance_to_start > ride["start_after"] + 1:
                next(rides)
                continue
            else:
                vehicle["current_position"] = assign_new_position_vehicle(ride)
                vehicle["rides"].append(idx)
        result.append(vehicle["rides"])

    return result


def assign_new_position_vehicle(ride):
    return {"x": ride["finish_row"], "y": ride["finish_column"]}


def start_distance(ride, vehicle):
    return ride_distance(vehicle["current_position"]["x"],
                         vehicle["current_position"]["y"],
                         ride["start_column"],
                         ride["start_row"])


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
