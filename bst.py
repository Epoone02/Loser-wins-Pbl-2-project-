class BidNode:
    def __init__(self, name, bid):
        self.names = [name]
        self.bid = int(bid)
        self.right = None
        self.left = None

    def is_leaf(self):
        return self.right is None and self.left is None



Player = BidNode


class Bid_tree:
    def __init__(self):
        self.root = None # root of the tree


    def insert(self, name, bid):
        bid = int(bid)
        if self.root is None:
            self.root = BidNode(name, bid) # create root node
            return
        current = self.root
        while True:
            if bid == current.bid:
                current.names.append(name) # same bid → add player
                return
            elif bid > current.bid:
                if current.right is None:
                    current.right = BidNode(name, bid) # go right
                    break
                else:
                    current = current.right
            else:
                if current.left is None:
                    current.left = BidNode(name, bid) # go left
                    break
                else:
                    current = current.left

    def build_tree(self, liste):
        for item in liste:
            self.insert(item[0], item[1]) # insert all bids into the tree


    def in_order_recursive(self, node, nodes_list):
        if node is not None:
            self.in_order_recursive(node.left, nodes_list)
            nodes_list.append(node)
            self.in_order_recursive(node.right, nodes_list)

    def get_inorder_nodes(self):
        nodes = []
        self.in_order_recursive(self.root, nodes)
        return nodes # return nodes sorted by price


    def find_winner(self):
        for node in self.get_inorder_nodes():
            if len(node.names) == 1:
                return node # first unique price = winner
        return None


    def search(self, bid):
        bid = int(bid)
        current = self.root
        while current is not None:
            if bid == current.bid:
                return current # found
            elif bid > current.bid:
                current = current.right
            else:
                current = current.left
        return None


    def successor(self, bid): # find next higher price
        bid = int(bid)
        result = None
        current = self.root
        while current is not None:
            if current.bid > bid:
                result = current
                current = current.left
            else:
                current = current.right
        return result

    def predecessor(self, bid): # find next lower price
        bid = int(bid)
        result = None
        current = self.root
        while current is not None:
            if current.bid < bid:
                result = current
                current = current.right
            else:
                current = current.left
        return result

    def delete_recursive(self, node, bid):
        if node is None:
            return None
        if bid < node.bid:
            node.left = self.delete_recursive(node.left, bid)
        elif bid > node.bid:
            node.right = self.delete_recursive(node.right, bid)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_larger = self._min_node(node.right)
            node.bid = min_larger.bid
            node.names = min_larger.names
            node.right = self._delete_recursive(node.right, min_larger.bid)
        return node

    def delete(self, bid):
        self.root = self._delete_recursive(self.root, int(bid))

    def conditional_delete(self, bid):
        node = self.search(bid)
        if node and len(node.names) > 1:
            self.delete(bid)
            return True
        return False



    def total_bids(self): # count all bids
        return sum(len(node.names) for node in self.get_inorder_nodes())

    def price_distribution(self):
        return {node.bid: len(node.names) for node in self.get_inorder_nodes()}

    def seller_revenue(self, base_cost=1.0, alpha=49.0):
        total = 0.0
        for node in self.get_inorder_nodes():
            cost = base_cost + alpha / (node.bid + 1)
            total += cost * len(node.names)
        return total # compute total money earned

    def average_cost_per_player(self, base_cost=1.0, alpha=49.0):
        total_cost = 0.0
        total_bids = 0
        for node in self.get_inorder_nodes():
            cost = base_cost + alpha / (node.bid + 1)
            total_cost += cost * len(node.names)
            total_bids += len(node.names)
        return total_cost / total_bids if total_bids > 0 else 0.0 # average cost per player


    def depth_recursive(self, node): # compute tree height
        if node is None:
            return 0
        return 1 + max(self.depth_recursive(node.left), self.depth_recursive(node.right))

    def depth(self):
        return self.depth_recursive(self.root)

    def is_degenerate(self): # check if tree is like a linked list (bad case)
        n = len(self.get_inorder_nodes())
        return n > 0 and self.depth() == n
