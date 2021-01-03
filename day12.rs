use common::get_input;

type Input = Vec<(String, usize)>;
type Point = (isize, isize);
type Update = Box<dyn Fn(Point, Point, &usize) -> (Point, Point)>;

fn move_point(diff: Point) -> Update {
    Box::new(move |heading, position, &value| {
        (
            heading,
            (position.0 + diff.0 * (value as isize), position.1 + diff.1 * (value as isize))
        )
    })
}

fn turn(update: Box<dyn Fn(Point) -> Point>) -> Update {
    Box::new(move |heading, position, &value| {
        let mut heading = heading;
        let mut value = value;
        while value > 0 {
            value -= 90;
            heading = update(heading);
        }
        assert!(value == 0);
        (heading, position)
    })
}

fn part1(directions: &Input) -> isize {
    let mut heading = (1, 0);
    let mut position = (0, 0);
    for (order, value) in directions {
        let forward: Update = Box::new(|heading, position, &value| {
            (heading, (position.0 + value as isize * heading.0, position.1 + value as isize * heading.1))
        });
        let update = match order.as_str() {
            "N" => move_point((0, 1)),
            "S" => move_point((0, -1)),
            "E" => move_point((1, 0)),
            "W" => move_point((-1, 0)),
            "R" => turn(Box::new(|(r, i)| (i, -r))),
            "L" => turn(Box::new(|(r, i)| (-i, r))),
            "F" => forward,
            _ => unimplemented!(),
        };
        let result = update(heading, position, value);
        heading = result.0;
        position = result.1;
    }
    position.0.abs() + position.1.abs()
}

fn swap(func: Update) -> Update {
    Box::new(move |heading, position, value| {
        let result = func(position, heading, value);
        (result.1, result.0)
    })
}

fn part2(directions: &Input) -> isize {
    let mut waypoint = (10, 1);
    let mut position = (0, 0);
    for (order, value) in directions {
        let forward: Update = Box::new(|heading, position, &value| {
            (heading, (position.0 + value as isize * heading.0, position.1 + value as isize * heading.1))
        });
        let update = match order.as_str() {
            "N" => swap(move_point((0, 1))),
            "S" => swap(move_point((0, -1))),
            "E" => swap(move_point((1, 0))),
            "W" => swap(move_point((-1, 0))),
            "R" => turn(Box::new(|(r, i)| (i, -r))),
            "L" => turn(Box::new(|(r, i)| (-i, r))),
            "F" => forward,
            _ => unimplemented!(),
        };
        let result = update(waypoint, position, value);
        waypoint = result.0;
        position = result.1;
    }
    position.0.abs() + position.1.abs()
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|line| {
            (
                line.chars().next().unwrap().to_string(),
                line.chars().skip(1).collect::<String>().parse::<usize>().unwrap(),
            )
        })
        .collect()
}

fn main() {
    let input = parse(get_input(12, 2020)); 
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

