use common::get_input;
use std::collections::{HashMap, HashSet};
use itertools::Itertools;

type Point = Vec<isize>;
type Input = HashMap<Point, char>;

fn neighbors(p: &Point) -> Vec<Point> {
    (0..p.len()).map(|_| -1..2).multi_cartesian_product()
        .filter_map(|d|
            if d.iter().all(|v| v == &0) {
                None
            } else {
                Some(p.iter().zip(d.iter()).map(|(i, j)| i + j).collect())
            })
        .collect()
}

fn part1(input: &Input) -> usize {
    let mut current: HashMap<Point, char> = input.iter()
        .filter_map(|(k, v)| if v == &'#' { Some((k.clone(), *v)) } else { None })
        .collect();
    for _ in 0..6 {
        let prev = current;
        current = HashMap::new();
        let active: HashSet<Point> = prev.iter()
            .filter_map(|(k, v)| if v == &'#' { Some(neighbors(k)) } else { None }).flatten().collect();
        for point in active {
            let value = prev.get(&point).unwrap_or(&'.');
            let count = neighbors(&point).iter().filter(|&p| Some(&'#') == prev.get(p)).count();
            if vec![(2, '#'), (3, '#'), (3, '.')].contains(&(count, *value)) {
                current.insert(point, '#');
            }
        }
    }
    current.len()
}

fn part2(input: &Input) -> usize {
    let mut current: HashMap<Point, char> = HashMap::new();
    for (k, v) in input.iter() {
        if v != &'#' {
            continue
        }
        let mut key = k.clone();
        key.push(0);
        current.insert(key, '#');
    }
    for _ in 0..6 {
        let prev = current;
        current = HashMap::new();
        let active: HashSet<Point> = prev.iter()
            .filter_map(|(k, v)| if v == &'#' { Some(neighbors(k)) } else { None }).flatten().collect();
        for point in active {
            let value = prev.get(&point).unwrap_or(&'.');
            let count = neighbors(&point).iter().filter(|&p| Some(&'#') == prev.get(p)).count();
            if vec![(2, '#'), (3, '#'), (3, '.')].contains(&(count, *value)) {
                current.insert(point, '#');
            }
        }
    }
    current.len()
}

fn parse(text: String) -> Input {
    text.trim().split('\n').enumerate().map(|(r, row)| {
        row.chars().enumerate().map(move |(c, chr)| (vec![c as isize, r as isize, 0], chr))
    }).flatten().collect()
}

fn main() {
    assert_eq!(part1(&parse(".#.\n..#\n###".to_string())), 112);
    assert_eq!(part2(&parse(".#.\n..#\n###".to_string())), 848);
    let input = parse(get_input(17, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
