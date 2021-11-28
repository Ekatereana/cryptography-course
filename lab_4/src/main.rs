use std::collections::HashMap;
use std::iter::FromIterator;

mod config;
mod formatter;
mod generator;
mod hasher;

fn main() {
    let matches = config::get_cli_matches();
    if let Some(amount) = matches.value_of(config::ARG_PASSWORDS_AMOUNT) {
        let n = amount
            .parse::<usize>()
            .expect("expect valid integer literal");

        let passwords = generator::generate_passwords(n);

        let data = if matches.is_present(config::ARG_HASH) {
            hasher::hash_passwords(
                passwords,
                matches
                    .values_of(config::ARG_HASH)
                    .unwrap()
                    .into_iter()
                    .map(|e| e.to_owned())
                    .collect(),
            )
        } else {
            passwords
                .into_iter()
                .map(|s| HashMap::from_iter(vec![("password", s)].into_iter()))
                .collect()
        };

        if !matches.is_present(config::ARG_NOT_PRINT) {
            formatter::print_passwords(&data);
        }

        if let Some(filepath) = matches.value_of(config::ARG_OUTPUT_FILEPATH) {
            formatter::write_to_file(&data, filepath, matches.value_of(config::ARG_FILE_FORMAT));
        }
    }
}
