import os
import sys

decompressed_folder = "./decompressed/"
compressed_folder = "./compressed/"

def validate_folders():
    if not os.path.isdir(decompressed_folder):
        os.mkdir(decompressed_folder)
    if not os.path.isdir(compressed_folder):
        os.mkdir(compressed_folder)

def open_binary(filename):
    with open(filename, "rb") as f:
        return f.read()

def save_file(filename, data):
    validate_folders()
    with open(filename, "wb") as f:
        f.write(data)

def parse_args():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <filename> <mode>")
        exit(1)
    return sys.argv[1], sys.argv[2]

def validate_args(filename, mode):
    mode = mode.lower()
    if mode not in ["compress", "decompress", "c", "d"]:
        print(f"Mode {mode} not supported")
        print("Supported modes: compress, decompress, c, d")
        exit(1)
    mode = mode[0]
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        exit(1)
    filename = filename.replace("\\", "/")
    if filename.endswith("/"):
        filename = filename[:-1]
    return filename, mode

def get_args():
    filename, mode = parse_args()
    filename, mode = validate_args(filename, mode)
    return filename, mode

def parse_filename(filename):
    filename = os.path.basename(filename)
    name, extension = os.path.splitext(filename)
    extension = extension[1:]
    return name, extension

def read_little_memory(data, size):
    return int.from_bytes(data[:size], byteorder="little")

def read_null_string_memory(data):
    return data[:data.index(b"\x00")].decode()

def make_folders(filename):
    file_path = os.path.dirname(filename)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

def fix_relative_path(filename):
    if filename.startswith(".."):
        return "_MAIN_" + filename[2:]
    return filename

def unfix_relative_path(filename):
    if filename.startswith("_MAIN_"):
        return ".." + filename[6:]
    return filename