from PIL import Image

def load_image(src):
    image = Image.open(src)
    hsvize = image.convert('HSV')
    width, height = hsvize.size

    instruction_array = np.zeros((width, height), dtype=(int, 3))
    pixels = hsvize.load()
    for i in range(width):
        for j in range(height):
            H, S, V = pixels[i, j]
            Hue = H / 255 * 359
            if 0 <= Hue < 60:
                C = 0 #red
            elif 60 <= Hue < 120:
                C = 1 #yellow
            elif 120 <= Hue < 180:
                C = 2 #green
            elif 180 <= Hue < 240:
                C = 3 #cyan
            elif 240 <= Hue < 300:
                C = 4 #blue
            elif 300 <= Hue < 360:
                C = 5 #magenta
            instruction_array[i, j] = (C, S, V)

    return instruction_array
