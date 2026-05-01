# Rust AoC Cheatsheet

## Project Setup

```bash
cargo new day01
cd day01
```

For regex and other common deps, add to `Cargo.toml`:

```toml
[dependencies]
regex = "1"
itertools = "0.13"
```

---

## Reading Input

```rust
use std::fs;

fn main() {
    let input = fs::read_to_string("input.txt").unwrap();

    // Lines as iterator
    for line in input.lines() { }

    // Collect into Vec
    let lines: Vec<&str> = input.lines().collect();
}
```

---

## Parsing Numbers

```rust
// Parse a single number
let n: i64 = "42".parse().unwrap();

// Parse all numbers from a line of space-separated values
let nums: Vec<i64> = line
    .split_whitespace()
    .map(|s| s.parse().unwrap())
    .collect();

// Parse a grid of single digits
let grid: Vec<Vec<u32>> = input
    .lines()
    .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
    .collect();
```

---

## Regex

```rust
use regex::Regex;

let re = Regex::new(r"(\d+),(\d+)").unwrap();

// Find first match
if let Some(caps) = re.captures(line) {
    let x: i64 = caps[1].parse().unwrap();
    let y: i64 = caps[2].parse().unwrap();
}

// Find all matches in a string
for caps in re.captures_iter(input) {
    let x: i64 = caps[1].parse().unwrap();
}

// Named captures
let re = Regex::new(r"(?P<x>\d+),(?P<y>\d+)").unwrap();
let x = &caps["x"];
```

---

## Splitting and Parsing Structured Lines

```rust
// "Alice: 10 20 30"
let (name, rest) = line.split_once(": ").unwrap();
let nums: Vec<i64> = rest.split(' ').map(|s| s.parse().unwrap()).collect();

// Split input into sections separated by blank lines
let sections: Vec<&str> = input.split("\n\n").collect();
```

---

## HashMap and HashSet

```rust
use std::collections::{HashMap, HashSet};

// Frequency count
let mut freq: HashMap<char, usize> = HashMap::new();
for c in line.chars() {
    *freq.entry(c).or_insert(0) += 1;
}

// Check membership
let mut seen: HashSet<(i32, i32)> = HashSet::new();
seen.insert((x, y));
if seen.contains(&(x, y)) { }
```

---

## 2D Grids

```rust
// Parse into Vec<Vec<char>>
let grid: Vec<Vec<char>> = input
    .lines()
    .map(|l| l.chars().collect())
    .collect();

let rows = grid.len();
let cols = grid[0].len();

// 4-directional neighbors
let dirs: [(i32, i32); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];
for (dr, dc) in dirs {
    let nr = r as i32 + dr;
    let nc = c as i32 + dc;
    if nr >= 0 && nc >= 0 && nr < rows as i32 && nc < cols as i32 {
        let neighbor = grid[nr as usize][nc as usize];
    }
}

// 8-directional (includes diagonals)
let dirs: [(i32, i32); 8] = [
    (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)
];
```

---

## BFS / Shortest Path

```rust
use std::collections::{HashMap, VecDeque};

fn bfs(grid: &Vec<Vec<char>>, start: (usize, usize)) -> HashMap<(usize, usize), usize> {
    let mut dist = HashMap::new();
    let mut queue = VecDeque::new();
    dist.insert(start, 0);
    queue.push_back(start);

    while let Some((r, c)) = queue.pop_front() {
        let d = dist[&(r, c)];
        for (dr, dc) in [(0i32,1),(0,-1),(1,0),(-1,0)] {
            let nr = r as i32 + dr;
            let nc = c as i32 + dc;
            if nr < 0 || nc < 0 { continue; }
            let next = (nr as usize, nc as usize);
            if grid[next.0][next.1] == '#' { continue; }
            if !dist.contains_key(&next) {
                dist.insert(next, d + 1);
                queue.push_back(next);
            }
        }
    }
    dist
}
```

## Dijkstra / Weighted Shortest Path

```rust
use std::collections::{BinaryHeap, HashMap};
use std::cmp::Reverse;

// BinaryHeap is a max-heap; wrap in Reverse for min-heap
let mut heap: BinaryHeap<Reverse<(usize, (usize, usize))>> = BinaryHeap::new();
let mut dist: HashMap<(usize, usize), usize> = HashMap::new();

heap.push(Reverse((0, start)));
while let Some(Reverse((cost, node))) = heap.pop() {
    if dist.contains_key(&node) { continue; }
    dist.insert(node, cost);
    for neighbor in neighbors(node) {
        let new_cost = cost + edge_weight;
        if !dist.contains_key(&neighbor) {
            heap.push(Reverse((new_cost, neighbor)));
        }
    }
}
```

---

## Useful Iterators

```rust
use itertools::Itertools;

// All pairs
for (a, b) in items.iter().tuple_combinations() { }

// Permutations
for perm in items.iter().permutations(items.len()) { }

// Cartesian product (nested loops)
for (x, y) in (0..5).cartesian_product(0..5) { }

// Chunk lines into groups of N
for chunk in lines.chunks(3) { }

// Min/max of a collection
let max = nums.iter().copied().max().unwrap();

// Sum / product
let total: i64 = nums.iter().sum();
let product: i64 = nums.iter().product();

// Enumerate with index
for (i, line) in input.lines().enumerate() { }

// Zip two iterators
for (a, b) in xs.iter().zip(ys.iter()) { }

// Windows / sliding window
for window in nums.windows(3) { // window is &[T] of len 3
    let sum: i64 = window.iter().sum();
}
```

---

## Sorting and Deduplication

```rust
let mut v = vec![3, 1, 4, 1, 5];
v.sort();
v.dedup(); // removes consecutive duplicates (sort first)

// Sort by custom key
v.sort_by_key(|&x| std::cmp::Reverse(x)); // descending

// Sort structs
structs.sort_by(|a, b| a.value.cmp(&b.value));
```

---

## Ranges and Intervals

```rust
// Inclusive range
for i in 0..=10 { }

// Check overlap: [a,b] and [c,d] overlap when a <= d && c <= b
fn overlaps(a: i64, b: i64, c: i64, d: i64) -> bool {
    a <= d && c <= b
}

// Check containment: [c,d] fully inside [a,b]
fn contains(a: i64, b: i64, c: i64, d: i64) -> bool {
    a <= c && d <= b
}
```

---

## Common Number Tricks

```rust
// GCD / LCM
fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}
fn lcm(a: u64, b: u64) -> u64 {
    a / gcd(a, b) * b
}

// LCM of a list (for cycle detection)
let result = nums.iter().copied().fold(1u64, lcm);

// Integer square root (check if n is a perfect square)
let sqrt = (n as f64).sqrt() as u64;
let is_square = sqrt * sqrt == n;

// Modular arithmetic (keep positive)
let r = ((x % m) + m) % m;
```

---

## Structs and Enums for AoC

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn neighbors(&self) -> impl Iterator<Item = Point> + '_ {
        [(0i32,1),(0,-1),(1,0),(-1,0)].iter().map(move |&(dx, dy)| Point {
            x: self.x + dx,
            y: self.y + dy,
        })
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Dir { North, South, East, West }

impl Dir {
    fn turn_right(self) -> Dir {
        match self { Dir::North => Dir::East, Dir::East => Dir::South,
                     Dir::South => Dir::West, Dir::West => Dir::North }
    }
    fn delta(self) -> (i32, i32) {
        match self { Dir::North => (-1,0), Dir::South => (1,0),
                     Dir::East => (0,1),  Dir::West => (0,-1) }
    }
}
```

---

## Memoization / Caching with HashMap

```rust
use std::collections::HashMap;

fn solve(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {
    if let Some(&cached) = memo.get(&n) { return cached; }
    let result = if n == 0 {
        1
    } else {
        solve(n - 1, memo) + solve(n - 2, memo)
    };
    memo.insert(n, result);
    result
}

// Call with:
let mut memo = HashMap::new();
println!("{}", solve(50, &mut memo));
```

---

## Printing Debug Output

```rust
// Debug-print any type that derives Debug
println!("{:?}", my_vec);
println!("{:#?}", my_struct); // pretty-printed

// Conditional debug output
if cfg!(debug_assertions) {
    eprintln!("grid: {:?}", grid);
}
```

---

## Tips

- Use `i64` or `i32` for most numbers; `usize` for indexing.
- `.unwrap()` is fine for AoC — don't over-engineer error handling.
- `clippy` (`cargo clippy`) catches many common mistakes.
- Part 1 and Part 2 often share parsing — put it in a `parse(input: &str)` function.
- When in doubt, `#[derive(Debug, Clone, PartialEq, Eq, Hash)]` on your types.
