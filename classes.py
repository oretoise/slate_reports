class Node:
    bin_name = None
    date_completed = None
    next = None
    list_data = []

    def __init__(self):
        # This node will split date and bin name into member data
        pass

    def set_data_split(self, input):
        self.bin_name, self.date_completed = input.split(' - ')

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
            input.next = self.head
            self.head = input

    def append(self, input):
        if self.tail == None:
            self.tail = input
            self.head = input
        else:
            self.tail.next = input
            self.tail = input



if __name__ == "__main__":
    node1 = Node()
    node2 = Node()
    node3 = Node()

    node1.set_data_split("hello - bye bye")
    node2.set_data_split("1 - 2")
    node3.list_data = [1, 2, 3, 4, 5]

    test_list = List()

    test_list.append(node1)
    test_list.prepend(node2)
    test_list.append(node3)

    print(test_list.tail.list_data[4])
    print(test_list.head.bin_name)
    print(test_list.head.next.date_completed)



    
