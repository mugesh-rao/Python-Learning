function SquareStarPatter(n) {
  for (i = 0; i < n; i++) {
    console.log("*".repeat(n));
  }
}
// SquareStarPatter(13);

function HolloSquarePatter(n) {
  for (let i = 0; i < n; i++) {
    if (i === 0 || i === n - 1) {
      console.log("*".repeat(n));
    } else {
      console.log("*" + " ".repeat(n - 2) + "*");
    }
  }
}
// HolloSquarePatter(12)

function InvertedPyramid(n) {
  for (let i = n; i > 0; i--) {
    console.log("*".repeat(i));
  }
}
// InvertedPyramid(10)

function StarPyramid(n) {
  for (let i = 1; i <= n; i++) {
    let spaces = " ".repeat(n - 1);
    let stars = "*".repeat(2 * i - 1);
    console.log(spaces + stars);
  }
}
// StarPyramid(4)

function ButterflyStar(n) {
  for (let i = 1; i <= n; i++) {
    // Left wing
    let row = "*".repeat(i);

    // Spaces in the middle
    row += " ".repeat(2 * (n - i));

    // Right wing
    row += "*".repeat(i);

    console.log(row);
  }

  for (let i = n - 1; i >= 1; i--) {
        // Left wing
        let row = "*".repeat(i);

        // Spaces in the middle
        row += " ".repeat(2 * (n - i));

        // Right wing
        row += "*".repeat(i);

        console.log(row);
    }

}

// ButterflyStar(4)

function DownWardTriangle(n) {
  for (let i = 0; i < n ; i++) {
    const element = array[i];
    
  }
}
