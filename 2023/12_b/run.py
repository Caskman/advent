from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        for line in fin:
            line = line.strip()
            springs, groups = line.split(" ")
            new_springs = springs
            new_groups = groups
            for i in range(4):
                new_springs += "?" + springs
                new_groups += "," + groups
            groups = [int(g) for g in new_groups.split(",")]
            yield new_springs, groups

    def get_possibilities(self, springs, groups):
        G = len(groups)
        dp = {}

        def backtrack(spring_index, group_index, group_count):
            key = (spring_index, group_index, group_count)
            if key not in dp:
                dp[key] = backtrack_raw(spring_index, group_index, group_count)
            return dp[key]

        def empty(spring_index, group_index, group_count):

            if group_count:
                # finished group isn't big enough
                if group_count != groups[group_index]:
                    return 0
                # right size, continue on
                else:
                    return backtrack(spring_index + 1, group_index + 1, 0)
            # continuing empty space
            else:
                return backtrack(spring_index + 1, group_index, group_count)

        def spring(spring_index, group_index, group_count):
            # check that group index is in bounds
            if group_index >= G:
                return 0
            # If continuing existing group
            if group_count:
                return backtrack(spring_index + 1, group_index, group_count + 1)
            # starting new group
            else:
                return backtrack(spring_index + 1, group_index, 1)

        def backtrack_raw(spring_index, group_index, group_count):
            # if we've reach end of springs
            if spring_index >= len(springs):
                # if we've also reached the end of the groups, we're done
                if (group_index >= G or (group_index == G - 1 and group_count == groups[group_index])):
                    return 1
                else:
                    return 0
            
            # if current group is too big
            if group_index < G and group_count > groups[group_index]:
                return 0
            
            cur_spring = springs[spring_index]
            if cur_spring == ".":
                return empty(spring_index, group_index, group_count)
            # either start new group or increment current group
            elif cur_spring == "#":
                return spring(spring_index, group_index, group_count)
            # try empty space or another spring
            elif cur_spring == "?":
                acc = 0
                # attempt empty space
                acc += empty(spring_index, group_index, group_count)
                # attempt spring
                acc += spring(spring_index, group_index, group_count)
                return acc
            
        return backtrack(0, 0, 0)


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
