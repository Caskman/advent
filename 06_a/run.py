import re

class Solution:
    def parse_input(self, fin) -> tuple[list[int], list[int]]:
        lines = fin.read().split("\n")
        t = lambda l: [int(i) for i in re.split(r"\s+", l.split(":")[-1].strip())]
        times = t(lines[0])
        dists = t(lines[1])
        return times, dists

    def can_win(self, time: int, dist: int, acc_time: int) -> bool:
        remaining_time = time - acc_time
        return dist < remaining_time * acc_time

    def run(self, fin):
        times, dists = self.parse_input(fin)
        acc = 1
        for i in range(len(times)):
            time = times[i]
            dist = dists[i]
            lower_bound = 0
            for j in range(1,time):
                if self.can_win(time, dist, j):
                    lower_bound = j
                    break
            upper_bound = lower_bound
            for j in range(time-1, 1, -1):
                if self.can_win(time, dist, j):
                    upper_bound = j
                    break
            acc *= upper_bound - lower_bound + 1
        return acc



if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    
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
