#![feature(test)]

use common::get_input;
use std::collections::{HashMap, HashSet};
use std::iter::FromIterator;


type Input = Vec<usize>;

fn part1(adaptors: &Input) -> usize {
    let mut adaptors = adaptors.clone();
    adaptors.push(0);
    adaptors.push(adaptors.iter().max().unwrap()+3);
    adaptors.sort();
    let mut diff_count = HashMap::new();
    for (a, b) in adaptors.iter().zip(adaptors.iter().skip(1)) {
        *diff_count.entry(b-a).or_insert(0) += 1;
    }
    diff_count[&1] * diff_count[&3]
}

fn part2(adaptors: &Input) -> usize {
    part2_recurse(adaptors)
}

fn part2_recurse(adaptors: &Input) -> usize {
    let start = *adaptors.iter().max().unwrap() as isize;
    let adaptors = HashSet::from_iter(adaptors.iter().map(|&n| n as isize));
    let mut cache = HashMap::new();
    steps(start, &adaptors, &mut cache)
}

fn steps(n: isize, adaptors: &HashSet<isize>, cache: &mut HashMap<isize, usize>) -> usize {
    if !cache.contains_key(&n) {
        let result = match n {
            0 => 1,
            a if !adaptors.contains(&a) => 0,
            _ => steps(n-1, adaptors, cache) + steps(n-2, adaptors, cache) + steps(n-3, adaptors, cache)
        };
        cache.insert(n, result);
    }
    *cache.get(&n).unwrap()
}

#[allow(dead_code)]
fn part2_iter(adaptors: &Input) -> usize {
    let mut paths: HashMap<usize, usize> = HashMap::new();
    paths.insert(0, 1);
    let mut chain = adaptors.clone();
    chain.push(0);
    chain.sort();
    for (i, adaptor) in chain.iter().enumerate() {
        for value in chain[(i+1)..].iter() {
            if value - adaptor > 3 {
                break
            }
            *paths.entry(*value).or_insert(0) += paths.get(&adaptor).unwrap().clone();
        }
    }
    paths[adaptors.iter().max().unwrap()]
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|n| n.parse::<usize>().unwrap())
        .collect()
}

fn main() {
    let input = parse(get_input(10, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}


#[cfg(test)]
mod tests {
    extern crate test;

    use super::*;
    use test::Bencher;

    #[bench]
    fn bench_iter(b: &mut Bencher) {
        let input = parse(get_input(10, 2020));
        b.iter(|| part2_iter(&input));
    }

    #[bench]
    fn bench_recurse(b: &mut Bencher) {
        let input = parse(get_input(10, 2020));
        b.iter(|| part2_recurse(&input));
    }
}
