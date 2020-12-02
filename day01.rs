use common::get_input;
use itertools::Itertools;

type Input = Vec<isize>;

fn find_size(nums: &Vec<isize>, target: isize, len: usize) -> Option<isize> {
    for combo in nums.into_iter().combinations(len) {
        if combo.clone().into_iter().sum::<isize>() == target {
            return Some(combo.into_iter().product::<isize>())
        }
    }
    None
}

fn part1(input: &Input) -> isize {
    find_size(input, 2020, 2).unwrap()
}

fn part2(input: &Input) -> isize {
    find_size(input, 2020, 3).unwrap()
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|n| n.parse::<isize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(get_input(01, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
