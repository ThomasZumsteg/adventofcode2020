use common::get_input;
use common::point::Point;
use std::collections::HashMap;

type Input = HashMap<Point, char>;

fn surround(grid: &Input, location: &Point, seek: &dyn Fn(&Input, &Point, &Point) -> bool) -> usize {
    let mut total = 0;
    let points = vec![
        Point::new( 1, -1), Point::new( 1,  0), Point::new( 1,  1),
        Point::new( 0, -1),                     Point::new( 0,  1),
        Point::new(-1, -1), Point::new(-1,  0), Point::new(-1,  1),
    ];
    for diff in points {
        if seek(grid, &location, &diff) {
            total += 1;
        }
    }
    total
}

fn update(grid: &Input, rules: &dyn Fn(&Input, &Point) -> char) -> Input {
    let mut new = grid.clone();
    for (key, val) in new.iter_mut() {
        *val = rules(grid, key);
    }
    new
}

fn part1(seating: &Input) -> usize {
    let mut last = seating.clone();
    let mut current;
    loop {
        fn rules(grid: &Input, location: &Point) -> char {
            fn seek(grid: &Input, pos: &Point, diff: &Point) -> bool {
                grid.get(&(*pos + *diff)) == Some(&'#')
            }
            let seat = grid[location];
            if seat == 'L' && surround(&grid, location, &seek) == 0 {
                return '#'
            } else if seat == '#' && surround(&grid, location, &seek) >= 4 {
                return 'L'
            }
            seat
        };
        current = update(&last, &rules);
        if last == current {
            return current.values().filter(|&&c| c == '#').count()
        }
        last = current;
    }
}

fn part2(seating: &Input) -> usize {
    let mut last = seating.clone();
    let mut current;
    loop {
        fn rules(grid: &Input, location: &Point) -> char {
            fn seek(grid: &Input, pos: &Point, diff: &Point) -> bool {
                match grid.get(&(*pos + *diff)) {
                    Some('#') => true,
                    Some('L')|None => false,
                    Some('.') => seek(grid, &(*pos+*diff), diff),
                    _ => unimplemented!()
                }
            }
            let seat = grid[location];
            if seat == 'L' && surround(&grid, location, &seek) == 0 {
                return '#'
            } else if seat == '#' && surround(&grid, location, &seek) >= 5 {
                return 'L'
            }
            seat
        };
        current = update(&last, &rules);
        if last == current {
            return current.values().filter(|&&c| c == '#').count()
        }
        last = current;
    }
}

fn parse(text: String) -> Input {
    let mut seats = HashMap::new();
    for (r, row) in text.split('\n').enumerate() {
        for (c, seat) in row.chars().enumerate() {
            seats.insert(Point::new(r as i32, c as i32), seat);
        }
    }
    seats
}

fn main() {
    let input = parse(get_input(11, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
