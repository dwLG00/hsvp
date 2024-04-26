from src import interpreter
from src import load_img

if __name__ == '__main__':
    import sys
    image_src = sys.argv[1]
    instruction_array = load_img.load_image(image_src)

    program = interpreter.program(instruction_array.shape, instruction_array)
    for c in program.run_program():
        print(c, end='')
