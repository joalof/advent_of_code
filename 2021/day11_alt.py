import numpy as np
from scipy.ndimage import correlate


def parse_input(file_path="./input_day11.txt"):
    """Reads the height map and adds some padding. """
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        grid = np.zeros((len(lines), len(lines[0])), dtype=int)
        for i, line in enumerate(lines):
            grid[i, :] = [int(c) for c in line]
    return grid


class OctopusGrid:
    def __init__(self, grid):
        self.grid = grid
        self.total_flashes = 0
        self.recent_flashes = 0
        self.kernel = np.ones((3, 3), dtype=int)
        self.kernel[1, 1] = 0

    def step(self, num=1):
        for i in range(num):

            self.grid += 1

            ind_flash_new = self.grid > 9
            ind_flash = np.zeros_like(ind_flash_new)

            while np.sum(ind_flash_new) > 0:
                self.grid[ind_flash_new] = 0
                ind_flash |= ind_flash_new

                # when an octopus flashes the energy of all neighbors increases by one
                delta_energy = correlate(ind_flash_new.astype(int), self.kernel, mode='constant', cval=0)

                delta_energy[ind_flash] = 0
                self.grid += delta_energy
                ind_flash_new = self.grid > 9

    @property
    def size(self):
        return self.grid.size

    def view(self):
        print(self.grid)


if __name__ == '__main__':
    grid = parse_input('./test.txt')
    og = OctopusGrid(grid.copy())

    # Part I 
    og.step(2)
    og.view()

    # Part II
    # og = OctopusGrid(grid)
    # num_step = 0
    # while og.recent_flashes < og.size:
    #     og.step()
    #     num_step += 1
    # print(num_step)
