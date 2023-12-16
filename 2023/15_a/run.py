from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        line = fin.read().strip()
        return line.split(",")
    
    def hash(self, string):
        hash = 0
        for c in string:
            hash = (17 * (hash + ord(c))) % 256
        return hash

    def run(self, fin):
        strings = self.parse_input(fin)
        return sum([self.hash(s) for s in strings])
        
        
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
