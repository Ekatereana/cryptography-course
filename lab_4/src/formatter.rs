use prettytable::{Cell, Row, Table};
use std::collections::HashMap;

fn to_csv(data: &Vec<HashMap<&str, String>>, order: Vec<&str>) -> String {
    let mut header: String = order.join(",");
    header.push('\n');
    header.push_str(
        &data
            .iter()
            .map(|r| {
                let mut res = Vec::new();
                for key in order.iter() {
                    res.push(r.get(key).unwrap().to_owned());
                }
                res.join(",")
            })
            .collect::<Vec<String>>()
            .join("\n"),
    );
    header
}

pub fn write_to_file(data: &Vec<HashMap<&str, String>>, filepath: &str, format: Option<&str>) {
    let formatter = if let Some(format) = format {
        match format {
            "csv" => to_csv,
            _ => panic!(
                "File format {} is not supported. Use --help for more information",
                format
            ),
        }
    } else {
        to_csv
    };
    let order = data[0].keys().map(|e| e.to_owned()).collect::<Vec<_>>();
    std::fs::write(filepath, formatter(data, order))
        .expect(&format!("Unable to write result into {}:", filepath));
}

pub fn print_passwords(passwords: &Vec<HashMap<&str, String>>) {
    let mut table = Table::new();
    let keys = passwords[0]
        .keys()
        .map(|e| e.to_owned())
        .collect::<Vec<_>>();
    table.add_row(Row::new(keys.iter().map(|e| Cell::new(e)).collect()));
    for row in passwords {
        table.add_row(Row::new(
            keys.iter()
                .map(|e| Cell::new(row.get(e).unwrap()))
                .collect(),
        ));
    }
    table.printstd();
}
