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
    
    def calculate_load(self, grid):
        load = 0
        for i in range(len(grid)):
            load += sum([1 for c in grid[i] if c == "O"]) * (len(grid) - i)
        return load

    def run(self, fin):
        grid = self.parse_input(fin)
        self.shift_rocks(grid)
        return self.calculate_load(grid)

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
