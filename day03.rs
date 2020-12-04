use common::get_input;
use common::point::Point;

#[derive(PartialEq)]
enum Space {
    Tree,
    Open
}

type Input = Vec<Vec<Space>>;

fn count_trees(input: &Vec<Vec<Space>>, slope: &Point) -> usize {
    let mut pos = Point::new(0, 0);
    let mut total = 0;
    while (pos.y as usize) < input.len() {
        let y = pos.y as usize;
        let x = (pos.x as usize) % (input[y].len());
        if input[y][x] == Space::Tree {
            total += 1;
        }
        pos = pos + *slope;
    }
    total
}

fn part1(input: &Input) -> usize {
    count_trees(input, &Point::new(3, 1))
}

fn part2(input: &Input) -> usize {
    let slopes = vec![
        Point::new(1, 1),
        Point::new(3, 1),
        Point::new(5, 1),
        Point::new(7, 1),
        Point::new(1, 2)
    ];
    let mut total = 1;
    for slope in slopes {
        total *= count_trees(input, &slope);
    }
    total
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|line| {
            line.chars()
                .map(|c| if c == '#' { Space::Tree } else { Space::Open })
                .collect()
        })
        .collect()
}

fn main() {
    let input = parse(get_input(03, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

