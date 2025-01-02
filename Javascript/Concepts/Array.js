const arr1 = [10, 20, 30, 40, 50, 100];
const arr2 = [11, 21, 31, 41, 51, 101];

const exists = arr1.includes(20);

const found = arr1.find((value) => value > 40);

function reverseArray(arr) {
  let start = 0,
    end = arr.length - 1;

  while (start < end) {
    [arr[start], arr[end]] = [arr[end], arr[start]];
    start++;
    end--;
  }
  return arr;
}

// Example
//   console.log(reverseArray(arr1));

function mergeSortedArrays(arr1, arr2) {
  let mergered = [];
  let i = 0,
    j = 0;
  while (i < arr1.length && j < arr2.length) {
    if (arr1[i] < arr2[j]) {
      mergered.push(arr1[i]);
      i++;
    } else {
      mergered.push(arr2[j]);
      j++;
    }
  }
  return mergered.concat(arr1.slice(i).concat(arr2.slice(j)));
}

// console.log(mergeSortedArrays(arr1, arr2));

function MaxProduct(arr) {
  arr.sort((a, b) => b - a);
  console.log(arr[0], arr[1]);
  return arr[0] * arr[1];
}
// console.log(MaxProduct(arr1, arr2));

function FindMaxMin(arr) {
  let max = arr[0];
  let min = arr[0];
  for (let i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
      max = arr[i];
    } else if (arr[i] < min) {
      min = arr[i];
    }
  }
  return { max, min };
}
// console.log(FindMaxMin(arr1))

function Find2Largest(arr) {
  for (let i = 0; i < arr.length; i++) {
    if (i < arr[i]) {
      console.log(arr[i] - 1);
    }
  }
}

// console.log(Find2Largest(arr1))




