use rand_chacha::rand_core::{RngCore, SeedableRng};
use rand_chacha::ChaCha20Rng;
use std::collections::HashMap;
use sha2::Digest;

pub const PLAIN: &str = "plain";
pub const SHA256: &str = "sha256";
pub const MD5: &str = "md5";
pub const ARGON2: &str = "argon2";
pub const BCRYPT: &str = "bcrypt";

fn format_argon2_hash(hash: String) -> String {
    let parts = hash.split("$").collect::<Vec<_>>();
    format!("${}${}", parts[4], parts[5])
}

fn hash_password(
    pass: &str,
    algos: &Vec<&str>,
    generator: &mut ChaCha20Rng,
) -> HashMap<&'static str, String> {
    let mut hashes = HashMap::new();
    hashes.insert(PLAIN, pass.to_owned());
    for algo in algos {
        let (algo, hash) = match algo {
            &MD5 => (MD5, format!("{:x}", md5::compute(pass.as_bytes()))),
            &SHA256 => (SHA256, {
                let mut hasher = sha2::Sha256::new();
                hasher.update(pass.as_bytes());
                format!("{:x}", hasher.finalize())
            }),
            &ARGON2 => (
                ARGON2,
                format_argon2_hash(argon2::hash_encoded(
                    pass.as_bytes(),
                    &(0..15)
                        .map(|_| (generator.next_u32() % 256) as u8)
                        .collect::<Vec<_>>(),
                    &argon2::Config::default(),
                )
                .unwrap()),
            ),
            // bcrypt::hash will generate the salt by itself
            &BCRYPT => (BCRYPT, bcrypt::hash(pass, 8).unwrap()),
            _ => panic!(
                "Hashing algorithm {} is not supported. See --help for more information.",
                algo
            ),
        };
        hashes.insert(algo, hash);
    }
    hashes
}

pub fn hash_passwords(
    passwords: &Vec<String>,
    algorithms: &Vec<&str>,
) -> Vec<HashMap<&'static str, String>> {
    let mut generator = rand_chacha::ChaCha20Rng::from_seed([
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9,
        1, 1,
    ]);
    passwords
        .into_iter()
        .map(|p| hash_password(p, algorithms, &mut generator))
        .collect()
}
