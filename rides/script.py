import datetime

DEBUG = False


def solve(problem):
    result = []

    rides = problem["rides"].copy()

    start = {
        "number": "start",
        "start": create_location(0, 0),
        "finish": create_location(0, 0),
        "start_after": 0}

    while len(result) < problem["vehicles"]:
        closest_to_start = connected_rides(start, rides)[0]
        rides.remove(closest_to_start)
        plan = [closest_to_start]
        if valid_ride_plan(problem, plan):
            result.append({
                "plan": [closest_to_start],
                "value": ride_distance(closest_to_start)})

    not_changed = False
    while(True):
        if not_changed:
            break
        not_changed = True

        for vehicle in result:
            if not rides:
                break
            [last_ride] = vehicle["plan"][-1:]
            best_connection = connected_rides(last_ride, rides)[0]

            if valid_ride_plan(problem, vehicle["plan"] + [best_connection]):
                if DEBUG:
                    print("Valid connection, adding to ride")
                rides.remove(best_connection)
                vehicle["plan"].append(best_connection)
                vehicle["value"] += ride_distance(best_connection)
                not_changed = False

    print("Missed {} rides".format(len(rides)))
    return result


def valid_ride_plan(problem, ride_plan):
    location = create_location(0, 0)
    step = 0

    if DEBUG:
        print("Simulating ride_plan: {}".format(format_ride_plan(ride_plan)))
    for ride in ride_plan:

        if DEBUG:
            print("Starting ride {} at step {}".format(ride["number"], step))

        step += distance(ride["start"], location)
        if step < ride["start_after"]:
            step = ride["start_after"]
        step += ride_distance(ride)

        location = ride["finish"]

        if DEBUG:
            print("Ending ride {} at step {}".format(ride["number"], step))

        if step > ride["finish_before"]:
            if DEBUG:
                print("Failed to finish")
            return False

    return True


def connected_rides(start_ride, rides):
    arrival = start_ride["start_after"] + ride_distance(start_ride)
    result = []

    if DEBUG:
        print("Looking for a connection from {}".format(start_ride["number"]))

    for ride in rides:
        empty_time = distance(start_ride["finish"], ride["start"])

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
            ride["start"] = create_location(int(a), int(b))
            ride["finish"] = create_location(int(x), int(y))
            ride["start_after"] = int(s)
            ride["finish_before"] = int(f)
            rides.append(ride)

        result["rides"] = rides

    return result


def create_location(row, column):
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
