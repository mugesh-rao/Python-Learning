const everyone = ["Gill", "marlin", "Blloat", "nemo"];

function FindNemo(array) {
  let t0 = performance.now();
  for (let i = 0; i < array.length; i++) {
    if (array[i] === "nemo") {
      console.log("Found Nemo");
      break;
    }
  }
  let t1 = performance.now();
  console.log(t1 - t0 + " Milliseconds");
}
const FindNemo2 = array =>{
  array.forEach(i => {
    if (i === "nemo") {
      console.log("Found Nemo")
    }
  })
}
// FindNemo2(everyone);



const number = [1, 2, 3, 4];

function logPairs(array) {
  for (let i = 0; i < array.length; i++) {
    for (let j = 0; j < array.length; j++) {
      console.log(array[i], array[j]);
    }
  }
}

// logPairs(number) //O(n^2)

function SumAllNums(nums) {
  nums.forEach((a) => {
    console.log(a);
  });
  console.log("-------------");
  nums.forEach((a) => {
    nums.forEach((b) => {
      console.log(a + b);
    });
  });
}

// SumAllNums([1, 2, 3, 4]);

function Broo(n) {
  for (let i = 0; i < n.length; i++) {
    console.log("Boo");
  }
}

// Broo([1, 2, 3]);

function HiNArray(n) {
  let msg = [];

  for (let i = 0; i < n; i++) {
    msg[i] = 'Hello';
  }
  console.log(msg)
}

// HiNArray(5)

