use common::get_input;
use std::collections::{HashMap,HashSet};

type Input = Vec<Option<Passport>>;

#[derive(Debug)]
struct Passport {
    byr: String,
    iyr: String,
    eyr: String,
    hgt: String,
    hcl: String,
    ecl: String,
    pid: String,
    cid: Option<String>,
}

impl Passport {
    fn new(line: String) -> Option<Passport> {
        let mut fields = HashMap::new();
        for field in line.split(" ") {
            let index = field.find(":").unwrap();
            fields.insert(field[0..index].to_string(), field[index+1..].to_string());
        }
        Some(Passport {
            byr: fields.get("byr")?.to_string(),
            iyr: fields.get("iyr")?.to_string(),
            eyr: fields.get("eyr")?.to_string(),
            hgt: fields.get("hgt")?.to_string(),
            hcl: fields.get("hcl")?.to_string(),
            ecl: fields.get("ecl")?.to_string(),
            pid: fields.get("pid")?.to_string(),
            cid: fields.get("cid").map(|s| s.to_string()),
        })
    }

    fn is_valid(&self) -> bool {
        self.valid_hgt() && self.valid_byr() && self.valid_iyr() &&
            self.valid_hcl() &&self.valid_ecl() && self.valid_pid() && self.valid_eyr()
    }

    fn valid_byr(&self) -> bool {
        if let Ok(year) = self.byr.parse::<usize>() {
            return 1920 <= year && year <= 2002
        }
        false
    }

    fn valid_iyr(&self) -> bool {
        if let Ok(year) = self.iyr.parse::<usize>() {
            return 2010 <= year && year <= 2020
        }
        false
    }

    fn valid_eyr(&self) -> bool {
        if let Ok(year) = self.eyr.parse::<usize>() {
            return 2020 <= year && year <= 2030
        }
        false
    }

    fn valid_hgt(&self) -> bool {
        if self.hgt.ends_with("cm") {
            if let Ok(hgt) = self.hgt[..self.hgt.len()-2].parse::<usize>() {
                return 150 <= hgt && hgt <= 193;
            }
        } else if self.hgt.ends_with("in") {
            if let Ok(hgt) = self.hgt[..self.hgt.len()-2].parse::<usize>() {
                return 59 <= hgt && hgt <= 76;
            }
        }
        false
    }

    fn valid_hcl(&self) -> bool {
        if self.hcl.len() == 7 && &self.hcl[..1] == "#" {
            let letters = self.hcl[1..].chars().collect::<HashSet<char>>();
            let hex = "abcdef0123456789".chars().collect::<HashSet<char>>();
            return letters.is_subset(&hex)
        }
        false
    }

    fn valid_ecl(&self) -> bool {
        let valid_colors = vec!["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            .iter()
            .map(|&s| s)
            .collect::<HashSet<&str>>();
        valid_colors.contains(&self.ecl.as_str())
    }

    fn valid_pid(&self) -> bool {
        if self.pid.len() == 9 {
            return self.pid.parse::<usize>().is_ok()
        }
        false
    }
}

fn part1(passports: &Input) -> isize {
    passports.iter().filter(|p| p.is_some()).count() as isize
}

fn part2(passports: &Input) -> isize {
    passports.iter().filter(|p| {
        if let Some(p) = p {
            return p.is_valid()
        }
        false
    }).count() as isize
}

fn parse(text: String) -> Input {
    let mut fields: Vec<String> = vec![];
    let mut results = vec![];
    let text = text + "\n";
    for line in text.split('\n') {
        if line == "" && fields.len() > 0 {
            results.push(Passport::new(fields.join(" ")));
            fields.clear();
        } else {
            fields.push(line.to_string());
        }
    }
    results
}

fn main() {
    let input = parse(get_input(04, 2020));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
