from os import listdir, walk
from os.path import isfile

class BufferIO:

    def write_buf(filename : str, buffer : bytes):
        with open(filename, 'wb') as fp:
            fp.write(buffer)

    def read_buf(filename : str):
        with open(filename, 'rb') as fp:
            return fp.read()

def main():
    sprite_sheet_bytes = b''
    sprite_path = './output'
    for file in listdir(sprite_path):
        full_path = f'{sprite_path}/{file}' 
        if isfile(full_path):
            sprite_sheet_bytes += BufferIO.read_buf(full_path)
    
    print(f'spritesheet len bytes: {len(sprite_sheet_bytes)}')
    BufferIO.write_buf(f'{sprite_path}/spritesheet.bin', sprite_sheet_bytes)


if __name__ == "__main__":
    main()