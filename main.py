import csv
import streamlit as st

class Player:
    def __init__(self, name, bid):
        self.name = name
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
                self.root = self.delete(current.bid, self.root)                           
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

    def minBST(self):
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return [current.name, current.bid]

    def maxBST(self):
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return [current.name, current.bid]

    def delete(self, bid, node):         
         
        if node is None:
            return None
        if bid < node.bid:
            node.left = self.delete(bid, node.left)
        elif bid > node.bid:
            node.right = self.delete(bid, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                name, bid2, node.left = self.suppmax(node.left)
                node.name, node.bid = name, bid2
        return node

    def suppmax(self, node):
        if node.right is None:
            return node.name, node.bid, node.left
        name, bid, node.right = self.suppmax(node.right)
        return name, bid, node


def load_bid(file):
    bid_list = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                bid_list.append(row)
    return bid_list


bid = load_bid('Loser-wins-Pbl-2-project-/APP_lowbid_data/lowbid_stress_200k.csv')
tree1 = Bid_tree()
tree1.build_tree(bid)



