
numbers = [
    ("one", "1"),
    ("two", "2"),
    ("three", "3"),
    ("four", "4"),
    ("five", "5"),
    ("six", "6"),
    ("seven", "7"),
    ("eight", "8"),
    ("nine", "9"),
]

def get_first(string):
    for i in range(len(string)):
        for ns, ni in numbers:
            if string[i].isdigit():
                return string[i]
            if string[i:i+len(ns)] == ns:
                return ni

def get_last(string):
    for i in range(len(string) - 1, -1, -1):
        for ns, ni in numbers:
            if string[i].isdigit():
                return string[i]
            if string[i:i+len(ns)] == ns:
                return ni


def run(input_fin):
    print("start")
    lines = input_fin.read().split("\n")
    acc = 0
    for l in lines:
        val = int(get_first(l) + get_last(l))
        acc += val
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


