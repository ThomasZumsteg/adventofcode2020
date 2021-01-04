use common::get_input;
use num::BigInt;
use regex::Regex;
use std::collections::HashMap;

type Input = Vec<Mask>;

enum Mask {
    Mem {address: usize, value: usize},
    Mask {mask: String}
}

fn apply_mask(value: &String, mask: &String, update: &Box<dyn Fn(char, char) -> char>) -> BigInt {
    assert_eq!(value.len(), mask.len());
    assert_eq!(value.len(), 36);
    let mut result: BigInt = BigInt::from(0);
    for (v, m) in value.chars().zip(mask.chars()) {
        result *= BigInt::from(2);
        result += BigInt::from(update(v, m) as u8 - '0' as u8);
    }
    result
}

fn part1(input: &Input) -> BigInt {
    let mut memory: HashMap<usize, BigInt> = HashMap::new();
    let mut mask: Option<&String> = None;
    let update: Box<dyn Fn(char, char) -> char> = Box::new(|v, m| {
        match m {
            'X' => v,
            '1' | '0' => m,
            _ => unimplemented!()
        }
    });
    for line in input {
        match line {
            Mask::Mem { address, value } => {
                let value = format!("{:036b}", value);
                memory.insert(*address, apply_mask(&value, mask.unwrap(), &update));
            },
            Mask::Mask { mask: m } => { mask = Some(m); },
        };
    }
    memory.values().fold(BigInt::from(0), |acc, x| acc + x)
}

fn make_masks(mask: String, value: &usize) -> Box<dyn Iterator<Item=BigInt>> {
    let count = mask.matches("X").count();
    let value = format!("{:036b}", value);
    assert_eq!(value.len(), mask.len());
    assert_eq!(value.len(), 36);
    Box::new((0u32..2u32.pow(count as u32)).map(move |combo| {
        let mut combo = combo;
        let mut result = BigInt::from(0);
        for (m, v) in mask.chars().zip(value.chars()) {
            result *= 2;
            result += BigInt::from(match m {
                'X' => {
                    // Value
                    let t = combo & 1;
                    combo >>= 1;
                    t
                },
                '0' => (v as u32 - '0' as u32),
                '1' => (m as u32 - '0' as u32),
                _ => unimplemented!(),
            });
        }
        assert_eq!(combo, 0);
        result
    }))
}

fn part2(input: &Input) -> usize {
    let mut memory: HashMap<BigInt, usize> = HashMap::new();
    let mut mask: Option<&String> = None;
    for line in input {
        match line {
            Mask::Mem { address, value } => {
                for addr in make_masks(mask.unwrap().clone(), address) {
                    memory.insert(addr, *value);
                }
            },
            Mask::Mask { mask: m } => { mask = Some(m); },
        };
    }
    memory.values().fold(0, |acc, x| acc + x)
}

fn parse(text: String) -> Input {
    let mem_regex = Regex::new(r"mem\[(\d+)\] = (\d+)").unwrap();
    let mask_regex = Regex::new(r"mask = ([01X]+)").unwrap();
    text.trim()
        .split('\n')
        .map(|line| {
            if let Some(m) = mem_regex.captures(line.trim()) {
                Mask::Mem { 
                    address: m.get(1).unwrap().as_str().parse::<usize>().unwrap(),
                    value: m.get(2).unwrap().as_str().parse::<usize>().unwrap()
                }
            } else if let Some(m) = mask_regex.captures(line.trim()) {
                Mask::Mask {
                    mask: m.get(1).unwrap().as_str().to_string()
                }
            } else {
                unimplemented!()
            }
        })
        .collect()
}

fn main() {
    let input = parse(get_input(14, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
