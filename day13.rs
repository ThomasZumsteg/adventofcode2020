use common::get_input;
use num::BigInt;
use std::cmp;

type Input = (usize, Vec<Option<usize>>);

fn part1(input: &Input) -> isize {
    let start = input.0.clone();
    let next = input.1.iter()
        .filter_map(|&b| b)
        .map(|b| {
            (b, b * (start/ b + 1))
        })
        .min_by_key(|&b| b.1)
        .unwrap();
    (next.0 * (next.1 - start)) as isize
}

type Bus = (BigInt, usize);

fn bus_lcm(bus_a: &Bus, bus_b: &Bus) -> Bus {
    let mut a = cmp::max(bus_a.1, bus_b.1);
    let mut b = cmp::min(bus_a.1, bus_b.1);
    while b > 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    let period = (bus_a.1 * bus_b.1) / a;
    let mut offset: BigInt = bus_a.0.clone();
    loop {
        offset += bus_a.1;
        if (offset.clone() - bus_b.0.clone()) % BigInt::from(bus_b.1) == BigInt::from(0) {
            return (offset, period)
        }
    }
}

fn part2(buses: &Input) -> BigInt {
    let mut bus_list = buses.1.iter().enumerate()
        .filter_map(|bus| if let (b, Some(num)) = bus { Some((BigInt::from(b), *num)) } else { None });
    let mut last = bus_list.next().map(|b| (BigInt::from(b.0), b.1)).unwrap();
    for bus in bus_list {
        last = bus_lcm(&last, &bus);
    }
    last.1 - last.0
}

fn parse(text: String) -> Input {
    let mut lines = text.trim().split('\n').map(|l| l.trim());
    (
        lines.next().unwrap().parse::<usize>().unwrap(),
        lines.next().unwrap().split(',')
            .map(|line| if line == "x" { None } else { Some(line.parse::<usize>().unwrap()) })
            .collect()
    )
}

fn main() {
    let input = parse(get_input(13, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));

}
