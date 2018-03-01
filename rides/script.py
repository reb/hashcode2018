import datetime

DEBUG = False


def solve(problem):
    result = []

    rides = problem["rides"].copy()

    start = {
        "number": "start",
        "start": {
            "row": 0,
            "column": 0},
        "finish": {
            "row": 0,
            "column": 0},
        "start_after": 0}

    for _ in range(problem["vehicles"]):
        closest_to_start = closest_connected_ride(start, rides)
        rides.remove(closest_to_start)
        result.append({
            "plan": [closest_to_start],
            "value": ride_distance(closest_to_start)})

    not_changed = False
    while(True):
        if not_changed:
            break
        not_changed = True

        for vehicle in result:
            if len(rides) == 0:
                break
            [last_ride] = vehicle["plan"][-1:]
            best_connection = closest_connected_ride(last_ride, rides)

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
    location = {"row": 0, "column": 0}
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


def closest_connected_ride(ride_to_check, rides):
    arrival = ride_to_check["start_after"] + ride_distance(ride_to_check)
    closest_ride = {}
    minimum = 999999999999

    for ride in rides:
        empty_time = distance(ride_to_check["finish"], ride["start"])

        if arrival < ride["start_after"]:
            waiting_time = ride["start_after"] - arrival
            empty_time += waiting_time
            empty_time -= problem["bonus"]

        if DEBUG:
            message = "Found an empty time of {} for ride {}"
            print(message.format(empty_time, ride["number"]))

        if minimum > empty_time:
            minimum = empty_time
            closest_ride = ride

    if DEBUG:
        msg = "Found that {} connects best to {}"
        print(msg.format(closest_ride["number"], ride_to_check["number"]))

    return closest_ride


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
            ride["start"] = {}
            ride["start"]["row"] = int(start_row)
            ride["start"]["column"] = int(start_column)
            ride["finish"] = {}
            ride["finish"]["row"] = int(finish_row)
            ride["finish"]["column"] = int(finish_column)
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
        for vehicle in data:
            plan = vehicle["plan"]
            line = "{} {}\n".format(str(len(plan)), format_ride_plan(plan))
            file.write(line)

        print('file was written in directory: ' + output_dir + filename)


def format_ride_plan(ride_plan):
    return " ".join(str(ride["number"]) for ride in ride_plan)


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
