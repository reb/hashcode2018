use std::fs::File;
use std::io::prelude::*;

const DEBUG: bool = true;

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

#[derive(Debug)]
struct Location {
    row: i32,
    column: i32
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

fn main() {
    let datasets: Vec<String>;
    if DEBUG {
        datasets = vec!("a_example".to_string());
    } else {
        datasets = vec!("a_example".to_string());
    }

    for dataset in datasets {
        let problem = load_file(format!("{}.in", dataset));
        if DEBUG {
            println!("{:?}", problem);
        }
    }
}
