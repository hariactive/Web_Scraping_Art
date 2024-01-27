from PIL import Image

# Open the cropped image file
image = Image.open('image_1_cropped.png')

# Convert the image to RGBA mode (if not already in RGBA)
image = image.convert("RGBA")

# Define a copyright symbol as a simple white square (you can replace this with your symbol)
symbol_size = 50  # Adjust the size of the symbol
symbol = Image.new('RGBA', (symbol_size, symbol_size), color=(255, 255, 255, 150))  # White square as an example

# Get the size of the image
width, height = image.size

# Define the position to place the watermark (bottom right corner)
position = (width - symbol_size, height - symbol_size)

# Paste the watermark onto the image
image.paste(symbol, position, symbol)

# Save the modified image as final.png
image.save('final.png')
