from PIL import Image
import numpy as np
from .helper import tupsum, tupprod

class Program:
    def __init__(self, size, instructions):
        self.size = size
        self.instructions = instructions
        self.memory = np.zeros(size, dtype=int)
        self.instruction_pointer = (0, 0)
        self.register_pointer = (0, 0)
        # given in R^2
        self.instruction_direction = (1, 0)
        self.register_direction = (1, 0)

    def run_program(self, debug=False):
        while not self.out_of_bounds(self.instruction_pointer):
            px, py = self.instruction_pointer
            color, S, V = self.instructions[:, px, py]

            if debug:
                print('ip: %s' % (self.instruction_pointer,))
                print('id: %s' % (self.instruction_direction,))
                print('rp: %s' % (self.register_pointer,))
                print('rd: %s' % (self.register_direction,))
                print('hsv: %s' % ((color, S, V),))

            if color == 0: #red
                self.memory[*self.register_pointer] = (self.memory[*self.register_pointer] + S) % 255
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 1: #yellow
                self.register_pointer = tupsum(self.register_pointer, tupprod(S, self.register_direction))
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 2: #green
                idx, idy = self.instruction_direction
                self.instruction_direction = (-idy, idx)
                self.memory[*self.register_pointer] = (self.memory[*self.register_pointer] + S) % 255
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 3: #cyan
                rdx, rdy = self.register_direction
                self.register_direction = (-rdy, rdx)
                self.memory[*self.register_pointer] = (self.memory[*self.register_pointer] + S) % 255
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 4: #blue
                idx, idy = self.instruction_direction
                memory_value = self.memory[*self.register_pointer]
                if memory_value < S:
                    self.instruction_direction = (idy, -idx)
                if memory_value > S:
                    self.instruction_direction = (-idy, idx)
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 5: #magenta
                memory_value = self.memory[*self.register_pointer]
                yield memory_value
                self.register_pointer = tupsum(self.register_pointer, tupprod(S, self.register_direction))
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if self.out_of_bounds(self.register_pointer):
                raise MemoryError('Memory register out of bounds!')

    def out_of_bounds(self, pointer):
        if pointer[0] >= self.size[0] or pointer[0] < 0: return True
        if pointer[1] >= self.size[1] or pointer[1] < 0: return True
        return False

