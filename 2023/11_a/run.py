from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque

class Solution:
    def parse_input(self, fin) -> None:
        universe = fin.read().split("\n")
        return universe
    
    def expand_universe(self, universe):
        universe = self.expand_rows(universe)
        universe = self.expand_cols(universe)
        self.N = len(universe)
        self.M = len(universe[0])
        return universe

    def expand_rows(self, universe):
        new_universe = []
        for row in universe:
            empty = True
            for c in row:
                if c != ".":
                    empty = False
                    break
            if empty:
                new_universe.append(["."] * len(row))
            new_universe.append(row)
        return new_universe

    def expand_cols(self, universe):
        new_universe = [[] for i in range(len(universe))]
        for j in range(len(universe[0])):
            empty = True
            for i in range(len(universe)):
                if universe[i][j] != ".":
                    empty = False
                new_universe[i].append(universe[i][j])
            if empty:
                for k in range(len(universe)):
                    new_universe[k].append(".")
        return new_universe

    def convert_coords(self, x, y):
        return x * self.M + y
    
    def is_valid(self, x, y):
        return x >= 0 and y >= 0 and x < self.N and y < self.M

    def create_edges(self, universe):
        transforms = [(-1,0),(1,0),(0,-1),(0,1)]
        edges = defaultdict(list)
        for i in range(len(universe)):
            for j in range(len(universe[0])):
                node = self.convert_coords(i,j)
                for tx,ty in transforms:
                    x,y = i + tx, j + ty
                    if self.is_valid(x,y):
                        edges[node].append(self.convert_coords(x,y))
        return edges

    def get_relevant_nodes(self, universe):
        r = []
        for i, row in enumerate(universe):
            for j, c in enumerate(row):
                if c == "#":
                    r.append(self.convert_coords(i,j))
        return r

    def bfs(self, edges, dists, targets, start):
        targets = set(targets)
        q = deque([start])
        visited = set()
        counter = 1
        while q and targets:
            new_q = deque([])
            while q:
                node = q.popleft()
                for n in edges[node]:
                    if n in visited:
                        continue
                    visited.add(n)
                    new_q.append(n)
                    if n in targets:
                        targets.remove(n)
                        dists[start][n] = counter
            counter += 1
            q = new_q
        if targets:
            print(f"targets length still {len(targets)}")
                    

    def all_pairs_paths(self, universe, edges):
        relevant_nodes = self.get_relevant_nodes(universe)
        dists = defaultdict(dict)
        for i in range(len(relevant_nodes)):
            targets = relevant_nodes[:i] + relevant_nodes[i+1:]
            self.bfs(edges, dists, targets, relevant_nodes[i])
        return dists, relevant_nodes


    def run(self, fin):
        universe = self.parse_input(fin)
        # Expand universe
        universe = self.expand_universe(universe)
        # Create edges
        edges = self.create_edges(universe)
        # compute all pairs shortest path
        dists, relevant_nodes = self.all_pairs_paths(universe, edges)
        # calculate all pairs sum
        acc = 0
        for i, start in enumerate(relevant_nodes):
            for end in relevant_nodes[i+1:]:
                acc += dists[start][end]
        return acc

if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    # case_markers = ["1"]
    
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
