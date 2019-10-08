from sys import platform
linux = platform == "linux"

# Define the colors we will use in RGB format
if linux:
    BLACK = 0
    WHITE = 1
else:
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)

BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
