# This is an example of how to visualize, as bitmap images, certain tester inputs/outputs
# You need to install python modules numpy and pillow to be able to use this code

from PIL import Image       # don't change this line
import numpy                # don't change this line
from test_inputs import *   # this line is only needed if you want to visualize tester inputs
from test_outputs import *  # this line is only needed if you want to visualize tester outputs

# in this example we use tester input gray_image_5
# alternatively, you can visualize a certain tester output, e.g. img_data = fill_5.output
# or, you can replace it with your own list_of_lists, e.g. img_data = [[1,2,3],[4,5,6], [7,8,9]]
img_data = gray_image_5.input

# this line creates a grayscale image
# replace 'L' with 'RGB' if img_data holds a color image instead
img = Image.fromarray(numpy.asarray(img_data).astype(numpy.uint8), 'L')

# optional -- this line saves the image as a bitmap file in your disk
img.save('output_5.bmp')

# optional -- this line throws a window that displays the image
img.show()
