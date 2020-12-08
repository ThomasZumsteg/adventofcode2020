use common::get_input;
use itertools::Itertools;

type Input = Vec<Vec<Vec<char>>>;

fn part1(groups: &Input) -> usize {
    groups.iter().map(|group|
        group.iter().flatten().unique().count()
    ).sum()
}

fn part2(groups: &Input) -> usize {
    groups.iter().map(|group| {
        group.iter()
            .flatten()
            .unique()
            .filter(|c| group.iter().all(|g| g.contains(c)))
            .count()
    }).sum()
}

fn parse(text: String) -> Input {
    let mut result = vec![vec![]];
    for line in text.trim().split('\n') {
        if line == "" {
            result.push(vec![]);
        } else {
            result.last_mut().unwrap().push(line.chars().collect());
        }
    }
    result
}

fn main() {
    let input = parse(get_input(06, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
