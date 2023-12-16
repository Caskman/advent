from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

"""
1###
##2#
#3#4

1##
##3
#2#
##4
"""


class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        pattern = []
        for line in fin:
            line = line.strip()
            if line == "":
                yield pattern
                pattern = []
            else:
                pattern.append(line)
        yield pattern

    def transpose(self, pattern):
        new_pattern = []
        for j in range(len(pattern[0])):
            new_row = ""
            for i in range(len(pattern)):
                new_row += pattern[i][j]
            new_pattern.append(new_row)
        return new_pattern

    def get_diff(self, s1, s2):
        diffs = 0
        for i in range(len(s1)):
            diffs += 0 if s1[i] == s2[i] else 1
        return diffs

    def horizontal(self, pattern):
        for i in range(len(pattern)):
            success = False
            smudges = 1
            u = i
            l = i + 1
            while u >= 0 and l < len(pattern):
                success = True
                if self.get_diff(pattern[u], pattern[l]) > 1 \
                    or (self.get_diff(pattern[u], pattern[l]) == 1 and smudges == 0):
                    success = False
                    break
                elif self.get_diff(pattern[u], pattern[l]) == 1 and smudges > 0:
                    smudges -= 1
                u -= 1
                l += 1
            if success and smudges == 0:
                return i + 1
        return -1

    def vertical(self, pattern):
        tp = self.transpose(pattern)
        return self.horizontal(tp)

    def summarize(self, pattern):
        hor_ref = self.horizontal(pattern)
        if hor_ref == -1:
            vert_ref = self.vertical(pattern)
            # print(f"vert {vert_ref}")
            return vert_ref
        else:
            # print(f"hor {hor_ref}")
            return hor_ref * 100

    def run(self, fin):
        patterns = self.parse_input(fin)
        acc = 0
        for pattern in patterns:
            count = self.summarize(pattern)
            # print(count)
            acc += count
        return acc
        # return sum([self.summarize(pattern) for pattern in patterns])


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
