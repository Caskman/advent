from dataclasses import dataclass
from bisect import bisect_left, bisect_right

@dataclass
class Interval:
    left: int
    right: int

    def __init__(self, left, right):
        self.left = left
        self.right = right
        if left > right:
            raise Exception("problem!")

@dataclass
class AdventMapRange:
    src: Interval
    dest: Interval

@dataclass
class AdventMap:
    key: str
    dest: str
    ranges: list[AdventMapRange]

    def add_range(self, src: int, dest: int, range_len: int) -> None:
        new_range = AdventMapRange(Interval(src, src + range_len - 1), Interval(dest, dest + range_len - 1))
        ranges = [r.src.left for r in self.ranges]
        left = bisect_left(ranges, new_range.src.left)
        right = bisect_right(ranges, new_range.src.left)
        if left == right:
            self.ranges.insert(left, new_range)
        else:
            rights = [r.src.right for r in self.ranges]
            insertion = bisect_left(rights, range_len, lo=left, hi=right)
            self.ranges.insert(insertion, new_range)

    def map_interval(self, interval: Interval) -> int:
        # identify likely ranges
            # left range has smallest right larger than interval left
            # right range has largest left smaller than interval right
        # resolve interval with each range
            # at most three intervals come out
        # consider space between each range
            # init prev_right with interval.left
            # each loop, if prev_right < range.left and range.left - prev_right > 1, produce unmapped interval
            # after loop, if prev_right < interval.right, produce unmapped interval

        # lefts = [r.src.left for r in self.ranges]
        # rights = [r.src.right for r in self.ranges]
        # left_range = bisect_left(rights, interval.left)
        # right_range = bisect_right(lefts, interval.right)

        result_intervals = []
        prev_right = interval.left
        for map_range in self.ranges:
        # for map_range in self.ranges[left_range:right_range+1]:
            # Account for unmapped spaces before first range and in between ranges
            if map_range.src.left - prev_right > 1:
                new_interval = Interval(prev_right, map_range.src.left - 1)
                result_intervals.append(new_interval)
            # Account for mapped intersection of range and interval
            new_src_left = max(map_range.src.left, interval.left)
            new_src_right = min(map_range.src.right, interval.right)
            if new_src_left <= new_src_right:
                range_len = new_src_right - new_src_left
                new_dest_left = map_range.dest.left + new_src_left - map_range.src.left
                new_dest_right = new_dest_left + range_len
                
                new_interval = Interval(new_dest_left, new_dest_right)
                result_intervals.append(new_interval)

            # Save range right for next loop
            prev_right = map_range.src.right + 1

        # Account for unmapped space after right range
        if prev_right <= interval.right:
            new_interval = Interval(prev_right,interval.right)
            result_intervals.append(new_interval)

        return result_intervals



        # src_ranges = [r.src for r in self.ranges]
        # left = bisect_left(src_ranges, val)
        # right = bisect_right(src_ranges, val)
        # for i in range(max(left-1, 0), right):
        #     r = self.ranges[i]
        #     if val >= r.src and val <= r.src + r.range_len:
        #         diff = val - r.src
        #         return r.dest + diff
        # return val


class Solution:
    def parse_input(self, fin) -> tuple[list[Interval], dict[str, AdventMap]]:
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
    
    def parse_seeds(self, line: str) -> list[Interval]:
        nums = line.split(": ")[-1].split(" ")
        seeds = [int(n) for n in nums]
        final_seeds = []
        for i in range(len(seeds)):
            if i % 2 == 1:
                continue
            start = seeds[i]
            range_len = seeds[i+1]
            left = start
            right = start + range_len - 1
            final_seeds.append(Interval(left, right))
        return final_seeds
    
    def init_map(self, line: str) -> AdventMap:
        edges = line.split(" ")[0]
        src, dest = edges.split("-to-")
        return AdventMap(src, dest, [])
    
    def add_to_map(self, advent_map: AdventMap, line: str) -> None:
        dest_start, src_start, range_len = line.split(" ")
        advent_map.add_range(int(src_start), int(dest_start), int(range_len))

    def get_lowest_location(self, seeds: list[Interval], maps: dict[str, AdventMap]) -> int:
        curr = "seed"
        intervals = seeds
        while curr != "location":
            print(f"at {curr}")
            print(intervals)
            print()
            alm = maps[curr]
            new_intervals = []
            for interval in intervals:
                new_intervals += alm.map_interval(interval)
            intervals = new_intervals
            curr = alm.dest
        # import pprint; pprint.pprint(intervals)
        print("at end")
        print(intervals)
        return min([i.left for i in intervals])

    def run(self, fin):
        seeds, maps = self.parse_input(fin)
        return self.get_lowest_location(seeds, maps)

if __name__ == "__main__":
    import os
    case_markers = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.startswith("input"):
            marker = int(f.split(".")[0].split("_")[1])
            case_markers.append(marker)
    case_markers = ["1"]
    
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
