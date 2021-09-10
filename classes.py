from datetime import datetime as dt

class Node:
    bin_name = None
    date_completed = None
    next = None
    prev = None
    list_data = []

    def __init__(self):
        # This node will split date and bin name into member data
        pass

    def set_data_split(self, input):
        self.date_completed, self.bin_name = input.split(' - ')
        self.date_completed = self.date_completed.strip()
        self.date_completed = dt.strptime(self.date_completed, '%m/%d/%Y')

    def set_next(self, input_node):
        self.next = input_node

class List:
    head = None
    tail = None
    def __init__(self):
        pass

    def prepend(self, input):
        if self.head == None:
            self.head = input
            self.tail = input
        else:
            self.head.prev = input
            input.next = self.head
            self.head = input

    def append(self, input):
        if self.tail == None:
            self.tail = input
            self.head = input
        else:
            input.prev = self.tail
            self.tail.next = input
            self.tail = input

    def insert_before(self, node , tmp):
        if tmp == self.head or self.head == None:
            self.prepend(node)
            return
        if self.tail != None and tmp == None:
            self.append(node)
            return
        
        node.next = tmp
        node.prev = tmp.prev
        tmp.prev.next = node
        tmp.prev = node

    def display(self):
        tmp = self.head

        while tmp!=None:
            print(tmp.date_completed)
            tmp = tmp.next

if __name__ == "__main__":
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node4 = Node()

    node1.list_data = ["this is node 1"]
    node2.list_data = ['this is node 2']
    node3.list_data = ['this is node 3']
    node4.list_data = ["this is node 4"]

    test_list = List()

    test_list.append(node1)
    test_list.append(node2)
    test_list.append(node3)
    test_list.insert_before(node4, None)

    test_list.display()


    



    
