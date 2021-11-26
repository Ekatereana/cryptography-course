use rand::rngs::ThreadRng;
use rand::{thread_rng, Rng};

const ALPHABET: [char; 79] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '0', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=',
    '+', '/', '|',
];
const DEFAULT_PASSWORD_LEN: usize = 12;

pub struct PasswordGenerator {
    rand: ThreadRng,
    common: Vec<String>,
}

impl PasswordGenerator {
    pub fn new(common_passwords: &str) -> Self {
        PasswordGenerator {
            rand: thread_rng(),
            common: std::fs::read_to_string(common_passwords)
                .expect(&format!("unable to read the file {}", common_passwords))
                .split("\n")
                .map(|p| p.trim().to_owned())
                .collect(),
        }
    }

    fn generate_random_password(&mut self) -> String {
        let alphabet_len = ALPHABET.len();
        (0..(DEFAULT_PASSWORD_LEN + self.rand.gen::<usize>() % 7))
            .map::<char, _>(|_| ALPHABET[self.rand.gen::<usize>() % alphabet_len])
            .collect::<String>()
    }

    fn generate_humanlike_password(&mut self) -> String {
        String::from("")
    }

    fn generate_password(&mut self) -> String {
        match self.rand.gen::<u16>() % 1000 {
            0..=100 => self.generate_random_password(),
            101..=800 => self.common[self.rand.gen::<usize>() % self.common.len()].clone(),
            _ => "".to_owned(),
        }
    }

    pub fn generate_passwords(&mut self, amount: usize) -> Vec<String> {
        (1..amount)
            .map(|_| self.generate_password())
            .collect::<Vec<String>>()
    }
}
