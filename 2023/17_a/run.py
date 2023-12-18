from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

TUP = (-1,0)
TDOWN = (1,0)
TLEFT = (0,-1)
TRIGHT = (0,1)

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        return fin.read().split("\n")

    dir_turn_map = {
        "l": {
            "l": (TUP, "d"),
            "s": (TRIGHT, "l"),
            "r": (TDOWN, "u"),
        },
        "r": {
            "l": (TDOWN, "u"),
            "s": (TLEFT, "r"),
            "r": (TUP, "d"),
        },
        "u": {
            "l": (TRIGHT, "l"),
            "s": (TDOWN, "u"),
            "r": (TLEFT, "r"),
        },
        "d": {
            "l": (TLEFT, "r"),
            "s": (TUP, "d"),
            "r": (TRIGHT, "l"),
        },
    }
    def translate(self, x, y, incoming_dir, turn):
        translation, new_incoming_dir = self.dir_turn_map[incoming_dir][turn]
        tx, ty = translation
        return x + tx, y + ty, new_incoming_dir


    def get_neighbors(self, grid, curr_node):
        x, y, incoming_dir, length = curr_node
        turns = ["l","r"]
        if length < 3:
            turns.append("s")
        
        for turn in turns:
            a, b, new_incoming_dir = self.translate(x, y, incoming_dir, turn)
            if a >= 0 and b >= 0 and a < len(grid) and b < len(grid[0]):
                new_length = length + 1 if turn == "s" else 1
                weight = int(grid[a][b])
                new_node = (a, b, new_incoming_dir, new_length)
                yield new_node, weight

    def run(self, fin):
        grid = self.parse_input(fin)
        start = (0, 0, "u", 0)
        q = [(0, start)]
        dists = defaultdict(lambda: float("inf"))
        dists[start] = 0
        visited = set()
        while q:
            curr_node_data = heappop(q)
            node_dist, curr_node = curr_node_data
            x, y, dir, length = curr_node
            if curr_node in visited:
                continue
            visited.add(curr_node)

            if x == len(grid) - 1 and y == len(grid[0]) - 1:
                return dists[curr_node]
            
            for neighbor_node, weight in self.get_neighbors(grid, curr_node):
                if neighbor_node in visited:
                    continue

                new_dist = dists[curr_node] + weight
                if new_dist < dists[neighbor_node]:
                    dists[neighbor_node] = new_dist
                    heappush(q, (dists[neighbor_node], neighbor_node))
                


        
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
