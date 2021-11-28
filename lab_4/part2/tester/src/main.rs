use rand::rngs::ThreadRng;
use rand::Rng;

const ALPHABET: [char; 84] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '0', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=',
    '+', '/', '|', '?', '<', '>', ':', ';',
];

fn generate_random_pass(len: usize, random: &mut ThreadRng) -> String {
    (0..len).map(|_| ALPHABET[random.gen::<usize>() % ALPHABET.len()]).collect()
}

fn hash(pass: &str, salt: &str) -> String {
    format!("{:x}", md5::compute(format!("{}{}", pass, salt)))
}

fn main() {
    let mut rand = rand::thread_rng();
    for _ in 0..10 {
        let pass = generate_random_pass(16, &mut rand);
        let hash = hash(&pass, "24326124313124416d444943717a4d7a302f56345269312f764b6a444f");
        println!("{} {}", pass, hash);
    }
}
