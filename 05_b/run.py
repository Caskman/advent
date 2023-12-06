from dataclasses import dataclass
from bisect import bisect_left, bisect_right


@dataclass
class AdventMapRange:
    src: int
    dest: int
    range_len: int

@dataclass
class AdventMap:
    key: str
    dest: str
    ranges: list[AdventMapRange]

    def add_range(self, src: int, dest: int, range_len: int) -> None:
        new_range = AdventMapRange(src, dest, range_len)
        src_ranges = [r.src for r in self.ranges]
        left = bisect_left(src_ranges, src)
        right = bisect_right(src_ranges, src)
        if left == right:
            self.ranges.insert(left, new_range)
        else:
            lens = [r.range_len for r in self.ranges]
            insertion = bisect_left(lens[left:right], range_len)
            self.ranges.insert(insertion, new_range)

    def map_val(self, val: int) -> int:
        # src_ranges = [r.src for r in self.ranges]
        # left = bisect_left(src_ranges, val)
        # right = bisect_right(src_ranges, val)
        for i in range(len(self.ranges)):
            r = self.ranges[i]
            if val >= r.src and val < r.src + r.range_len:
                diff = val - r.src
                return r.dest + diff
        return val


class Solution:
    def parse_input(self, fin) -> tuple[list[str], dict[str, AdventMap]]:
        seeds = None
        curr_map: AdventMap = None
        maps: dict[str, AdventMap] = {}
        for line in fin:
            line = line.strip()
            if line.startswith("seeds:"):
                seeds = self.parse_seeds(line)
            elif line.endswith("map:"):
                if curr_map:
                    maps[curr_map.key] = curr_map
                curr_map = self.init_map(line)
            elif curr_map and line != "":
                self.add_to_map(curr_map, line)
        if curr_map and curr_map.key not in maps:
            maps[curr_map.key] = curr_map
        return seeds, maps
    
    def parse_seeds(self, line: str) -> list[int]:
        nums = line.split(": ")[-1].split(" ")
        seeds = [int(n) for n in nums]
        final_seeds = []
        for i in range(len(seeds)):
            if i % 2 == 1:
                continue
            start = seeds[i]
            range_len = seeds[i+1]
            final_seeds += list(range(start, start + range_len))
        return final_seeds
    
    def init_map(self, line: str) -> AdventMap:
        edges = line.split(" ")[0]
        src, dest = edges.split("-to-")
        return AdventMap(src, dest, [])
    
    def add_to_map(self, advent_map: AdventMap, line: str) -> None:
        dest_start, src_start, range_len = line.split(" ")
        advent_map.add_range(int(src_start), int(dest_start), int(range_len))

    def get_lowest_location(self, seeds: list[int], maps: dict[str, AdventMap]) -> int:
        curr = "seed"
        vals = seeds
        while curr != "location":
            alm = maps[curr]
            vals = [alm.map_val(val) for val in vals]
            curr = alm.dest
        return min(vals)

    def run(self, fin):
        seeds, maps = self.parse_input(fin)
        return self.get_lowest_location(seeds, maps)

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
