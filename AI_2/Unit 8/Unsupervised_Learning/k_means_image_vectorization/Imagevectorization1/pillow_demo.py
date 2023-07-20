import urllib.request
import io
from PIL import Image

URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyObEHVIMF5dEXqJCuEqjd0r0MRiShqqBUfg:x-raw-image:///297a9c3b253f37d5e21ee9dd2e4c7575b2c14fd2057dea990ea459da8cd74d83&usqp=CAU'
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
img = Image.open(f) # You can also use this on a local file; just put the local filename in quotes in place of f.
img.show() # Send the image to your OS to be displayed as a temporary file
print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.
img.show() # Now, you should see a single white pixel near the upper left corner
img.save("my_image.png") # Save the resulting image. Alter your filename as necessary.