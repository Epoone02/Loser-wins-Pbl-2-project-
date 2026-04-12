class BidNode:
    """A node in the BST. Stores one bid price and all players who placed that price."""
    def __init__(self, name, bid):
        self.names = [name]
        self.bid = int(bid)
        self.right = None
        self.left = None

    def is_leaf(self):
        return self.right is None and self.left is None


# Backward-compat alias
Player = BidNode


class Bid_tree:
    def __init__(self):
        self.root = None

    # ---------- Insertion ----------

    def insert(self, name, bid):
        bid = int(bid)
        if self.root is None:
            self.root = BidNode(name, bid)
            return
        current = self.root
        while True:
            if bid == current.bid:
                current.names.append(name)
                return
            elif bid > current.bid:
                if current.right is None:
                    current.right = BidNode(name, bid)
                    break
                else:
                    current = current.right
            else:
                if current.left is None:
                    current.left = BidNode(name, bid)
                    break
                else:
                    current = current.left

    def build_tree(self, liste):
        for item in liste:
            self.insert(item[0], item[1])

    # ---------- Traversal ----------

    def _in_order_recursive(self, node, nodes_list):
        if node is not None:
            self._in_order_recursive(node.left, nodes_list)
            nodes_list.append(node)
            self._in_order_recursive(node.right, nodes_list)

    def get_inorder_nodes(self):
        nodes = []
        self._in_order_recursive(self.root, nodes)
        return nodes

    # ---------- Winner ----------

    def find_winner(self):
        """Return the node with the lowest unique bid, or None if no unique bid."""
        for node in self.get_inorder_nodes():
            if len(node.names) == 1:
                return node
        return None

    # ---------- Search ----------

    def search(self, bid):
        """Return the node with the given bid, or None if not found."""
        bid = int(bid)
        current = self.root
        while current is not None:
            if bid == current.bid:
                return current
            elif bid > current.bid:
                current = current.right
            else:
                current = current.left
        return None

    # ---------- Successor & Predecessor ----------

    def successor(self, bid):
        """Return the node with the smallest bid strictly greater than `bid`."""
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

    def predecessor(self, bid):
        """Return the node with the largest bid strictly less than `bid`."""
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

    # ---------- Deletion ----------

    def _min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_recursive(self, node, bid):
        if node is None:
            return None
        if bid < node.bid:
            node.left = self._delete_recursive(node.left, bid)
        elif bid > node.bid:
            node.right = self._delete_recursive(node.right, bid)
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
        """Remove the node with the given bid from the tree."""
        self.root = self._delete_recursive(self.root, int(bid))

    def conditional_delete(self, bid):
        """Remove a node only if it has duplicate bids (not unique)."""
        node = self.search(bid)
        if node and len(node.names) > 1:
            self.delete(bid)
            return True
        return False

    # ---------- Analysis ----------

    def total_bids(self):
        """Total number of individual bids placed."""
        return sum(len(node.names) for node in self.get_inorder_nodes())

    def price_distribution(self):
        """Return a dict {price: count} for all bids."""
        return {node.bid: len(node.names) for node in self.get_inorder_nodes()}

    def seller_revenue(self, base_cost=1.0, alpha=49.0):
        """Calculate total seller revenue using the risk premium formula."""
        total = 0.0
        for node in self.get_inorder_nodes():
            cost = base_cost + alpha / (node.bid + 1)
            total += cost * len(node.names)
        return total

    def average_cost_per_player(self, base_cost=1.0, alpha=49.0):
        """Average cost paid per individual bid."""
        total_cost = 0.0
        total_bids = 0
        for node in self.get_inorder_nodes():
            cost = base_cost + alpha / (node.bid + 1)
            total_cost += cost * len(node.names)
            total_bids += len(node.names)
        return total_cost / total_bids if total_bids > 0 else 0.0

    # ---------- Tree metrics (degeneration analysis) ----------

    def _depth_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._depth_recursive(node.left), self._depth_recursive(node.right))

    def depth(self):
        """
        Return the height of the BST (longest root-to-leaf path).

        Average case O(log n) for random input, worst case O(n) when
        insertions are sorted — the tree degenerates into a linked list.
        """
        return self._depth_recursive(self.root)

    def is_degenerate(self):
        """Return True if the tree is fully degenerate (depth == number of nodes)."""
        n = len(self.get_inorder_nodes())
        return n > 0 and self.depth() == n
