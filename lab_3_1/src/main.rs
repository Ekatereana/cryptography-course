use std::collections::HashMap;

fn hack_lcg() {
    println!("Start hacking...");
    let x1: i32 = 56979147;
    let x2: i32 = -1534233170;
    let x3: i32 = 1920942389;
    let x4: i32 = 520970512;

    let m: i64 = 2_i64.pow(32);
    for a in 2..m {
        let mut c = x2 as i64 - ((x1 as i64 * a) % m);
        if c < 0 {
            c += m;
        }
        let my_x2 = ((x1 as i64 * a + c) % m) as i32;
        let my_x3 = ((x2 as i64 * a + c) % m) as i32;
        let my_x4 = ((x3 as i64 * a + c) % m) as i32;
        if my_x2 == x2 && my_x3 == x3 && my_x4 == x4 {
            println!("a: {}; c: {};", a, c);
            println!("Goooood!");
            return;
        }
    }
    println!("Fuck :(");
}

fn create_account() {

}

#[tokio::main]
async fn main() {
    let resp = reqwest::get(format!("http://95.217.177.249/casino/createacc?id={}", 4731))
        .await.unwrap()
        .json::<HashMap<String, String>>()
        .await.unwrap()
        ;
    println!("{:?}", resp);
}

