#! /usr/bin/env python3
from sys import byteorder
import os
from Node import Node
from bitstring import BitArray, BitStream
import pickle
from db import *

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


def bit_string_to_byte_file(data: str, filepath: str) -> str:
    """
    Parameters: encoded string, filepath string.
    Convert bits string to bytes and write to a binary file
    Returns: binary file output path and txt nodes file path
    """

    output_bytes = BitArray(bin=data)

    extension_index = filepath.index(".txt")
    dirpath = filepath[:extension_index]
    outputpath = dirpath + "_encoded.bin"
    nodespath = dirpath + "_nodes.bin"

    with open(outputpath, "wb") as file:
        file.write(output_bytes.tobytes())

    return outputpath, nodespath


def byte_file_to_bits_str(filepath: str) -> str:
    """
    Convert binary file's content and returning that as string
    """
    bytes = BitArray(filename=filepath)
    return bytes.bin


def decoded_str_to_file(decoded_string: str, filename: str):
    with open(filename + "_decoded.txt", "w") as file:
        file.write(decoded_string)

    outputpath = filename + "_decoded.txt"
    return outputpath


def create_huffman_tree(nodes: list) -> list:
    """create huffman tree to the root from list of leaf nodes"""
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

    return nodes[0]


def huffman_encoding(data: str):
    """Encode the given data using huffman encoding"""
    symbol_with_prob = calculate_probability(data)
    nodes = []
    for symbol in symbol_with_prob:
        nodes.append(Node(symbol_with_prob[symbol], symbol))

    list_of_nodes = [(node.symbol, node.prob) for node in nodes]
    conn = connect()
    delete(conn)
    insert(conn, list_of_nodes)
    close(conn)

    huffman_tree = create_huffman_tree(nodes)

    # Menggunakan nodes[0] karena hanya tersisa satu node (yaitu root) dalam nodes list
    symbol_with_code = calculate_codes(huffman_tree)
    output_encoded_str = output_encoded(data, symbol_with_code)
    before_compression, after_compression = total_gain(
        data, symbol_with_code, symbol_with_prob
    )

    return (
        output_encoded_str,
        symbol_with_code,
        symbol_with_prob,
        before_compression,
        after_compression,
        huffman_tree,
    )


def huffman_decoding(encoded_data: str, huffman_tree: Node):
    tree_head = huffman_tree
    decoded_output = []

    for x in encoded_data:
        if x == "1":
            huffman_tree = huffman_tree.right
        elif x == "0":
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    string = "".join([str(item) for item in decoded_output])
    return string
