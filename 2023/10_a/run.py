from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque

class Solution:
    def parse_input(self, fin) -> None:
        lines = fin.read().split("\n")
        self.lines = lines
        self.edges = defaultdict(list)
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] != ".":
                    self.add_edge(i, j)

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

    def add_edge(self, i, j):
        transforms = [
            (-1,0,"up"),
            (1,0,"down"),
            (0,-1,"left"),
            (0,1,"right"),
        ]

        for tx,ty,d in transforms:
            x, y = i + tx, j + ty
            if self.is_valid(x, y) and self.is_adj(i, j, d, x, y):
                self.edges[(i,j)].append((x, y))

    def is_valid(self, i, j):
        return i >= 0 and j >= 0 and i < len(self.lines) and j < len(self.lines[0])
    
    def is_adj(self, x, y, d, i, j):
        tile = self.lines[x][y]
        other = self.lines[i][j]
        available_directions = self.possible_directions[tile]
        if d not in available_directions:
            return False
        return other in self.dirs[d]

    def bfs(self):
        start = None
        lines = self.lines
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "S":
                    start = (i,j)
                    break
        
        q = deque([start])
        visited = set([start])
        dist = 0
        while q:
            newq = deque([])
            while q:
                curr = q.popleft()
                for n in self.edges[curr]:
                    if n in visited:
                        continue
                    visited.add(n)
                    newq.append(n)
            dist += 1
            q = newq
        return dist - 1
    
    def run(self, fin):
        self.parse_input(fin)
        steps = self.bfs()
        return steps

if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    # case_markers = ["1","2"]
    
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
