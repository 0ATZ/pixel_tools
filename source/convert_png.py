from PIL import Image
from struct import pack

RED_MASK = 0xFF0000
GREEN_MASK = 0x00FF00
BLUE_MASK = 0x0000FF
TRANSPARENT = 0xF81F

def Color_24bit_to_16bit(color : int):
    red   = (color & RED_MASK) >> 16
    green = (color & GREEN_MASK) >> 8
    blue  = (color & BLUE_MASK)
    color_16bit = (red >> 3) << 11| (green >> 2) << 5 | (blue >> 3)
    # print(hex(color_16bit))
    return color_16bit
    
def Color_Tuple_to_16bit(color : tuple):
    if color[3] == 0:
        return TRANSPARENT
    red = (color[0] >> 3) & 0x1F
    green = (color[1] >> 2) & 0x3F 
    blue  = (color[2] >> 3) & 0x1F
    color_16bit = red << 11 | green << 5 | blue
    return color_16bit
    
    
def convert_sprite(row, col, num_cols, width, height):

    # skip all the pixels of the previous rows
    # row offset = row number times pixels per row
    row_offset = row * (num_cols*width*height)
    
    # skip all the pixels of the previous cols
    # col offset = column number times pixels per col
    col_offset = col * width

    # row_offset + col_offset gives the start position 
    # need to add another offset to jump to the next line 
    # after each row of sprite pixels
    offset = 0
    
    for px_index in range(width*height):
        
        index = (row_offset)+(col_offset)+px_index+offset
        
        # val = '#' if pixels[index] == 1 else '_'
        # print(f'{val} ', end='')
        
        # write the converted pixel to the file
        yield index
        
        # this is the last sprite pixel in this line 
        if (px_index % width) == (width - 1): 
            # add another offset to go to the next line of pixels for this sprite
            offset += (width * (num_cols - 1))


# Open the PNG image pixel format is (RED, GREEN, BLUE, ALPHA)
image = Image.open("C:/Josh/aseprite/josh/cursor32.png")

# Get the width, height, and pixel bytes
width, height = image.size
print(width, height)
pixels = list(image.getdata())

count = 0
with open('../../aaa_game_engine/assets/sprites/cursors.bin', 'wb') as fp:
    num_rows = 1
    num_cols = 3
    width = 32
    height = 32
    
    for row in range(num_rows):
        for col in range(num_cols):            
            for index in convert_sprite(row, col, num_cols, width, height):
                converted_color = Color_Tuple_to_16bit(pixels[index])
                print(f'{hex(converted_color)} ', end='')
                if index % 32 == 31:
                    print()
                fp.write(pack('@H', converted_color))
                count += 1
    
print('pixel count: ', count)
