use clap::{App, Arg, ArgMatches};

pub const ARG_PASSWORDS_AMOUNT: &str = "pass-amount";
pub const ARG_OUTPUT_FILEPATH: &str = "out";

pub fn get_cli_matches() -> ArgMatches<'static> {
    App::new("password generator")
        .version("1.0")
        .author("Pavlo Myroniuk <pspos.developqkation@gmail.com>, Katia")
        .about("can generate new passwords and their hashes")
        .arg(
            Arg::new(ARG_PASSWORDS_AMOUNT)
                .help("specify amount of passwords to generate")
                .takes_value(true)
                .long(ARG_PASSWORDS_AMOUNT)
                .required(true),
        )
        .arg(
            Arg::new(ARG_OUTPUT_FILEPATH)
                .help("specify a filepath to save generated data")
                .takes_value(true)
                .long(ARG_OUTPUT_FILEPATH),
        )
        .get_matches()
}
