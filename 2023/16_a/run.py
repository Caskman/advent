from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        grid = fin.read().split("\n")
        self.N = len(grid)
        self.M = len(grid[0])
        return grid

    def translate(self, node, directions):
        transforms = {
            "u": (-1,0),
            "d": (1,0),
            "l": (0,-1),
            "r": (0,1),
        }
        new_nodes = []
        for d in directions:
            tx,ty = transforms[d]
            x,y,d2 = node
            a,b = x + tx, y + ty
            if a >= 0 and b >= 0 and a < self.N and b < self.M:
                new_nodes.append((a,b,self.r(d)))
        return new_nodes
    
    reverse_map = {
        "l": "r",
        "r": "l",
        "u": "d",
        "d": "u",
    }
    def r(self, d):
        return self.reverse_map[d]

    def get_neighbors(self, grid, node):
        x, y, d = node
        tile = grid[x][y]
        if tile == "|":
            if d in ("l","r"):
                return self.translate(node, ["u","d"])
            else:
                return self.translate(node, [self.r(d)])
        elif tile == "-":
            if d in ("u","d"):
                return self.translate(node, ["l","r"])
            else:
                return self.translate(node, [self.r(d)])
        elif tile == ".":
            return self.translate(node, [self.r(d)])
        elif tile == "/":
            m = {
                "u": "l",
                "d": "r",
                "l": "u",
                "r": "d",
            }
            return self.translate(node, [m[d]])
        elif tile == "\\":
            m = {
                "u": "r",
                "d": "l",
                "l": "d",
                "r": "u",
            }
            return self.translate(node, [m[d]])
        else:
            raise Exception(f"woops {tile}")


    def run(self, fin):
        grid = self.parse_input(fin)

        start = (0,0,"l")
        visited = set()
        q = deque([])
        energized = set()

        visited.add(start)
        q.append(start)
        energized.add((0,0))
        while q:
            node = q.popleft()
            x, y, d = node
            energized.add((x,y))
            for n in self.get_neighbors(grid, node):
                if n in visited:
                    continue
                visited.add(n)
                q.append(n)
        return len(energized)
        
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
