from collections import defaultdict

class Solution:
    def get_nums(self):
        for i in range(len(self.lines)):
            line = self.lines[i]
            start = -1
            for j in range(len(line)):
                c = line[j]
                if start >= 0 and not c.isdigit():
                    stop = j
                    yield int(line[start:stop]), i, start, stop
                    start = -1
                elif start < 0 and c.isdigit():
                    start = j
            if start >= 0:
                stop = self.M
                yield int(line[start:stop]), i, start, stop

    def is_part(self, row, col):
        if row < 0 or col < 0 or row >= self.N or col >= self.M:
            return False
        char = self.lines[row][col]
        if char.isdigit() or char == ".":
            return False
        return True

    def adjacent_to_part(self, row, start, stop):
        if self.is_part(row, start - 1) or self.is_part(row, stop):
            return True
        else:
            for i in range(start - 1, stop + 1):
                if self.is_part(row - 1, i) or self.is_part(row + 1, i):
                    return True
        return False
    
    def is_star(self, row, col):
        if row < 0 or col < 0 or row >= self.N or col >= self.M:
            return False
        char = self.lines[row][col]
        return char == "*"
    
    def get_adjacent_stars(self, row, start, stop):
        if self.is_star(row, start - 1):
            yield (row, start - 1)
        if self.is_star(row, stop):
            yield (row, stop)
        for i in range(start - 1, stop + 1):
            if self.is_star(row - 1, i):
                yield (row - 1, i)
            if self.is_star(row + 1, i):
                yield (row + 1, i)

    def run(self, fin):
        lines = fin.read().split("\n")
        self.N = len(lines)
        self.M = len(lines[0])
        self.lines = lines
        acc = 0
        stars = defaultdict(set)
        for num, row, start, stop in self.get_nums():
            for star in self.get_adjacent_stars(row, start, stop):
                stars[star].add(num)
        for star in stars:
            if len(stars[star]) == 2:
                nums = list(stars[star])
                acc += nums[0] * nums[1]
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
