#! /usr/bin/env python3
from Node import Node

codes = {}


def calculate_probability(data: str) -> dict:
    """ Calculate probability of occurence of each symbol in the given data"""
    probability = {}
    for symbol in data:
        if symbol not in probability:
            probability[symbol] = 1
        else:
            probability[symbol] += 1
    return probability


def calculate_codes(node: Node, val="") -> dict:
    """ Calculate encoding code for each symbol """
    newVal = val + str(node.code)

    if node.left:
        calculate_codes(node.left, newVal)
    if node.right:
        calculate_codes(node.right, newVal)

    if not node.left and not node.right:
        codes[node.symbol] = newVal

    return codes


def huffman_encoding(data: str):
    """ Encode the given data using huffman encoding """
    symbol_with_prob_dict = calculate_probability(data)
    nodes = []
    for symbol in symbol_with_prob_dict:
        nodes.append(Node(symbol, symbol_with_prob_dict[symbol]))

    print(nodes)
