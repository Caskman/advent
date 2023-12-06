import re

def run(input_fin):
    lines = input_fin.read().split("\n")
    acc = 0
    for l in lines:
        li = list(l)
        # nums = re.findall(r"")
        nums = [s for s in li if s.isdigit()]
        acc += int(nums[0] + nums[-1])
    return acc


if __name__ == "__main__":
    with open("answer_1.txt", "r") as fin:
        answer = fin.read()
    with open("input_1.txt", "r") as fin:
        output = run(fin)
        print(f"Expected: {answer} Actual: {output}")

    with open("answer_2.txt", "r") as fin:
        answer = fin.read()
    with open("input_2.txt", "r") as fin:
        output = run(fin)
        print(f"Expected: {answer} Actual: {output}")
