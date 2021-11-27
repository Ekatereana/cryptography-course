use rand::rngs::ThreadRng;
use rand::{thread_rng, Rng};

const ALPHABET: [char; 85] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '0', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=',
    '+', '/', '|', ',', '?', '<', '>', ':', ';',
];
const DEFAULT_PASSWORD_LEN: usize = 12;

pub struct PasswordGenerator {
    rand: ThreadRng,
    common: Vec<String>,
    dictionary: Vec<String>,
}

fn read_file(filepath: &str) -> Vec<String> {
    std::fs::read_to_string(filepath)
        .expect(&format!("unable to read the file {}", filepath))
        .split("\n")
        .map(|p| p.trim().to_owned())
        .collect()
}

impl PasswordGenerator {
    pub fn new(common_passwords: &str, dictionary: &str) -> Self {
        PasswordGenerator {
            rand: thread_rng(),
            common: read_file(common_passwords),
            dictionary: read_file(dictionary),
        }
    }

    fn generate_random_password(&mut self) -> String {
        let alphabet_len = ALPHABET.len();
        (0..(DEFAULT_PASSWORD_LEN + self.rand.gen::<usize>() % 7))
            .map::<char, _>(|_| ALPHABET[self.rand.gen::<usize>() % alphabet_len])
            .collect::<String>()
    }

    fn map_char(&mut self, c: char) -> char {
        match c {
            'o' | 'O' => '0',
            'e' | 'E' => '3',
            ' ' => ALPHABET[62 + self.rand.gen::<usize>() % 8],
            _ => c,
        }
    }

    fn generate_humanlike_password(&mut self) -> String {
        let mut res_password = String::new();
        while res_password.len() < 12 {
            res_password
                .push_str(&self.dictionary[self.rand.gen::<usize>() % self.dictionary.len()]);
            res_password.push(' ');
        }
        res_password
            .trim()
            .chars()
            .map(|c| self.map_char(c))
            .collect::<String>()
            .replace("ch", "4")
    }

    fn generate_password(&mut self) -> String {
        match self.rand.gen::<u16>() % 1000 {
            0..=100 => self.generate_random_password(),
            101..=700 => self.common[self.rand.gen::<usize>() % self.common.len()].clone(),
            _ => self.generate_humanlike_password(),
        }
    }

    pub fn generate_passwords(&mut self, amount: usize) -> Vec<String> {
        (1..=amount)
            .map(|_| self.generate_password())
            .collect::<Vec<String>>()
    }
}
