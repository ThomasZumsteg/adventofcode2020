use common::get_input;
use std::collections::HashSet;

type Input = Vec<(String, isize)>;

#[derive(Debug, Clone)]
struct Program {
    code: Input,
    accumulator: isize,
    index: isize
}

impl Program {
    fn new(code: Input) -> Program {
        Program { code, index: 0, accumulator: 0 }
    }

    fn run(&mut self) -> Program {
        let mut seen = HashSet::new();
        while let Some((op, value)) = self.code.get(self.index as usize) {
            if seen.contains(&self.index) {
                return self.clone();
            }
            seen.insert(self.index);

            match op.as_str() {
                "jmp" => self.index += *value,
                "nop" => self.index += 1,
                "acc" => {
                    self.accumulator += value;
                    self.index += 1;
                }
                _ => unimplemented!(),
            }
        }
        self.clone()
    }
}

fn part1(code: &Input) -> isize {
    let mut program = Program::new(code.clone());
    program.run();
    program.accumulator
}

fn part2(input: &Input) -> isize {
    for (line_num, (cmd, value)) in input.iter().enumerate() {
        let mut program = input.clone();
        match cmd.as_str() {
            "jmp" => program[line_num] = ("nop".to_string(), *value),
            "nop" => program[line_num] = ("jmp".to_string(), *value),
            _ => continue,
        }
        let result = Program::new(program).run();
        if !(0 <= result.index && result.index < result.code.len() as isize) {
            return result.accumulator
        }
    }
    unimplemented!()
}

fn parse(text: String) -> Input {
    text.trim()
        .split('\n')
        .map(|line| {
            let mut split = line.split(' ');
            let command = split.next().unwrap().to_string();
            let value = split.next().unwrap().parse::<isize>().unwrap();
            (command, value)
        })
        .collect()
}

fn main() {
    let input = parse(get_input(08, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
