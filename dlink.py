class dlink_node(object):

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class dlink(object):

    def __init__(self):
        self.head = dlink_node(None)

    def add_data(self, data):
        node = dlink_node(data)
        node.prev = self.head
        node.next = self.head.next
        self.head.next = node
