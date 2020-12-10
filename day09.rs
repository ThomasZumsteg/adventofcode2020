use common::get_input;
use itertools::Itertools;

type Input = Vec<isize>;

fn part1(input: &Input) -> isize {
    for i in 25.. {
        let slice: Vec<&isize> = input[i-25..i].iter().collect();
        if !slice.iter().combinations(2).any(|combo| *combo[0] + *combo[1] == input[i]) {
            return input[i]
        }
    }
    unimplemented!()
}

fn part2(input: &Input) -> isize {
    let target = part1(input);
    for i in 0..input.len() {
        for j in (i+1)..input.len() {
            let total: isize = input[i..j].iter().sum();
            if total == target {
                return input[i..j].iter().max().unwrap() + input[i..j].iter().min().unwrap();
            } else if total > target {
                break
            }
        }
    }
    unimplemented!()
}

fn parse(text: String) -> Input {
    text.trim().split('\n')
        .map(|n| n.parse::<isize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(get_input(09, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
