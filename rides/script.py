from datetime import datetime
from copy import deepcopy
from sys import stdout

DEBUG = False
LOOKAHEAD = False


def solve(problem):
    vehicles = []

    assigned = 0

    rides = problem["rides"].copy()

    vehicle = new_vehicle()
    add_connections(problem, vehicle, rides)

    vehicles.append(vehicle)

    while(True):
        if not rides:
            break

        try:
            vehicle = best_vehicle(vehicles)
        except ValueError:
            break

        best_connection = vehicle["connections"].pop(0)["ride"]

        starting_vehicle = not vehicle["plan"]
        fleet_not_full = len(vehicles) < problem["vehicles"]
        if starting_vehicle and fleet_not_full:
            vehicles.append(deepcopy(vehicle))

        if DEBUG:
            print("Found {} as best".format(best_connection["number"]))

        add_ride(problem, vehicle, best_connection)

        assigned += 1
        message = "Rides assigned: {}/{}\r"
        stdout.write(message.format(assigned, problem["ride_amount"]))
        stdout.flush()

        if DEBUG:
            print("Added ride {} to vehicle".format(best_connection["number"]))
        rides.remove(best_connection)

        connections = connected_rides(problem, vehicle, rides)
        vehicle["connections"] = connections
        remove_from_connections(best_connection, vehicles, rides)

        if connections:
            add_lookahead(problem, vehicle, rides)

    # pad the vehicles if there are not enough
    while len(vehicles) < problem["vehicles"]:
        vehicles.append(new_vehicle())

    return vehicles


def remove_from_connections(ride, vehicles, rides):
    for vehicle in vehicles:
        index = None
        for i, entry in enumerate(vehicle["connections"]):
            if entry["ride"] == ride:
                index = i
                break

        if index is not None:
            vehicle["connections"].pop(index)

        if not LOOKAHEAD:
            continue

        if index == 0 and vehicle["connections"]:
            add_lookahead(problem, vehicle, rides)

        index = None
        for i, entry in enumerate(vehicle["lookahead"]):
            if entry["ride"] == ride:
                index = i
                break

        if index is not None:
            vehicle["lookahead"].pop(index)

        if not vehicle["lookahead"]:
            add_lookahead(problem, vehicle, rides)


def add_connections(problem, vehicle, rides):
    if DEBUG:
        print("Adding connections")
    if "lookahead" in vehicle:
        if vehicle["lookahead"][0]["ride"]:
            vehicle["connections"] = vehicle["lookahead"]
        else:
            vehicle["connections"] = []
    else:
        vehicle["connections"] = connected_rides(problem, vehicle, rides)

    add_lookahead(problem, vehicle, rides)


def add_lookahead(problem, vehicle, rides):
    if not LOOKAHEAD:
        return
    if not vehicle["connections"]:
        return
    if DEBUG:
        print("Adding lookahead")

    # add the first ride from connections to a new vehicle
    best_vehicle = new_vehicle()
    best_vehicle["step"] = vehicle["step"]
    best_vehicle["location"] = vehicle["location"]
    connection = vehicle["connections"][0]
    add_ride(problem, best_vehicle, connection["ride"])

    lookahead = connected_rides(problem, best_vehicle, rides)
    if not lookahead:
        # if there are no further connections from the best connection
        # add a penalty for the rest of the remaining time in the simulation
        waiting_time = problem["steps"] - best_vehicle["step"]
        utility = waiting_time
        lookahead = [{
            "ride": False,
            "utility": utility
        }]
        if DEBUG:
            message = "No lookahead from {}, adding {} as a final utility"
            print(message.format(connection["ride"]["number"], utility))

    vehicle["lookahead"] = lookahead


def connection_and_lookahead(vehicle):
    connection = vehicle["connections"][0]
    lookahead = vehicle["lookahead"][0]

    return connection["utility"] + lookahead["utility"]


def best_vehicle(vehicles):
    connectable = (vehicle for vehicle in vehicles if vehicle["connections"])
    if not LOOKAHEAD:
        return min(connectable, key=lambda v: v["connections"][0]["utility"])
    return min(connectable, key=connection_and_lookahead)


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
        print("Starting ride {} at step {}".format(ride["number"], step))

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

    # update vehicle
    vehicle["step"] = step
    vehicle["plan"] += [ride]
    vehicle["location"] = ride["finish"]
    vehicle["value"] += ride_value


def connected_rides(problem, vehicle, rides):
    result = []

    if DEBUG:
        print("Looking for a connection from {}".format(vehicle["location"]))

    for ride in rides:
        distance_to_start = distance(vehicle["location"], ride["start"])
        utility = distance_to_start  # penalty for moving to start
        arrival = vehicle["step"] + distance_to_start

        if arrival < ride["start_after"]:
            waiting_time = ride["start_after"] - arrival
            utility += waiting_time  # penalty for waiting
            utility -= problem["bonus"] * 1000  # bonus for bonus

        ride_length = ride_distance(ride)
        finish = arrival + ride_length
        utility -= (ride_length / 10)  # bonus for longer rides

        if finish > ride["finish_before"]:
            if DEBUG:
                print("Not adding {}, won't finish".format(ride["number"]))
            continue

        result.append({
            "utility": utility,
            "ride": ride})

    result.sort(key=lambda entry: entry["utility"])

    if DEBUG:
        message = "Found a connection with {} (utility: {})"
        for entry in result:
            number = entry["ride"]["number"]
            utility = entry["utility"]
            print(message.format(number, utility))

    return result


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
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
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
    assigned = 0
    for vehicle in solution:
        total_value += vehicle["value"]
        assigned += len(vehicle["plan"])
    print("Rides assigned: {}/{}".format(assigned, problem["ride_amount"]))
    print("Total expected value: {}".format(total_value))
    return total_value


if __name__ == "__main__":
    if DEBUG:
        datasets = ['a_example']
    else:
        datasets = ['a_example', 'b_should_be_easy', 'c_no_hurry',
                    'd_metropolis', 'e_high_bonus']

    total = 0
    for dataset in datasets:
        print("=={}==".format(dataset))
        problem = load_file(dataset + '.in')
        solution = solve(problem)
        if DEBUG:
            print(solution)
        total += stats(problem, solution)
        export(dataset, solution)
        print()  # new line
    print("Total expected value of this solution: {}".format(total))
