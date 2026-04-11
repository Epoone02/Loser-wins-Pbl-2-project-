import csv


class Player:
    def __init__(self, name, bid):
        self.names = [name]
        self.bid = int(bid)
        self.right = None
        self.left = None

    def is_leaf(self):
        return self.right is None and self.left is None


class Bid_tree:
    def __init__(self):
        self.root = None

    def insert(self, name, bid):
        bid = int(bid)
        if self.root is None:
            self.root = Player(name, bid)
            return
        current = self.root
        while True:
            if bid == current.bid:
                current.names.append(name)                       
                return
            elif bid > current.bid:
                if current.right is None:
                    current.right = Player(name, bid)
                    break
                else:
                    current = current.right
            else:
                if current.left is None:
                    current.left = Player(name, bid)
                    break
                else:
                    current = current.left

    def build_tree(self, liste):
        for item in liste:
            self.insert(item[0], item[1])

    def _in_order_recursive(self, node, nodes_list):
        if node is not None:
            self._in_order_recursive(node.left, nodes_list)
            nodes_list.append(node)
            self._in_order_recursive(node.right, nodes_list)

    def get_inorder_nodes(self):
        nodes = []
        self._in_order_recursive(self.root, nodes)
        return nodes


def load_bid(file):
    bid_list = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                bid_list.append(row)
    return bid_list


bid = load_bid('APP_lowbid_data\lowbid_stress_200k.csv')
tree1 = Bid_tree()
tree1.build_tree(bid)



