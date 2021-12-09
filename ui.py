from math import e
import PySimpleGUI as ui
from utility import *
import os
from db import *
from Node import Node


layout = [
    [
        ui.Text("Browse txt file: "),
        ui.In(size=(25, 1), enable_events=True, key="-FILE-"),
        ui.FileBrowse(),
    ],
    [ui.Text("", key="-ERROR-")],
    [],
    [
        ui.Button(button_text="Encode", enable_events=True, key="-ENCODE-"),
        ui.Button(button_text="Decode", enable_events=True, key="-DECODE-"),
    ],
    [ui.Text("", key="-PROCESS-")],
    [ui.Text("", key="-OUTPUT-")],
    [ui.HorizontalSeparator()],
    [ui.Text("", key="-BITS-")],
    [ui.Text("", key="-SIZE-")],
]

window = ui.Window(title="Huffman Encoder", layout=layout, size=(700, 350))

# Program still running or has not yet terminated
while True:
    event, values = window.read()
    # program terminated
    if event == "Exit" or event == ui.WIN_CLOSED:
        break

    elif event == "-ENCODE-":
        filepath = values["-FILE-"]
        try:
            window["-ERROR-"].update("")
            window["-PROCESS-"].update("")
            window["-OUTPUT-"].update("")
            window["-BITS-"].update("")
            window["-SIZE-"].update("")

            with open(filepath) as file:
                input_string = "".join(file.readlines())

            (
                output_encoded_str,
                symbol_with_code,
                symbol_with_prob,
                before_compression,
                after_compression,
                node,
            ) = huffman_encoding(input_string)

            outputpath, nodespath = bit_string_to_byte_file(
                output_encoded_str, filepath
            )

            outputsize = os.path.getsize(outputpath)
            inputsize = os.path.getsize(filepath)

            window["-PROCESS-"].update("Encoding process succeeded")
            window["-OUTPUT-"].update(f"compressed file at :\n{outputpath}")
            window["-BITS-"].update(
                f"NUMBER OF BIT\nbefore compression: {before_compression} bits\nafter compression: {after_compression} bits."
            )
            window["-SIZE-"].update(
                f"FILE SIZE\nbefore compression: {inputsize} bytes\nafter compression: {outputsize} bytes"
            )

        except Exception as e:
            window["-ERROR-"].update(f"ERROR: {e}")
            window["-PROCESS-"].update("")
            window["-OUTPUT-"].update("")
            window["-BITS-"].update("")
            window["-SIZE-"].update("")

    elif event == "-DECODE-":
        filepath = values["-FILE-"]
        filename = filepath[: filepath.index("_encoded.bin")]
        try:
            window["-ERROR-"].update("")
            window["-PROCESS-"].update("")
            window["-OUTPUT-"].update("")
            window["-BITS-"].update("")
            window["-SIZE-"].update("")

            bits_string = byte_file_to_bits_str(filepath)
            conn = connect()
            rows = fetch(conn)
            close(conn)

            nodes = [Node(row[2], row[1]) for row in rows]
            huffman_tree = create_huffman_tree(nodes)
            decoded_string = huffman_decoding(bits_string, huffman_tree)
            outputpath = decoded_str_to_file(decoded_string, filename)

            inputsize = os.path.getsize(filepath)
            outputsize = os.path.getsize(outputpath)

            window["-PROCESS-"].update("Decoding process succeeded")
            window["-OUTPUT-"].update(f"decompressed file at :\n{outputpath}")
            window["-SIZE-"].update(
                f"FILE SIZE\nbefore decompression: {inputsize} bytes\nafter decompression: {outputsize} bytes"
            )

        except Exception as e:
            window["-ERROR-"].update(f"ERROR: {e}")
            window["-PROCESS-"].update("")
            window["-OUTPUT-"].update("")
            window["-BITS-"].update("")
            window["-SIZE-"].update("")


window.close()
