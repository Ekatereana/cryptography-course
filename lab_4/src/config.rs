use clap::{App, Arg, ArgMatches};

pub const ARG_PASSWORDS_AMOUNT: &str = "pass-amount";
pub const ARG_OUTPUT_FILEPATH: &str = "out";
pub const ARG_FILE_FORMAT: &str = "out-format";
pub const ARG_NOT_PRINT: &str = "not-print";
pub const ARG_HASH: &str = "hash";

pub fn get_cli_matches() -> ArgMatches<'static> {
    App::new("password generator")
        .version("1.0")
        .author("Pavlo Myroniuk <pspos.developqkation@gmail.com>, Ekatereana Gricaenko <ekatereanagricaenko@gmail.com>")
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
        .arg(
            Arg::new(ARG_FILE_FORMAT)
                .help("specify a file format for output file")
                .takes_value(true)
                .possible_values(vec!["csv"])
                .long(ARG_FILE_FORMAT)
                .requires(ARG_OUTPUT_FILEPATH)
        )
        .arg(
            Arg::new(ARG_NOT_PRINT)
                .help("do not print the generated data to stdout")
                .long(ARG_NOT_PRINT)
        )
        .arg(
            Arg::new(ARG_HASH)
                .help("specify hashing algorithms")
                .long(ARG_HASH)
                .takes_value(true)
                .multiple(true)
                .possible_values(vec!["sha256", "argon2", "bcrypt", "md5"])
        )
        .get_matches()
}
