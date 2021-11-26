use tabled::{Table, Tabled};

pub fn print_passwords(passwords: &Vec<String>) {
    println!("{}", Table::new(passwords).to_string());
}
