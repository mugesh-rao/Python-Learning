function createNode(data) {
  return {
    data: data,
    next: null,
  };
}

function CreateLinkedList() {
  let head = null;

  function insert(data) {
    const newNode = createNode(data);

    if (!head) {
      head = newNode;
    } else {
      let current = head;
      while (current.next) {
        current = current.next;
      }
      current.next = newNode;
    }
  }

  function Display() {
   let current =head
   const result = []
   
  }
}
