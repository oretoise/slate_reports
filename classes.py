from datetime import datetime as dt

class Node:
    bin_name = None
    date_completed = None
    next = None
    prev = None
    list_data = []


    def __init__(self):
        # This node will split date and bin name into member data.
        pass
    

    def __str__(self):
        # Override default string representation to provide more information about the Node.
        return "Node:\n\tBin Name:%s\n\tDate:%s" % (self.bin_name, self.date_completed)


    def set_data_split(self, input):
        # Split the bin history item into the date and name members.
        self.date_completed, self.bin_name = input.split(' - ')

        # Strip any remaining whitespace from the date.
        self.date_completed = self.date_completed.strip()

        # Convert it to a datetime object.
        self.date_completed = dt.strptime(self.date_completed, '%m/%d/%Y')


class List:
    head = None
    key = ""
    tail = None


    def __init__(self, key):
        # Key is to know what type of application and therefore, which bin structure to validate against.
        self.key = key
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


    # not sure if this function is working as intended
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
        """ Give a printout of the linked list. """
        print("Key:", self.key)

        # Set our starting point: the head of the linked list.
        node = self.head

        # Loop until we reach the tail of the linked list.
        while node != self.tail:

            # Request the Node prinout.
            print(node)

            # Set our loop variable to the next node in the linked list.
            node = node.next


if __name__ == "__main__":
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node4 = Node()

    node1.list_data = ["this is node 1"]
    node2.list_data = ['this is node 2']
    node3.list_data = ['this is node 3']
    node4.list_data = ["this is node 4"]

    test_list = List("UG")

    test_list.append(node1)
    test_list.append(node2)
    test_list.append(node3)

    # this doesn't appear to be working
    test_list.insert_before(node4, None)

    test_list.display()