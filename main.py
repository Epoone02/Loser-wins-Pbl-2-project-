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