extern crate chrono;
extern crate rayon;

use std::fs::File;
use std::io::prelude::*;
use std::io;
use chrono::Local;
use rayon::prelude::*;

const DEBUG: bool = false;

#[derive(Debug)]
struct Problem {
    rows: i32,
    columns: i32,
    vehicles: i32,
    ride_amount: i32,
    bonus: i32,
    steps: i32,
    rides: Vec<Ride>
}

#[derive(Debug)]
struct Ride {
    start: Location,
    finish: Location,
    start_after: i32,
    finish_before: i32
}

#[derive(Debug, Clone)]
struct Location {
    row: i32,
    column: i32
}

#[derive(Debug, Clone)]
struct Vehicle {
    plan: Vec<usize>,
    step: i32,
    location: Location,
    value: i32,
    connections: Vec<Connection>
}

impl Vehicle {
    fn add_ride(&mut self, problem: &Problem, ride_number: usize) {
        let ride = get_ride(problem, ride_number);

        let mut step = self.step;
        let mut ride_value = 0;

        if DEBUG {
            println!("Starting ride {} at step {}", ride_number, step);
        }

        step += distance(&ride.start, &self.location);
        if step < ride.start_after {
            step = ride.start_after;
            // bonus gotten
            ride_value += problem.bonus;
        }

        let ride_length = ride_distance(&ride);
        ride_value += ride_length;
        step += ride_length;

        if DEBUG {
            println!("Ending ride {} at step {}", ride_number, step);
        }

        self.step = step;
        self.plan.push(ride_number);
        copy_location(&mut self.location, &ride.finish);
        self.value += ride_value;
    }

    fn add_connections(&mut self, problem: &Problem, unused: &Vec<usize>) {
        if DEBUG {
            println!("Adding connections")
        }
        self.connections = connected_rides(problem, &self, unused)
    }

    fn best_connection(&self) -> &Connection {
        self.connections.get(0)
            .expect("No best connection, because there are no connections")
    }

    fn remove_from_connections(&mut self, ride_number: usize) {
        self.connections.retain(|connection| connection.ride_number != ride_number);
    }
}

#[derive(PartialEq, Eq, PartialOrd, Ord, Debug, Clone)]
struct Connection {
    utility: i32,
    ride_number: usize
}

fn solve(problem: &Problem) -> Vec<Vehicle> {
    let mut vehicles = Vec::new();

    let mut assigned = 0;
    let mut stdout = io::stdout();

    let mut unused = (0..problem.rides.len()).collect();

    let mut vehicle = Vehicle {
        plan: Vec::new(),
        step: -1,
        location: Location {row: 0, column: 0},
        value: 0,
        connections: Vec::new()
    };
    vehicle.add_connections(problem, &unused);

    let mut vehicle_to_add: Option<Vehicle> = Some(vehicle);
    let mut ride_to_remove: Option<usize> = None;

    loop {
        if vehicle_to_add.is_some() {
            vehicles.push(vehicle_to_add.unwrap());
            vehicle_to_add = None;
        }
        if ride_to_remove.is_some() {
            remove_from_connections(ride_to_remove.unwrap(), &mut vehicles);
        }

        if unused.len() == 0 {
            break;
        }

        let fleet_not_full = (vehicles.len() as i32) < problem.vehicles;
        let optional_vehicle = best_vehicle(&mut vehicles);
        if optional_vehicle.is_none() {
            break;
        }
        let vehicle = optional_vehicle.unwrap();

        let best_ride_number = vehicle.best_connection().ride_number;

        let starting_vehicle = vehicle.plan.len() == 0;
        if starting_vehicle && fleet_not_full {
            vehicle_to_add = Some(vehicle.clone());
            if DEBUG {
                println!("Cloning starting vehicle");
            }
        }

        if DEBUG {
            println!("Found {} as best", best_ride_number);
        }

        vehicle.add_ride(problem, best_ride_number);
        ride_to_remove = Some(best_ride_number);

        assigned += 1;
        let message = format!("Rides assigned: {}/{}\r", assigned, problem.ride_amount);
        stdout.write(message.as_bytes()).expect("Could not write to stdout");
        stdout.flush().expect("Could not flush stdout");
        
        if DEBUG {
            println!("Added ride {} to vehicle", best_ride_number);
        }
        let unused_index = unused.iter()
            .position(|&ride_number| ride_number == best_ride_number)
            .expect("Best connection not in unused rides");
        unused.remove(unused_index);

        vehicle.add_connections(problem, &unused);
    }

    while (vehicles.len() as i32) < problem.vehicles {
        vehicles.push(Vehicle {
            plan: Vec::new(),
            step: -1,
            location: Location {row: 0, column: 0},
            value: 0,
            connections: Vec::new()
        });
    }

    vehicles
}

fn remove_from_connections(ride_number: usize, vehicles: &mut Vec<Vehicle>) {
    vehicles.par_iter_mut()
        .for_each(|vehicle| vehicle.remove_from_connections(ride_number));
}

fn best_vehicle(vehicles: &mut Vec<Vehicle>) -> Option<&mut Vehicle> {
    vehicles.iter_mut()
        .filter(|vehicle| !vehicle.connections.is_empty())
        .fold(None, |optional_min, vehicle| {
            if let Some(ref min) = optional_min {
                if min.best_connection().utility > vehicle.best_connection().utility {
                    return Some(vehicle);
                }
            } else {
                return Some(vehicle);
            }
            return optional_min;
        })
}


fn connected_rides(problem: &Problem, 
                   vehicle: &Vehicle, 
                   unused: &Vec<usize>) -> Vec<Connection> {

    let mut connections: Vec<Connection> = unused.par_iter()
        .map(|&ride_number| {
            let ride = get_ride(problem, ride_number);
            
            let distance_to_start = distance(&vehicle.location, &ride.start);
            let mut utility = distance_to_start;  // penalty for moving to start
            let arrival = vehicle.step + distance_to_start;

            if arrival < ride.start_after {
                let waiting_time = ride.start_after - arrival;
                utility += waiting_time;  // penalty for waiting
                utility -= problem.bonus * 1000;  // bonus for bonus
            }

            let ride_length = ride_distance(ride);
            let finish = arrival + ride_length;
            utility -= ride_length / 10;  // bonus for longer rides

            if finish > ride.finish_before {
                if DEBUG {
                    println!("Not adding {}, won't finish", ride_number);
                }
                return None;
            }
            if DEBUG {
                println!("Found a connection {} (utility: {})", ride_number, utility);
            }

            return Some(Connection {
                ride_number: ride_number,
                utility: utility
            });
        })
        .filter_map(|connection| connection)
        .collect();

    connections.par_sort_unstable();
    connections
}

fn get_ride(problem: &Problem, ride_number: usize) -> &Ride {
    problem.rides.get(ride_number)
        .expect("Ride number not found")
}

fn copy_location(target: &mut Location, source: &Location) {
    target.row = source.row;
    target.column = source.column;
}

fn ride_distance(ride: &Ride) -> i32 {
    distance(&ride.start, &ride.finish)
}

fn distance(start: &Location, finish: &Location) -> i32 {
    (start.row - finish.row).abs() + (start.column - finish.column).abs()
}

fn load_file(filename: String) -> Problem {
    let mut file = File::open(filename)
        .expect("File not found");

    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("Could not read file");

    if DEBUG {
        println!("contents:\n{}", contents);
    }

    let mut lines = contents.lines();

    let mut header = lines.next()
        .expect("Header line not found")
        .split_whitespace();

    let rows = header.next()
        .expect("Rows not found in header line")
        .parse()
        .expect("Rows is not a number");
    let columns = header.next()
        .expect("Columns not found in header line")
        .parse()
        .expect("Columns is not a number");
    let vehicles = header.next()
        .expect("Vehicles not found in header line")
        .parse()
        .expect("Vehicles is not a number");
    let ride_amount = header.next()
        .expect("Ride amount not found in header line")
        .parse()
        .expect("Ride amount is not a number");
    let bonus = header.next()
        .expect("Bonus not found in header line")
        .parse()
        .expect("Bonus is not a number");
    let steps = header.next()
        .expect("Steps not found in header line")
        .parse()
        .expect("Steps is not a number");

    let rides = lines
        .map(|line| {
            let mut split_line = line.split_whitespace();

            let start_row = split_line.next()
                .expect("Start row not found in ride")
                .parse()
                .expect("Start row not a number");
            let start_column = split_line.next()
                .expect("Start column not found in ride")
                .parse()
                .expect("Start column not a number");
            let start = Location {
                row: start_row,
                column: start_column
            };

            let finish_row = split_line.next()
                .expect("Finish row not found in ride")
                .parse()
                .expect("Finish row not a number");
            let finish_column = split_line.next()
                .expect("Finish column not found in ride")
                .parse()
                .expect("Finish column not a number");
            let finish = Location {
                row: finish_row,
                column: finish_column
            };

            let start_after = split_line.next()
                .expect("Start after not find in ride")
                .parse()
                .expect("Start after not a number");
            let finish_before = split_line.next()
                .expect("Finish before not find in ride")
                .parse()
                .expect("Finish before not a number");

            Ride {
                start: start,
                finish: finish,
                start_after: start_after,
                finish_before: finish_before
            }
        })
        .collect();

    Problem {
        rows: rows,
        columns: columns,
        vehicles: vehicles,
        ride_amount: ride_amount,
        bonus: bonus,
        steps: steps,
        rides: rides
    }
}

fn export(name: String, solution: Vec<Vehicle>) {
    let timestamp = Local::now().format("%Y%m%d-%H%M");
    let filename = format!("./output/{}_{}.txt", timestamp, name);
    
    let mut file = File::create(filename)
        .expect("File not found");

    for vehicle in solution {
        let plan: Vec<String> = vehicle.plan.iter()
            .map(|ride_number| ride_number.to_string())
            .collect();
        let line = format!("{} {}\n", vehicle.plan.len(), plan.join(" "));
        file.write(line.as_bytes())
            .expect("Could not write to file");
    }
}

fn stats(problem: &Problem, solution: &Vec<Vehicle>) -> i32 {
    let (total_value, assigned) = solution.iter()
        .fold((0, 0), |(total_value, assigned), vehicle| {
            return (total_value + vehicle.value, assigned + vehicle.plan.len());
        });

    println!("Rides assigned: {}/{}    ", assigned, problem.ride_amount);
    println!("Total expected value: {}", total_value);
    total_value
}

fn main() {
    let start = std::time::Instant::now();
    let datasets: Vec<String>;
    if DEBUG {
        datasets = vec!("a_example".to_string());
    } else {
        datasets = ["a_example", "b_should_be_easy", "c_no_hurry",
                    "d_metropolis", "e_high_bonus"].iter()
                        .map(|filename| filename.to_string())
                        .collect();
    }

    let mut total = 0;
    for dataset in datasets {
        println!("=={}==", dataset);
        let problem = load_file(format!("{}.in", dataset));
        if DEBUG {
            println!("{:?}", problem);
        }
        let solution = solve(&problem);
        total += stats(&problem, &solution);
        if DEBUG {
            println!("Solution:\n{:?}", solution);
        }
        println!("");  // new line
        export(dataset, solution);
    }
    println!("Total expected value of this solution: {}", total);

    let elapsed = start.elapsed();
    let seconds = (elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1_000_000_000.0);
    println!("Took: {} seconds", seconds);
}
