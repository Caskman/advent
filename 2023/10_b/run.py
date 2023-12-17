from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque

class Solution:
    def parse_input(self, fin) -> None:
        grid = [list(l) for l in fin.read().split("\n")]
        self.grid = grid
        self.N = len(grid)
        self.M = len(grid[0])
        edges = defaultdict(list)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != ".":
                    self.add_edge(edges, i, j)
        return grid, edges

    dirs = {
        "up": set([
            "|",
            "7",
            "F",
            "S",
        ]),
        "down": set([
            "|",
            "L",
            "J",
            "S",
        ]),
        "left": set([
            "-",
            "L",
            "F",
            "S",
        ]),
        "right": set([
            "-",
            "7",
            "J",
            "S",
        ]),
    }

    possible_directions = {
        "|": set([
            "up",
            "down",
        ]),
        "-": set([
            "left",
            "right",
        ]),
        "7": set([
            "left",
            "down",
        ]),
        "J": set([
            "left",
            "up",
        ]),
        "F": set([
            "right",
            "down",
        ]),
        "L": set([
            "up",
            "right",
        ]),
        "S": set([
            "up",
            "down",
            "left",
            "right",
        ]),
    }

    def add_edge(self, edges, i, j):
        transforms = [
            (-1,0,"up"),
            (1,0,"down"),
            (0,-1,"left"),
            (0,1,"right"),
        ]

        for tx,ty,d in transforms:
            x, y = i + tx, j + ty
            if self.is_valid(x, y) and self.is_adj(i, j, d, x, y):
                edges[(i,j)].append((x, y))

    def is_valid(self, i, j):
        return i >= 0 and j >= 0 and i < self.N and j < self.M
    
    def is_adj(self, x, y, d, i, j):
        tile = self.grid[x][y]
        other = self.grid[i][j]
        available_directions = self.possible_directions[tile]
        if d not in available_directions:
            return False
        return other in self.dirs[d]

    def find_loop_tiles(self, edges, grid):
        start = None
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "S":
                    start = (i,j)
                    break
        
        stack = []
        path = []
        visited = set()

        stack.append([start, None, edges[start]])
        while stack:
            node, prev, neighbors = stack[-1]

            if prev and node == start:
                break
            if node in visited:
                stack.pop()
                continue

            visited.add(node)
            path.append(node)
            if stack[-1][2]:
                neighbor = stack[-1][2].pop()
                if neighbor == prev:
                    neighbor = stack[-1][2].pop()
                stack.append([neighbor, node, edges[neighbor]])
            else:
                visited.remove(node)
                path.pop()
                stack.pop()

        return set(path)

    def clear_all_but(self, grid, loop_tiles):
        new_grid = []
        for i in range(self.N):
            row = []
            for j in range(self.M):
                val = "."
                if (i,j) in loop_tiles:
                    val = grid[i][j]
                row.append(val)
            new_grid.append(row)
        return new_grid

    placements = {
        "7": [
            (0,-1),
            (1,0),
        ],
        "F": [
            (0,1),
            (1,0),
        ],
        "L": [
            (-1,0),
            (0,1),
        ],
        "J": [
            (-1,0),
            (0,-1),
        ],
        "|": [
            (-1,0),
            (1,0),
        ],
        "-": [
            (0,-1),
            (0,1),
        ],
        "S": [
            (0,-1),
            (0,1),
            (1,0),
            (-1,0),
        ],
    }
    def expand_tile_on_grid(self, new_grid, tile, i, j):
        x,y = (3 * i) + 1, (3 * j) + 1
        new_grid[x][y] = "#"
        for tx,ty in self.placements[tile]:
            a,b = tx + x,ty + y
            new_grid[a][b] = "#"

    def expand_grid(self, grid):
        new_grid = [["."] * (3 * len(grid[0])) for i in range(len(grid) * 3)]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != ".":
                    self.expand_tile_on_grid(new_grid, grid[i][j], i, j)
        return new_grid

    def grid_neighbors(self, tile, grid):
        transforms = [
            (0,1),
            (0,-1),
            (1,0),
            (-1,0),
        ]
        i,j = tile
        for tx,ty in transforms:
            x,y = tx + i, ty + j
            if x >= 0 and y >= 0 and x < len(grid) and y < len(grid[0]):
                if grid[x][y] == ".":
                    yield (x,y)

    def is_original_tile(self, i, j):
        return i % 3 == 1 and j % 3 == 1

    def count_inner_tiles(self, grid):
        start = [(0,0)]
        q = deque(start)
        visited = set(start)
        while q:
            tile = q.popleft()
            for n in self.grid_neighbors(tile, grid):
                if n in visited:
                    continue
                visited.add(n)
                q.append(n)
        
        inner_tiles = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not self.is_original_tile(i,j):
                    continue
                if grid[i][j] != ".":
                    continue
                if (i,j) in visited:
                    continue
                inner_tiles += 1
        return inner_tiles


    def run(self, fin):
        grid, edges = self.parse_input(fin)
        # identify loop
        loop_tiles = self.find_loop_tiles(edges, grid)
        # clear everything but loop
        grid = self.clear_all_but(grid, loop_tiles)
        # expand to 3x3
        old_grid = grid
        grid = self.expand_grid(grid)
        # flood fill and count inner tiles
        count = self.count_inner_tiles(grid)
        return count

if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    # case_markers = ["1"]
    # case_markers = ["1","2","3","4"]
    
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
