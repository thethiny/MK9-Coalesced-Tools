from utils import *
from data_modifiers import *


def decompress_coalesced(filename):
    compressed_data = open_binary(filename)
    compressed_data = parse_zlib_header(compressed_data)
    decompressed_data = decompress_data(compressed_data)
    decompressed_data = sign_data(decompressed_data)
    return decompressed_data

def compress_coalesced(filename):
    data = open_binary(filename)
    data = sign_data(data)
    data_size = len(data)
    data = compress_data(data)
    data = generate_zlib_header(data, data_size)
    return data

def extract_coalesced(filename):
    original_name, extension = parse_filename(filename)
    decompressed_data = decompress_coalesced(filename)
    save_file(f"{decompressed_folder}{original_name}.{extension}", decompressed_data)
    for file_name, file_data in read_coalesced(decompressed_data):
        file_name = fix_relative_path(file_name)
        file_path = os.path.join(decompressed_folder, f"{filename}.out", file_name)
        make_folders(file_path)
        save_file(file_path, file_data)

def read_coalesced(data):
    files_count = read_little_memory(data, 4)//2
    data = data[4:]

    print(f"Reading {files_count} files")
    
    for i in range(files_count):
        name_length = read_little_memory(data, 4)
        data = data[4:]
        file_name = data[:name_length].strip(b"\x00").decode()
        data = data[name_length:]
        file_size = read_little_memory(data, 4)
        data = data[4:]
        file_data = data[:file_size]
        data = data[file_size:]
        print(f"{i+1}/{files_count} - {file_name} ({file_size} bytes)")
        yield file_name, file_data

def create_coalesced_data(filename: str, filepath: str):
    data = open_binary(os.path.join(filepath, filename))
    filename = unfix_relative_path(filename)
    filename = filename.replace("/", "\\")
    data_size = len(data)
    name_length = len(filename) +1
    data_size_bytes = int.to_bytes(data_size, 4, byteorder="little")
    name_length_bytes = int.to_bytes(name_length, 4, byteorder="little")
    data = name_length_bytes + filename.encode() + b"\x00" + data_size_bytes + data
    print(f"{filename} ({data_size} bytes)")
    return data

def repack_coalesced(foldername):
    folder_path, folder_base = foldername.replace("\\", "/").rsplit("/", 1)
    if folder_base.endswith(".out"):
        folder_base = folder_base[:-4]
    repack_files = []
    for root, dirs, files in os.walk(foldername):
        root = root.replace("\\", "/").split(foldername, 1)[1].strip('/')
        for file in files:
            repack_files.append(os.path.join(root, file))

    print(f"Repacking {len(repack_files)} files")

    files_count = len(repack_files) * 2
    files_count = int.to_bytes(files_count, 4, byteorder="little")

    out_file_name = os.path.join(compressed_folder, folder_base)
    uncompressed_name = out_file_name + ".uncompressed"

    with open(uncompressed_name, "wb") as f:
        f.write(files_count)
        for file in repack_files:
            data = create_coalesced_data(file, foldername)
            f.write(data)       

    data = compress_coalesced(uncompressed_name)
    save_file(f"{out_file_name}", data)