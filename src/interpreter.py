from PIL import Image
import numpy as np
from helper import tupsum, tupprod

class Program:
    def __init__(self, size, instructions):
        self.size = size
        self.instructions = instructions
        self.memory = np.zeros(size)
        self.instruction_pointer = (0, 0)
        self.register_pointer = (0, 0)
        # given in R^2
        self.instruction_direction = (1, 0)
        self.register_direction = (1, 0)

    def run_program(self):
        while not self.out_of_bounds(self.instruction_pointer):
            px, py = self.instruction_pointer
            color, S, V = self.instructions[px][py]

            if color == 'R':
                self.memory[*self.register_pointer] = (self.memory[*self.register_pointer] + S) % 255
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 'Y':
                self.register_pointer = tupsum(self.register_pointer, tupprod(S, self.register_direction))
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 'G':
                idx, idy = self.instruction_direction
                self.instruction_direction = (idy, -idx)
                self.memory[*self.register_pointer] = (self.memory[*self.register_pointer] + S) % 255
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 'C':
                rdx, rdy = self.register_direction
                self.register_direction = (rdy, -rdx)

            if color == 'B':
                idx, idy = self.instruction_direction
                memory_value = self.memory[*self.register_pointer]
                if memory_value < S:
                    self.instruction_direction = (-idy, idx)
                if memory_value > S:
                    self.instruction_direction = (idy, -idx)
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if color == 'M':
                memory_value = self.memory[*self.register_pointer]
                yield memory_value
                self.register_pointer = tupsum(self.register_pointer, tupprod(S, self.register_direction))
                self.instruction_pointer = tupsum(self.instruction_pointer, tupprod(V, self.instruction_direction))

            if self.out_of_bounds(self.register_pointer):
                raise MemoryError('Memory register out of bounds!')

    def out_of_bounds(self, pointer):
        if pointer[0] >= self.size[0] or pointer[0] < 0: return True
        if poitner[1] >= self.size[1] or pointer[1] < 0: return True
        return False

