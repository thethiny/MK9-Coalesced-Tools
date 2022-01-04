import zlib

def compress_data(data):
    return zlib.compress(data, 9)

def decompress_data(data):
    return zlib.decompress(data)

def parse_zlib_header(data):
    return data[4:]

def generate_zlib_header(data, size):
    return size.to_bytes(4, byteorder="little") + data

def sign_data(data):
    return bytes([
        ~x%256 for x in data
    ])