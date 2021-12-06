#! /usr/bin/env python3
from Node import Node

codes = {}


def calculate_probability(data: str) -> dict:
    """Calculate probability of occurence of each symbol in the given data"""
    probability = {}
    for symbol in data:
        if symbol not in probability:
            probability[symbol] = 1
        else:
            probability[symbol] += 1
    return probability


def calculate_codes(node: Node, val="") -> dict:
    """Calculate encoding code for each symbol"""
    newVal = val + str(node.code)

    if node.left:
        calculate_codes(node.left, newVal)
    if node.right:
        calculate_codes(node.right, newVal)

    if not node.left and not node.right:
        codes[node.symbol] = newVal

    return codes


def output_encoded(data: str, symbol_with_code: dict) -> str:
    """Print full encoded string"""
    strList = []
    for character in data:
        strList.append(symbol_with_code[character])

    joinedStr = "".join(strList)
    return joinedStr


def total_gain(data: str, symbol_with_code: dict, symbol_with_prob: dict):
    """Compare total bits before and after compression"""
    before_compression = len(data) * 8
    after_compression = 0

    for symbol in symbol_with_code:
        after_compression += len(symbol_with_code[symbol]) * symbol_with_prob[symbol]

    return before_compression, after_compression


def huffman_encoding(data: str):
    """Encode the given data using huffman encoding"""
    symbol_with_prob = calculate_probability(data)
    print("FREQUENCY FOR EACH CHARACTER: ")
    print(symbol_with_prob)
    nodes = []
    for symbol in symbol_with_prob:
        nodes.append(Node(symbol_with_prob[symbol], symbol))

    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.prob)
        right = nodes[0]
        left = nodes[1]

        right.code = 1
        left.code = 0

        newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    # Menggunakan nodes[0] karena hanya tersisa satu node (yaitu root) dalam nodes list
    symbols_with_code = calculate_codes(nodes[0])
    print("CODE FOR EACH CHARACTER: ")
    print(symbols_with_code)
    output_encoded_str = output_encoded(data, symbols_with_code)
    print("FULL ENCODED STRING: ")
    print(output_encoded_str)
    before_compression, after_compression = total_gain(
        data, symbols_with_code, symbol_with_prob
    )
    print("Before Compression: {} bits".format(before_compression))
    print("After compression: {} bits".format(after_compression))


def main():
    data = input("Masukkan String: ")
    huffman_encoding(data)


main()
