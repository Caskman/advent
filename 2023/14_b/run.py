from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        lines = [list(line) for line in fin.read().split("\n")]
        return lines
    
    def shift_rocks(self, grid):
        for col in range(len(grid[0])):
            cur = 0
            for row in range(len(grid)):
                if grid[row][col] == "#":
                    cur = row + 1
                elif grid[row][col] == "O":
                    if cur == row:
                        cur += 1
                    else:
                        grid[cur][col] = "O"
                        grid[row][col] = "."
                        cur += 1
        return grid
    
    def turn_grid_right(self, grid):
        new_grid = []
        for j in range(len(grid[0])):
            row = []
            for i in range(len(grid)-1, -1, -1):
                row.append(grid[i][j])
            new_grid.append(row)
        return new_grid
                

    def spin_grid(self, grid):
        for i in range(4):
            grid = self.shift_rocks(grid)
            grid = self.turn_grid_right(grid)
        return grid

    def calculate_load(self, grid):
        load = 0
        for i in range(len(grid)):
            load += sum([1 for c in grid[i] if c == "O"]) * (len(grid) - i)
        return load

    def hash_grid(self, grid):
        return "\n".join(["".join([c for c in row]) for row in grid])

    def unhash_grid(self, hash):
        return [list(line) for line in hash.split("\n")]

    def run(self, fin):
        grid = self.parse_input(fin)
        grid_step_map = {}
        step_grid_map = {}

        cycle_start, cycle_end = None, None
        for i in range(1, 1_000_000_000 + 1):
            grid = self.spin_grid(grid)
            hash = self.hash_grid(grid)
            if hash in grid_step_map:
                cycle_start, cycle_end = grid_step_map[hash], i
                # start 2 end 6
                # period 4
                # last step is 10
                # (last_step - end) % period
                # (10 - 6) % 4 = 0
                # so final state would be start + 0 so first step
                period = cycle_end - cycle_start
                offset = (1_000_000_000 - cycle_end) % period
                final_state_step = cycle_start + offset
                final_hash = step_grid_map[final_state_step]
                final_state = self.unhash_grid(final_hash)
                return self.calculate_load(final_state)
            else:
                grid_step_map[hash] = i
                step_grid_map[i] = hash
        
if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    # case_markers = ["1"]
    # case_markers = ["1","2","3"]
    
    for marker in sorted(case_markers):
        answer_path = f"answer_{marker}.txt"
        if not os.path.isfile(answer_path):
            continue
        with open(answer_path, "r") as fin:
            answer = fin.read()
        input_path = f"input_{marker}.txt"
        with open(input_path, "r") as fin:
            output = Solution().run(fin)
            success = str(answer) == str(output)
            success_message = "\u2705" if success else "\u274C"
            print(f"#{marker}\t{success_message} Expected: {answer}\tActual: {output}")
