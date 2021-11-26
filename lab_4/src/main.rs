use crate::formatter::print_passwords;
use crate::generator::PasswordGenerator;

mod config;
mod formatter;
mod generator;

fn main() {
    let matches = config::get_cli_matches();
    if let Some(amount) = matches.value_of(config::ARG_PASSWORDS_AMOUNT) {
        let n = amount
            .parse::<usize>()
            .expect("expect valid integer literal");

        let mut password_generator = generator::PasswordGenerator::new("top_passwords.txt");
        let passwords = password_generator.generate_passwords(n);

        formatter::print_passwords(&passwords);

        if let Some(filepath) = matches.value_of(config::ARG_OUTPUT_FILEPATH) {}
    } else {
        println!("Nothing to do :(");
    }
}
