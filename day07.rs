use common::get_input;
use std::collections::{VecDeque, HashSet, HashMap};
use regex::Regex;

type Bag = String;
type Input = HashMap<Bag, HashSet<(usize, Bag)>>;

fn part1(bags: &Input) -> usize {
    let mut container_map = HashMap::new();
    for (bag, containers) in bags {
        for (_, container) in containers {
            container_map.entry(container).or_insert(HashSet::new()).insert(bag);

        }
    }
    let mut queue: VecDeque<String> = VecDeque::new();
    let mut seen: HashSet<String> = HashSet::new();
    queue.push_back("shiny gold".to_string());
    while let Some(bag_type) = queue.pop_front() {
        if seen.contains(&bag_type) {
            continue;
        }
        seen.insert(bag_type.to_string());
        for container in container_map.get(&bag_type.to_string()).unwrap_or(&HashSet::new()).iter() {
            queue.push_back(container.to_string());
        }
    }
    seen.len() - 1
}

fn part2(bags: &Input) -> usize {
    let mut total = 0;
    let mut queue = VecDeque::new();
    queue.push_back((1, "shiny gold"));
    while let Some((count, bag_type)) = queue.pop_front() {
        total += count;
        for (inner_count, inner_type) in bags.get(bag_type).unwrap().iter() {
            queue.push_back((inner_count * count, inner_type));
        }
    }
    total - 1
}

fn parse(text: String) -> Input {
    let mut map = HashMap::new();
    let bag_regex = Regex::new(r"^(\w+ \w+)").unwrap();
    let contains_regex = Regex::new(r"(\d+) (\w+ \w+)").unwrap();
    for line in text.trim().split('\n') {
        let bag = bag_regex.find(line).unwrap().as_str();
        map.insert(bag.to_string(), HashSet::new());
        for contains in contains_regex.captures_iter(line) {
            let count = contains[1].parse::<usize>().unwrap();
            let container = contains[2].to_string();
            map.get_mut(&bag.to_string()).unwrap().insert((count, container));
        }
    }
    map
}

fn main() {
    let input = parse(get_input(07, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
