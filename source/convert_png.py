from PIL import Image
from struct import pack

RED_MASK = 0xFF0000
GREEN_MASK = 0x00FF00
BLUE_MASK = 0x0000FF

def Color_24bit_to_16bit(color):
    red   = (color & RED_MASK) >> 16
    green = (color & GREEN_MASK) >> 8
    blue  = (color & BLUE_MASK)
    color_16bit = (red >> 3) << 11| (green >> 2) << 5 | (blue >> 3)
    # print(hex(color_16bit))
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
        yield colors[pixels[index]]
        
        # this is the last sprite pixel in this line 
        if (px_index % width) == (width - 1): 
            # add another offset to go to the next line of pixels for this sprite
            offset += (width * (num_cols - 1))
            # print()
    

colors = {
    1  : 0x222034,
    4  : 0x8f563b,
    9  : 0x99e550,
    10 : 0x6abe30,
    11 : 0x37946e,
    12 : 0x4b692f,
    14 : 0x323c39,
    21 : 0xffffff,
    24 : 0x696a6a,
}

# convert to RGB565
for index, color in colors.items():
    colors[index] = Color_24bit_to_16bit(color)

# Open the PNG image
image = Image.open("C:/Josh/josh-grass-Sheet-Sheet.png")

# Get the width, height, and pixel bytes
width, height = image.size
print(width, height)
pixels = list(image.getdata())

count = 0
with open('../output/grass_sprites.bin', 'wb') as fp:
    num_rows = 6
    num_cols = 6
    width = 16
    height = 16
    
    for row in range(num_rows):
        for col in range(num_cols):            
            for px in convert_sprite(row, col, num_cols, width, height):
                fp.write(pack('@H', px))
                count += 1
    
print('pixel count: ', count)
