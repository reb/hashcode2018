

def calc_rides(rides):
    vehicles = []
    vehicle = {"current_position": {"x": 0, "y": 0}, "rides": 0}
    for ride in rides:
        distance = abs(vehicle["current_position"]["x"] - ride["start_row"]) + vehicle["current_position"]["y"] - ride["start_column"]
        if ride["start_after"] < distance:
            # rides.next()
            continue
        else:
            vehicle["current_position"] = {"x": ride["finish_row"], "y": ride["finish_column"]}
            vehicle["rides"] += 1
            # assign ride to vehicle
    vehicles.append([1, vehicle["rides"]])
    return vehicles
