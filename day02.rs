use common::get_input;
use regex::Regex;

type Input = Vec<((usize, usize), String, String)>;


fn part1(input: &Input) -> usize {
    input.iter()
        .filter(|((a, b), letter, password)| {
            let count = password.matches(letter).count();
            a <= &count && &count <= b
        })
        .count()
}

fn matches_once<T: PartialEq>(letter: T, a: T, b: T) -> bool {
    a != b && (letter == a || letter == b)
}

fn part2(input: &Input) -> usize {
    input.iter()
        .filter(|((a, b), letter, password)| {
            let chars = password.as_str();
            matches_once(letter.as_str(), &chars[(a-1)..*a], &chars[(b-1)..*b])
        })
        .count()
}

macro_rules! parse {
    ( $cap:expr, $i:expr, $type:ty ) => {
        $cap.get($i).unwrap().as_str().parse::<$type>().unwrap()
    }
}

fn parse(text: String) -> Input {
    let re = Regex::new(r"^(\d+)-(\d+) (.+): (.+)$").unwrap();
    text.trim()
        .split('\n')
        .map(|line| {
            let cap = re.captures(line).unwrap();
            ((parse!(cap, 1, usize), parse!(cap, 2, usize)), parse!(cap, 3, String), parse!(cap, 4, String))
        })
        .collect()
}

fn main() {
    let input = parse(get_input(02, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
