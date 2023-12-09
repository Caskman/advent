from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict

class Solution:
    def parse_input(self, fin) -> None:
        for line in fin:
            line = line.strip()
            yield [int(n) for n in line.split(" ")]

    def get_history(self, dataset: list[int]) -> list[int]:
        history = []
        prev = dataset[0]
        for d in dataset[1:]:
            history.append(d - prev)
            prev = d
        return history

    def is_all_zero(self, dataset: list[int]) -> bool:
        for d in dataset:
            if d != 0:
                return False
        return True

    def get_prev_val(self, dataset: list[int]) -> int:
        if self.is_all_zero(dataset):
            return 0
        history = self.get_history(dataset)
        prev_history = self.get_prev_val(history)
        return dataset[0] - prev_history

    def run(self, fin):
        datasets = self.parse_input(fin)
        acc = 0
        for dataset in datasets:
            acc += self.get_prev_val(dataset)
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
