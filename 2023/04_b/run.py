from collections import defaultdict
import re

class Solution:

    def run(self, fin):
        lines = fin.read().split("\n")
        acc = 0
        cardcounts = defaultdict(lambda:0)
        for line in lines:
            card, numsets = line.split(": ")
            cardnum = int(card.split(" ")[-1])
            copies = 1 + cardcounts[cardnum]
            acc += copies
            winning, possession = numsets.split(" | ")
            winning = re.split(r" +", winning.strip())
            possession = set(re.split(r" +", possession.strip()))
            for num in winning:
                if num in possession:
                    cardnum += 1
                    cardcounts[cardnum] += copies
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
