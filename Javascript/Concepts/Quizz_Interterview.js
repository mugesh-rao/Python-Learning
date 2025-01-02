function BinarySearch(arr, X) {
  let low = 0;
  let high = arr.length - 1;

  while (low <= high) {
    let mid = Math.floor((low + high) / 2);
    if (arr[mid] == X) {
      return mid;
    } else if (arr[mid] < X) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  return -1;
}

// console.log(BinarySearch([1, 5, 6, 7, 8, 9]), 8);

function ReverseString(str) {
  let left = 0;
  let right = str.length - 1;
  let arr = str.split("");

  while (left < right) {
    [arr[left], arr[right]] = [arr[right], arr[left]];
    left++;
    right--;
  }

  return arr.join("");
}

// console.log(ReverseString("Hello"));

function IsPallindrome(str) {
  let left = 0;
  let right = str.length - 1;
  let arr = str.split("");

  while (left < right) {
    if (arr[left] != arr[right]) {
      return false;
    }
    left++;
    right--;
  }

  return true;
}

// console.log(IsPallindrome("madam"));

function RemoveDuplicates(arr) {
  let output = [];
  let seen = {};

  for (let i = 0; i < arr.length; i++) {
    let current = arr[i];
    if (!seen[current]) {
      seen[current] = true;
      output.push(current);
    }
  }

  return output;
}

// console.log(RemoveDuplicates([1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 9, 10]));

function MaxProduct(arr1, arr2) {
  let maxProduct = 0;

  for (let i = 0; i < arr1.length; i++) {
    for (let j = 0; j < arr2.length; j++) {
      let product = arr1[i] * arr2[j];
      if (product > maxProduct) {
        maxProduct = product;
      }
    }
  }

  return maxProduct;
}

// console.log(MaxProduct([1, 2, 3], [4, 5, 6]));

function ReverseString(str) {
  let left = 0;
  let right = str.length - 1;
  let arr = str.split("");

  while (left < right) {
    [arr[left], arr[right]] = [arr[right], arr[left]];

    left++;
    right--;
  }

  console.log(arr);
}

// ReverseString("Hell0");

function FindSecondaryLargest(arr) {
  let largest = -Infinity;
  let secondLargest = -Infinity;

  for (let num of arr) {
    if (num > largest) {
      secondLargest = largest;
      largest = num;
    } else if (num > secondLargest && num !== largest) {
      secondLargest = num;
    }
  }
  
  return secondLargest === -Infinity ? null : secondLargest;
}

console.log(FindSecondaryLargest([1, 2, 3, 4, 5, 8]));
