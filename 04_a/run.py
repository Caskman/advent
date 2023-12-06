from collections import defaultdict
import re

class Solution:

    def run(self, fin):
        lines = fin.read().split("\n")
        acc = 0
        for line in lines:
            power = -1
            winning, possession = line.split(": ")[-1].split(" | ")
            winning = re.split(r" +", winning.strip())
            possession = set(re.split(r" +", possession.strip()))
            for num in winning:
                if num in possession:
                    power += 1
            acc += 2 ** power if power >= 0 else 0
        return acc


if __name__ == "__main__":
    import os
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            num = int(f.split(".")[0].split("_")[1])
            answer_path = f"answer_{num}.txt"
            if not os.path.isfile(answer_path):
                continue
            with open(answer_path, "r") as fin:
                answer = fin.read()
            with open(f, "r") as fin:
                output = Solution().run(fin)
                print(f"#{num} Expected: {answer} Actual: {output}")
