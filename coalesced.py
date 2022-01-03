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
    data = compress_data(data)
    data = generate_zlib_header(data)
    return data

def extract_coalesced(filename):
    original_name, extension = parse_filename(filename)
    decompressed_data = decompress_coalesced(filename)
    save_file(f"{decompressed_folder}{original_name}.{extension}", decompressed_data)
    flags = {}
    for file_name, file_data, flag in read_coalesced(decompressed_data):
        file_path = os.path.join(decompressed_folder, file_name)
        make_folders(file_path)
        save_file(file_path, file_data)
        flags[file_name] = flag

def read_coalesced(data):
    package_flag = read_little_memory(data, 4)
    data = data[4:]
    
    while data:
        flag = read_little_memory(data, 4)
        data = data[4:]
        file_name = read_null_string_memory(data)
        data = data[len(file_name) + 1:]
        file_size = read_little_memory(data, 4)
        data = data[4:]
        file_data = data[:file_size]
        data = data[file_size:]
        yield file_name, file_data, flag

    


    
# if mode == "c":
#     compressed_data = compress_coalesced(filename)
#     save_file(f"{compressed_folder}{original_name}.{extension}", compressed_data)
#     return