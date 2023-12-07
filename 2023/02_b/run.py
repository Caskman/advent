from collections import defaultdict

def run(fin):
    lines = fin.read().split("\n")
    acc = 0
    for line in lines:
        a1 = line.split(": ")
        rounds = a1[1].split("; ")
        max_colors = defaultdict(lambda:0)
        for round in rounds:
            categories = round.split(", ")
            for cat in categories:
                count, color = cat.split(" ")
                count = int(count)
                max_colors[color] = max(max_colors[color], count)
        power = max_colors["red"] * max_colors["green"] * max_colors["blue"]
        acc += power
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
                output = run(fin)
                print(f"#{num} Expected: {answer} Actual: {output}")
