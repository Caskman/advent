from dataclasses import dataclass
from functools import cmp_to_key
from collections import defaultdict

@dataclass
class AdventHand:
    hand: str
    bid: int

class Solution:
    def parse_input(self, fin) -> list[AdventHand]:
        for line in fin:
            line = line.strip()
            hand, bid = line.split(" ")
            bid = int(bid)
            yield AdventHand(hand, bid)
    
    def full_house(self, cs, jokers):
        counts = cs[0] + cs[1] + jokers
        return counts == 5

    def two_pair(self, cs, jokers):
        counts = cs[0] + cs[1] + jokers
        return counts == 4

    def get_rank(self, hand: AdventHand):
        counts = defaultdict(lambda: 0)
        for c in hand.hand:
            counts[c] += 1
        
        jokers = counts["J"]
        counts["J"] = 0
        counts = sorted(list(counts.values()), reverse=True)
        top_count = counts[0] + jokers
        if top_count == 5:
            return 6
        elif top_count == 4:
            return 5
        elif self.full_house(counts, jokers):
        # elif counts[0] == 3 and counts[1] == 2:
            return 4
        elif top_count == 3:
            return 3
        elif self.two_pair(counts, jokers):
        # elif counts[0] == 2 and counts[1] == 2:
            return 2
        elif top_count == 2:
            return 1
        else:
            return 0

    def convert_card(self, char: str) -> int:
        cards = {
            "T": 10,
            "J": -1,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        if char in cards:
            return cards[char]
        else:
            return int(char)

    def sort_hands(self, hands: list[AdventHand]) -> None:
        def cmp(h1: AdventHand, h2: AdventHand):
            r1 = self.get_rank(h1)
            r2 = self.get_rank(h2)
            if r1 == r2:
                for i in range(len(h1.hand)):
                    c1 = h1.hand[i]
                    c2 = h2.hand[i]
                    if c1 == c2:
                        continue
                    else:
                        return self.convert_card(c1) - self.convert_card(c2)
                return 0
            else:
                return r1 - r2

        return sorted(hands, key=cmp_to_key(cmp))

    def run(self, fin):
        hands = list(self.parse_input(fin))
        hands = self.sort_hands(hands)
        return sum([(i + 1) * h.bid for i, h in enumerate(hands)])

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
