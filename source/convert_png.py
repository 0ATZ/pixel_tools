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
    

colors = {
    1  : 0x222034,
    4  : 0x8f563b,
    9  : 0x99e550,
    10 : 0x6abe30,
    11 : 0x37946e,
    12 : 0x4b692f,
    14 : 0x323c39,
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
    width_px = 16
    height_px = 16
    
    for row in range(num_rows):
        for col in range(num_cols):
            for y in range(height_px):
                for x in range(width_px):
                    start_index = (col * width_px) + (row*width_px*num_cols)
                    i = start_index + x + (y*width_px*num_cols)
                    print(f'{i:04} ', end='')
                    if i % 16 == 15:
                        print()
                    fp.write(pack('@H', colors[pixels[i]]))
                    count += 1
    
print('pixel count: ', count)
