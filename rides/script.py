import datetime

DEBUG = False


def solve(problem):
    vehicles = []

    rides = problem["rides"].copy()

    starting_rides = connected_rides(problem, new_vehicle(), rides)

    while len(vehicles) < problem["vehicles"]:
        closest_to_start = starting_rides.pop(0)
        rides.remove(closest_to_start)
        vehicle = new_vehicle()
        if add_ride(problem, vehicle, closest_to_start):
            vehicles.append(vehicle)

    not_changed = False
    while(True):
        if not_changed:
            break
        not_changed = True

        for vehicle in vehicles:
            if not rides:
                break
            best_connection = connected_rides(problem, vehicle, rides)[0]

            if add_ride(problem, vehicle, best_connection):
                if DEBUG:
                    print("Valid connection, adding to ride")
                rides.remove(best_connection)
                not_changed = False

    return vehicles


def new_vehicle():
    return {
        "location": new_location(0, 0),
        "step": -1,
        "value": 0,
        "plan": []
    }


def add_ride(problem, vehicle, ride):
    step = vehicle["step"]
    location = vehicle["location"]
    ride_value = 0

    if DEBUG:
        print("Adding ride {} at step {}".format(ride["number"], step))

    step += distance(ride["start"], location)
    if step < ride["start_after"]:
        step = ride["start_after"]
        # bonus gotten
        ride_value += problem["bonus"]

    ride_length = ride_distance(ride)
    ride_value += ride_length
    step += ride_length

    if DEBUG:
        print("Ending ride {} at step {}".format(ride["number"], step))

    if step > ride["finish_before"]:
        if DEBUG:
            print("Failed to finish")
        return False

    # update vehicle
    vehicle["step"] = step
    vehicle["plan"] += [ride]
    vehicle["location"] = ride["finish"]
    vehicle["value"] += ride_value

    return True


def connected_rides(problem, vehicle, rides):
    result = []

    if DEBUG:
        print("Looking for a connection from {}".format(vehicle["location"]))

    for ride in rides:
        distance_to_start = distance(vehicle["location"], ride["start"])
        empty_time = distance_to_start
        arrival = vehicle["step"] + distance_to_start

        if arrival < ride["start_after"]:
            waiting_time = ride["start_after"] - arrival
            empty_time += waiting_time
            empty_time -= problem["bonus"]

        result.append({
            "empty_time": empty_time,
            "ride": ride})

    result.sort(key=lambda entry: entry["empty_time"])

    if DEBUG:
        message = "Found a connection with {} (empty time: {})"
        for entry in result:
            number = entry["ride"]["number"]
            empty_time = entry["empty_time"]
            print(message.format(number, empty_time))

    return [entry["ride"] for entry in result]


def ride_distance(ride):
    return distance(ride["start"], ride["finish"])


def distance(start, finish):
    row_difference = abs(start["row"] - finish["row"])
    column_difference = abs(start["column"] - finish["column"])
    return row_difference + column_difference


def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        [R, C, F, N, B, T] = lines[0].split(' ')

        result["rows"] = int(R)
        result["columns"] = int(C)
        result["vehicles"] = int(F)
        result["ride_amount"] = int(N)
        result["bonus"] = int(B)
        result["steps"] = int(T)

        rides = []
        for ride_number, line in enumerate(lines[1:]):
            [a, b, x, y, s, f] = line.split(' ')

            ride = {}
            ride["number"] = ride_number
            ride["start"] = new_location(int(a), int(b))
            ride["finish"] = new_location(int(x), int(y))
            ride["start_after"] = int(s)
            ride["finish_before"] = int(f)
            rides.append(ride)

        result["rides"] = rides

    return result


def new_location(row, column):
    return {"row": row, "column": column}


def export(name, data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = './output/'
    filename = timestamp + '_' + name + '.txt'

    with open(output_dir + filename, 'w') as file:
        for vehicle in data:
            plan = vehicle["plan"]
            line = "{} {}\n".format(str(len(plan)), format_ride_plan(plan))
            file.write(line)

        print('file was written in directory: ' + output_dir + filename)


def format_ride_plan(ride_plan):
    return " ".join(str(ride["number"]) for ride in ride_plan)


def stats(problem, solution):
    total_value = 0
    rides_taken = 0
    for vehicle in solution:
        total_value += vehicle["value"]
        rides_taken += len(vehicle["plan"])
    print("Total expected value: {}".format(total_value))
    print("Rides taken: {}/{}".format(rides_taken, problem["ride_amount"]))


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
        stats(problem, solution)
        export(dataset, solution)
