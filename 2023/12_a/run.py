from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        for line in fin:
            springs, groups = line.strip().split(" ")
            yield springs, [int(g) for g in groups.split(",")]

    def get_possibilities(self, springs_original, groups):
        G = len(groups)
        L = len(springs_original)

        def backtrack(springs, si, gi, group_count):
            if si >= L:
                return 0

            while si < L:
                curr = springs[si]
                if curr == "#" and gi >= G:
                    return 0
                elif curr == "." and group_count > -1:
                    if group_count != groups[gi]:
                        return 0
                    else:
                        gi += 1
                        group_count = -1
                elif curr == "#":
                    if group_count == -1:
                        group_count = 0
                    group_count += 1
                    if group_count > groups[gi]:
                        return 0
                elif curr == "?":
                    first_part = springs[:max(0,si)]
                    second_part = springs[si + 1:]
                    route_1_springs = first_part + "." + second_part
                    route_1_count = backtrack(route_1_springs, si, gi, group_count)
                    
                    route_2_springs = first_part + "#" + second_part
                    route_2_count = backtrack(route_2_springs, si, gi, group_count)
                    return route_1_count + route_2_count
                si += 1
            if si >= L \
                and \
                    (gi >= G \
                        or (gi == G - 1 and group_count == groups[gi])):
                # print(f"found possibility: {springs}")
                return 1
            else:
                return 0
            
        return backtrack(springs_original, 0, 0, -1)


    def run(self, fin):
        spring_rows = self.parse_input(fin)
        
        acc = 0
        for i, row in enumerate(spring_rows):
            springs, groups = row
            count = self.get_possibilities(springs, groups)
            # print(count)
            acc += count
        return acc


if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    # case_markers = ["3"]
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
