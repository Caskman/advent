from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict, deque
from heapq import heappop, heappush

class Solution:
    def parse_input(self, fin) -> tuple[int, list[list[str]]]:
        line = fin.read().strip()
        for step in line.split(","):
            splits = step.split("=")
            op = "="
            if len(splits) != 2:
                splits = step.split("-")
                op = "-"
                yield splits[0], op, 0
            else:
                yield splits[0], op, int(splits[1])

    
    def hash(self, string):
        hash = 0
        for c in string:
            hash = (17 * (hash + ord(c))) % 256
        return hash
    
    def get_entry(self, l, entry):
        for i, item in enumerate(l):
            label, power = item
            if label == entry[0]:
                return i
        return -1

    def execute_step(self, boxes, step):
        label, op, power = step
        entry = (label, power)
        hash = self.hash(label)
        index = self.get_entry(boxes[hash], entry)
        if op == "=":
            if index > -1:
                boxes[hash][index] = entry
            else:
                boxes[hash].append(entry)
        else:
            if index > -1:
                l = boxes[hash]
                boxes[hash] = l[:index] + l[index + 1:]

    def calculate_power(self, boxes):
        acc = 0
        for i in range(256):
            for j, item in enumerate(boxes[i]):
                label, power = item
                final_power = (i + 1) * (j + 1) * power
                acc += final_power
        return acc

    def print_boxes(self, boxes):
        keys = sorted(boxes.keys())
        for k in keys:
            if len(boxes[k]) > 0:
                lenses_string = ""
                for label, lens in boxes[k]:
                    lenses_string += f"[{label} {lens}] "
                print(f"Box {k}: {lenses_string}")
            

    def run(self, fin):
        steps = self.parse_input(fin)
        boxes = defaultdict(list)
        for step in steps:
            self.execute_step(boxes, step)
            # print(step)
            # self.print_boxes(boxes)
            # print()
        return self.calculate_power(boxes)
        
        
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
