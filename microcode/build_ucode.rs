use std::fs;

fn main() {
    let contents = fs::read_to_string("bwb_opcodes.txt")
        .expect("Something went wrong with reading the file");

    let lines: Vec<&str> = contents
        .lines()
        .collect::<&str>()
        .map(|s| s.trim())
        .filter(|s| !s.contains("#") && !s.is_empty());

    // for s in contents.lines() {
    //     if s.contains("#") {
    //         continue;
    //     }
    //     let sp = s.trim();
    //     if sp.is_empty() {
    //         continue;
    //     }
    //     println!("{}", sp);
    // }
}