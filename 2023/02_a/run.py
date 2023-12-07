
limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def run(fin):
    lines = fin.read().split("\n")
    acc = 0
    for line in lines:
        a1 = line.split(": ")
        id = a1[0].split(" ")[1]
        rounds = a1[1].split("; ")
        possible = True
        for round in rounds:
            categories = round.split(", ")
            for cat in categories:
                count, color = cat.split(" ")
                if int(count) > limits[color]:
                    possible = False
        if possible:
            acc += int(id)
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
