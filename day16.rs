use common::get_input;
use regex::Regex;
use std::collections::{HashMap, HashSet};

#[derive(Debug)]
struct Input {
    your_ticket: Vec<usize>,
    rules: HashMap<String, Rule>,
    nearby_tickets: Vec<Vec<usize>>,
}

type Rule = ((usize, usize), (usize, usize));

fn fits(rule: &Rule, value: usize) -> bool {
    assert!((rule.0).0 <= (rule.0).1 && (rule.1).0 <= (rule.1).1);
    ((rule.0).0 <= value && value <= (rule.0).1) || ((rule.1).0 <= value && value <= (rule.1).1)
}

fn part1(input: &Input) -> usize {
    input.nearby_tickets.iter().flatten().filter(|&&value| {
        input.rules.values().all(|rule| { !fits(rule, value)})
    }).sum()
}

fn part2(input: &Input) -> usize {
    let rules = input.rules.clone();
    let mut fields = (0..rules.len()).map(|n| (n, rules.keys().collect::<HashSet::<&String>>()))
        .collect::<HashMap<usize, HashSet<&String>>>();
    for ticket in input.nearby_tickets.clone() {
        if !ticket.iter().all(|&number| rules.values().any(|rule| fits(rule, number))) {
            continue
        }
        for (col, &num) in ticket.iter().enumerate() {
            for (name, rule) in rules.iter() {
                if !fits(&rule, num) {
                    fields.get_mut(&col).unwrap().remove(&name);
                }
            }
        }
    }
    let mut solved = HashSet::new();
    let mut names = HashMap::new();
    while solved.len() != fields.len() {
        for (key, value) in fields.iter() {
            if names.contains_key(key) {
                continue
            }
            let diff = value - &solved;
            if diff.len() == 1 {
                let name = diff.iter().next().unwrap().clone();
                solved.insert(name);
                names.insert(key, name);
                break
            } else if diff.len() == 0 {
                unimplemented!()
            }
        }
    }
    let mut total = 1;
    for (&&col, name) in names.iter() {
        if !name.starts_with("departure") {
            continue
        }
        total *= input.your_ticket[col];
    }
    return total
}

fn parse(text: String) -> Input {
    let mut state: Option<&str> = Some("rules");
    let mut result = Input { 
        your_ticket: Vec::new(),
        rules: HashMap::new(),
        nearby_tickets: Vec::new()
    };
    let rule_regex = Regex::new(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)").unwrap();
    for mut line in text.trim().split('\n') {
        line = line.trim();
        match state {
            _ if line == "" => state = None,
            Some("your ticket") =>
                result.your_ticket = line.split(',').map(|n| n.parse::<usize>().unwrap()).collect(),
            Some("nearby tickets") =>
                result.nearby_tickets.push(line.split(',').map(|n| n.parse::<usize>().unwrap()).collect()),
            Some("rules") => {
                let m = rule_regex.captures(line).unwrap();
                result.rules.insert(
                    m.get(1).unwrap().as_str().to_string(),
                    ((
                        m.get(2).unwrap().as_str().parse::<usize>().unwrap(),
                        m.get(3).unwrap().as_str().parse::<usize>().unwrap()
                    ),(
                        m.get(4).unwrap().as_str().parse::<usize>().unwrap(),
                        m.get(5).unwrap().as_str().parse::<usize>().unwrap()
                    ))
                );
            },
            None if line.chars().nth(line.len()-1) == Some(':') => state = Some(&line[0..line.len()-1]),
            _ => unimplemented!(),
        }
    }
    result
}

fn main() {
    let input = parse(get_input(16, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
