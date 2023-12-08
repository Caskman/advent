from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict

class Solution:
    def parse_input(self, fin) -> None:
        lines = fin.read().split("\n")
        directions = lines[0]
        edges = defaultdict(dict)

        for line in lines[2:]:
            node, es = line.split(" = ")
            left, right = es.replace(")","").replace("(","").split(", ")
            edges[node]["L"] = left
            edges[node]["R"] = right

        return directions, edges
    
    def lcm_pair(self, v1, v2):
        if v1 > v2:
            n, d = v1, v2
        else:
            n, d = v2, v1
        
        r = n % d
        while r != 0:
            n = d
            d = r
            r = n % d
        return v1 * v2 // d
    
    def lcm(self, vals):
        curr = vals[0]
        for v in vals:
            curr = self.lcm_pair(curr, v)
        return curr

    def run(self, fin):
        directions, edges = self.parse_input(fin)

        starts = [e for e in edges if e[2] == "A"]
        counts = {}
        for e in starts:
            count = 0
            start = e
            curr = e
            while curr[2] != "Z":
                for d in directions:
                    curr = edges[curr][d]
                count += 1
            counts[start] = count * len(directions)

        return self.lcm(list(counts.values()))

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
