from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        lines = fin.read().split("\n")
        expansion = int(lines[0])
        universe = lines[1:]
        self.N = len(universe)
        self.M = len(universe[0])
        return expansion, universe
    
    def convert_coords(self, x, y):
        return x * self.M + y
    
    def is_valid(self, x, y):
        return x >= 0 and y >= 0 and x < self.N and y < self.M

    def get_empty_areas(self, universe):
        empty_rows = []
        empty_cols = []
        for i, row in enumerate(universe):
            empty = True
            for c in row:
                if c == "#":
                    empty = False
                    break
            if empty:
                empty_rows.append(i)
    
        for j in range(len(universe[0])):
            empty = True
            for i in range(len(universe)):
                if universe[i][j] == "#":
                    empty = False
                    break
            if empty:
                empty_cols.append(j)

        # print(empty_rows)
        # print(empty_cols)
        # print()
        return set(empty_rows), set(empty_cols)

    def create_edges(self, universe, expansion_factor):
        col_transforms = [(-1,0),(1,0)]
        row_transforms = [(0,-1),(0,1)]

        empty_rows, empty_cols = self.get_empty_areas(universe)

        edges = defaultdict(dict)
        for i in range(len(universe)):
            for j in range(len(universe[0])):
                node = self.convert_coords(i,j)

                for tx,ty in col_transforms:
                    x,y = i + tx, j + ty
                    if self.is_valid(x,y):
                        target = self.convert_coords(x,y)
                        weight = expansion_factor if x in empty_rows else 1
                        edges[node][target] = weight

                for tx,ty in row_transforms:
                    x,y = i + tx, j + ty
                    if self.is_valid(x,y):
                        target = self.convert_coords(x,y)
                        weight = expansion_factor if y in empty_cols else 1
                        edges[node][target] = weight
        return edges

    def get_relevant_nodes(self, universe):
        r = []
        for i, row in enumerate(universe):
            for j, c in enumerate(row):
                if c == "#":
                    r.append(self.convert_coords(i,j))
        return r

    def shortest_paths(self, edges, global_dists, targets, start):
        old_targets = targets
        targets = set(targets)
        heap = [(0, start)]
        visited = set()
        dists = defaultdict(lambda: float("inf"))
        dists[start] = 0
        while heap and targets:
            node_dist, node = heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            if node in targets:
                targets.remove(node)
            for n in edges[node]:
                if n in visited:
                    continue
                weight = edges[node][n]
                new_dist = node_dist + weight
                if new_dist < dists[n]:
                    dists[n] = new_dist
                    heappush(heap, (new_dist, n))
        
        for n in old_targets:
            global_dists[start][n] = dists[n]
                    

    def all_pairs_paths(self, universe, edges):
        relevant_nodes = self.get_relevant_nodes(universe)
        dists = defaultdict(dict)
        for i in range(len(relevant_nodes)):
            targets = relevant_nodes[:i] + relevant_nodes[i+1:]
            self.shortest_paths(edges, dists, targets, relevant_nodes[i])
        return dists, relevant_nodes


    def run(self, fin):
        expansion, universe = self.parse_input(fin)
        # print(expansion)
        # Create edges
        edges = self.create_edges(universe, expansion)
        # for n in edges:
        #     print(n)
        #     print(edges[n])
        #     print()
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
