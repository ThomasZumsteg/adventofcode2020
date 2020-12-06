use common::get_input;
use std::collections::HashSet;
use itertools::Itertools;

type Input = Vec<Vec<char>>;

fn binary_search(values: &Vec<bool>, lower: isize, upper: isize) -> isize {
    let mut upper = upper as f32;
    let mut lower = lower as f32;
    for &value in values {
        let mid = ((upper - lower) / 2.0) + lower;
        if value {
            upper = mid.floor();
        } else {
            lower = mid.ceil();
        }
    }
    lower as isize
}

fn part1(boardingpasses: &Input) -> isize {
    boardingpasses.iter()
        .map(|pass| {
            let row = binary_search(&pass[..7].iter().map(|&c| c == 'F').collect(), 0, 127);
            let col = binary_search(&pass[7..pass.len()].iter().map(|&c| c == 'L').collect(), 0, 7);
            row * 8 + col
        })
        .max()
        .unwrap()
}

fn part2(boardingpasses: &Input) -> isize {
    let mut seats = (0..128).cartesian_product(0..8).collect::<HashSet<(isize, isize)>>();
    for boardingpass in boardingpasses {
        let row = binary_search(
            &boardingpass[..7].iter().map(|&c| c == 'F').collect(),
            0,
            127
        );
        let col = binary_search(
            &boardingpass[7..boardingpass.len()].iter().map(|&c| c == 'L').collect(),
            0,
            7
        );
        seats.remove(&(row, col));
    }
    for i in 0..(128/2) {
        if seats.len() == 1 {
            let seat = seats.iter().next().unwrap();
            return seat.0 * 8 + seat.1;
        }
        seats = seats.iter().filter(|&seat| i <= seat.0 && seat.0 <= (127 - i)).map(|&seat| seat).collect();
    }
    unimplemented!()

}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_search_row() {
        let search: Vec<bool> = "FBFBBFF".chars().map(|c| c == 'F').collect();
        assert_eq!(binary_search(&search, 0, 127), 44);
    }

    #[test]
    fn test_binary_search_col() {
        let search: Vec<bool> = "RLR".chars().map(|c| c == 'L').collect();
        assert_eq!(binary_search(&search, 0, 7), 5);
    }
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|l| l.chars().collect())
        .collect()
}

fn main() {
    let input = parse(get_input(05, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
