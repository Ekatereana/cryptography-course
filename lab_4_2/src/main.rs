use std::collections::HashMap;
use std::io::Write;
use std::sync::{Arc, Mutex};

fn read_file(filepath: &str) -> Vec<String> {
    std::fs::read_to_string(filepath)
        .unwrap()
        .split("\n")
        .map(|e| e.to_owned())
        .collect()
}

fn hash_with_md5(items: Vec<String>) -> HashMap<String, String> {
    items
        .into_iter()
        .map(|e| {
            (format!("{:x}", md5::compute(&e)), e)
        })
        .collect()
}

fn crack_md5() {
    let hashes = read_file("../md5.csv");
    let hashes_to_password = hash_with_md5(read_file("../top_passwords.txt"));

    let mut file_cracked = std::fs::File::create("md5_cracked.csv").unwrap();
    let mut file_rest = std::fs::File::create("md5_rest.csv").unwrap();
    for hash in hashes {
        match hashes_to_password.get(&hash) {
            Some(password) => {
                file_cracked.write(hash.as_bytes()).unwrap();
                file_cracked.write(&[44]).unwrap();
                file_cracked.write(password.as_bytes()).unwrap();
                file_cracked.write(&[0x0A]).unwrap();
            },
            None => {
                file_rest.write(hash.as_bytes()).unwrap();
                file_rest.write(&[0x0A]).unwrap();
            },
        }
    }
}

fn find_password_for_hash(hash: &str, passwords: &Vec<String>) -> Option<String> {
    for password in passwords {
        if bcrypt::verify(password, hash).unwrap() {
            return Some(password.to_owned());
        }
    }
    None
}

fn main() {
    // crack_md5();

    let hashes = read_file("../bcrypt.csv");
    let passwords = Arc::new(read_file("../top_passwords.txt"));

    let file_cracked = Arc::new(Mutex::new(std::fs::File::create("bcrypt_cracked.csv").unwrap()));
    let file_rest = Arc::new(Mutex::new(std::fs::File::create("bcrypt_rest.csv").unwrap()));

    let mut threads = Vec::new();
    for thread_hashes in hashes.chunks(3000) {
        let thread_hashes = thread_hashes.to_vec();

        let passwords = passwords.clone();
        let file_cracked = file_cracked.clone();
        let file_rest = file_rest.clone();

        threads.push(std::thread::spawn(move || {
            println!("thread started...");

            for hash in thread_hashes {
                match find_password_for_hash(&hash, &passwords) {
                    Some(password) => {
                        let mut f = file_cracked.lock().unwrap();
                        f.write(hash.as_bytes()).unwrap();
                        f.write(&[44]).unwrap();
                        f.write(password.as_bytes()).unwrap();
                        f.write(&[0x0A]).unwrap();
                    },
                    None => {
                        let mut f = file_rest.lock().unwrap();
                        f.write(hash.as_bytes()).unwrap();
                        f.write(&[0x0A]).unwrap();
                    },
                }
            }

            println!("thread finished!");
        }));
    }

    for thread in threads {
        thread.join().unwrap();
    }
}
