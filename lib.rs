use std::io::prelude::*;
use std::fs::File;

pub fn get_input(day: u8, year: u16) -> String {
    let file_name = format!(".AoC-{:04}-{:02}.tmp", year, day);
    let file = File::open(file_name);
    let mut result = String::new();
    if let Ok(mut f) = file {
        f.read_to_string(&mut result).expect("Unable to read file");
    } else {
        unimplemented!()
    }
    return result;
}

pub mod point {
    use std::ops::{Add, Sub};
    use std::fmt;

    #[derive(Clone, Copy, Eq, PartialEq, Hash)]
    pub struct Point {
        pub x: i32,
        pub y: i32,
    }

    impl Point {
        pub fn new(x: i32, y: i32) -> Point {
            Point { x, y }
        }

        pub fn from_str(text: &str) -> Point {
            let values = text.split(',').collect::<Vec<&str>>();
            Point::new(
                values[0].parse::<i32>().unwrap(),
                values[1].parse::<i32>().unwrap(),
            )
        }

        pub fn distance(self, to: Point) -> usize {
            ((self.x - to.x).abs() + (self.y - to.y).abs()) as usize
        }
    }

    impl Add for Point {
        type Output = Point;

        fn add(self, other: Point) -> Point {
            Point::new(self.x + other.x, self.y + other.y)
        }
    }

    impl Sub for Point {
        type Output = Point;

        fn sub(self, other: Point) -> Point {
            Point::new(self.x - other.x, self.y - other.y)
        }
    }

    impl fmt::Debug for Point {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            write!(f, "Point(x={}, y={})", self.x, self.y)
        }
    }

    pub fn directions() -> [Point; 4] { 
        [
            Point::new(0, 1),
            Point::new(0, -1),
            Point::new(1, 0),
            Point::new(-1, 0),
        ]
    }

    #[derive(Debug, Copy, Clone, Hash, Eq, PartialEq)]
    pub struct Point3d<T> {
        pub x: T,
        pub y: T,
        pub z: T,
    }

    pub trait Abs {
        fn abs_diff(&self, diff: &Self) -> usize;
    }

    impl Abs for usize {
        fn abs_diff(&self, diff: &Self) -> usize {
            if self < diff { diff - self } else { self - diff }
        }
    }

    impl Abs for i32 {
        fn abs_diff(&self, diff: &Self) -> usize {
            (self - diff).abs() as usize
        }
    }

    impl<T: Sub + Abs> Point3d<T> {
        pub fn new(x: T, y: T, z: T) -> Point3d<T> {
            Point3d { x, y, z }
        }
        
        pub fn distance(&self, to: &Point3d<T>) -> usize {
            (
                self.x.abs_diff(&to.x) +
                self.y.abs_diff(&to.y) +
                self.z.abs_diff(&to.z)
            ) as usize                
        }
    }

    impl<T: Abs + Sub + Add<Output=T>> Add for Point3d<T> {
        type Output = Self;

        fn add(self, other: Self) -> Self {
            Point3d::new(
                self.x + other.x,
                self.y + other.y, 
                self.z + other.z
            )
        }
    }

}

pub mod int_code_computer {
    type Args = [isize];

    enum Result {
        Value(isize),
        None,
        Done,
    }

    pub struct IntCodeFunc {
        func: &'static dyn Fn(&mut IntCodeComputer, &Args) -> Result,
        n_args: usize
    }

    pub struct IntCodeComputer {
        program: Vec<isize>,
        pointer: usize,
        pub done: bool,
        pub output: Vec<isize>,
        pub input: Vec<isize>,
    }

    impl IntCodeComputer {
        pub fn new(code: &Vec<isize>) -> Self {
            IntCodeComputer {
                program: code.clone(),
                pointer: 0,
                done: false,
                output: Vec::new(),
                input: Vec::new()
            }
        }

        pub fn step(&mut self) {
            let code = self.program[self.pointer] as usize;
            let func = IntCodeComputer::opcode(&code);
            let mut args: Vec<isize> = Vec::with_capacity(func.n_args);
            for i in 0..func.n_args {
                let arg = match ((code as isize) / 10_isize.pow((i+2) as u32)) % 10 {
                    1 => self.program[self.pointer+1+i],
                    0 => self.program[self.program[self.pointer+1+i] as usize],
                    _ => unimplemented!(),
                };
                args.push(arg);
            }
            self.pointer += 1+func.n_args;
            let result = (*func.func)(self, &args);
            match result {
                Result::Value(value) => {
                    let index = self.program[self.pointer] as usize;
                    self.program[index] = value;
                    self.pointer += 1;
                },
                Result::Done => self.done = true,
                Result::None => {},
            }
        }

        fn add(&mut self, args: &Args) -> Result {
            Result::Value(args[0] + args[1])
        }

        fn mult(&mut self, args: &Args) -> Result {
            Result::Value(args[0] * args[1])
        }

        fn done(&mut self, _: &Args) -> Result {
            Result::Done
        }

        fn input(&mut self, _: &Args) -> Result {
            Result::Value(self.input.pop().unwrap())
        }

        fn output(&mut self, args: &Args) -> Result {
            self.output.push(args[0]);
            Result::None
        }

        fn opcode(code: &usize) -> IntCodeFunc {
            match code % 100 {
                1 => IntCodeFunc { n_args: 2, func: &IntCodeComputer::add },
                2 => IntCodeFunc { n_args: 2, func: &IntCodeComputer::mult },
                3 => IntCodeFunc { n_args: 0, func: &IntCodeComputer::input },
                4 => IntCodeFunc { n_args: 1, func: &IntCodeComputer::output },
                99 => IntCodeFunc { n_args: 0, func: &IntCodeComputer::done},
                _ => unimplemented!(),
            }
        }
    }
}

