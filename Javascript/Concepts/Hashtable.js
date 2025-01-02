

const numbers = [2, 4, 67, 8, 44, 6, 12];

function LinearSearch(numbers, num) {
  for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] === num) {
      return i;
    }
  }
  return -1;
}

// console.log(LinearSearch(numbers, 6));

function BinarySearch(numbers, num) {
  let low = 0;
  let high = numbers.length - 1;

  while (low <= high) {
    let mid = Math.floor(low + (high - low) / 2);

    if (numbers[mid] === num) {
      return mid;
    } else if (numbers[mid < num]) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  return -1;
}

console.log(BinarySearch(numbers, 6));
