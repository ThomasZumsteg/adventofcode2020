use common::get_input;
use std::collections::HashMap;

type Input = Vec<usize>;

struct Game<'a> {
    turns: HashMap<usize, usize>,
    starting: &'a[usize],
    turn: usize,
    last: Option<usize>,
}

impl<'a> Game <'a> {
    fn new(starting: &'a[usize] ) -> Game {
        Game {
            turns: HashMap::new(),
            starting,
            turn: 0,
            last: None,
        }
    }
}

impl<'a> Iterator for Game<'a> {
    type Item = usize;

    fn next(&mut self) -> Option<usize> {
        self.turn += 1;
        let next = if let Some(&initial) = self.starting.get(self.turn-1) {
            initial
        } else if let Some(last) = self.turns.get(&self.last.unwrap()) {
            self.turn - last
        } else {
            0
        };
        // println!("{}: {} - {:?}", self.turn, next, self.turns);
        if let Some(last) = self.last {
            self.turns.insert(last, self.turn);
        }
        self.last = Some(next);
        Some(next)
    }
}

fn part1(input: &Input) -> usize {
    Game::new(input).nth(2020-1).unwrap()
}

fn part2(input: &Input) -> usize {
    Game::new(input).nth(30000000-1).unwrap()
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|line| line.split(',').map(|n| n.parse::<usize>().unwrap()).collect())
        .next()
        .unwrap()
}

fn main() {
    assert_eq!(part1(&vec![0, 3, 6]), 436);
    assert_eq!(part1(&vec![1, 3, 2]), 1);
    assert_eq!(part1(&vec![2, 1, 3]), 10);
    assert_eq!(part1(&vec![1, 2, 3]), 27);
    assert_eq!(part1(&vec![3, 1, 2]), 1836);
    assert_eq!(part1(&vec![3, 2, 1]), 438);
    let input = parse(get_input(15, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
