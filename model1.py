class Client:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None
        
    def select_a_case(self):
        
        
    def __str__(self):
        return self.value
        
class Queue:
    def __init__(self, head : Node):
        self.head = head
        self.tail : Node = head
        self.length = 1
    
    def append_node(self, node : Node):
        if self.tail == None:
            self.head = node
            self.tail = node
            self.length += 1
        else:
            self.tail.next = node
            self.tail = node
            self.length += 1
    
    def dequeue(self):
        if self.head != None:
            print(self.head.value)
            popped = self.head
            self.head = self.head.next
            self.length -= 1
            return popped
        else:
            print('Queue is empty')
    
    def size(self):
        print(f'Current length of the queue is {self.length}')
        
    def front(self):
        if self.head != None:
            print(f'Current front is {self.head.value}')
        else:
            print('Queue is empty')
    
    def __str__(self):
        listOfNodes = []
        if self.head == None:
            return 'Queue is empty :('
        else:
            current = self.head
            while current:
                listOfNodes.append(str(current.value))
                current = current.next
            return ', '.join(listOfNodes)
