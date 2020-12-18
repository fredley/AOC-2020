import asyncio
from collections import defaultdict
import operator
import time


async def parse_line(line):
    line = line.replace(" ", "")
    total = 0
    op = None
    i = 0
    while i < len(line):
        char = line[i]
        if char == '(':
            skip = find_closure(line[i:])
            inner_value = await parse_line(line[i + 1:i + skip])
            if op is None:
                total = inner_value
            else:
                total = op(total, inner_value)
            i += skip + 1
            continue
        elif char == '+':
            op = operator.add
        elif char == '*':
            op = operator.mul
        else:
            if op is None:
                total = int(char)
            else:
                total = op(total, int(char))
        i += 1
    return total


async def parse_line_2(line):
    line = line.replace(" ", "")
    # replace brackets with values, deepest to shallowest
    max_depth = 0
    depth = 0
    ranges = defaultdict(list)
    for i, char in enumerate(line):
        if char == '(':
            depth += 1
            max_depth = max(depth, max_depth)
            ranges[depth].append([i])
        if char == ')':
            ranges[depth][-1].append(i)
            depth -= 1
    list_line = [int(char) if char.isdigit() else char for char in line]
    for depth in range(max_depth, 0, -1):
        for r in ranges[depth]:
            list_line = replace_range(list_line, r)
    return evaluate_line(list_line)


def replace_range(line, r):
    # sub out this portion of the string with the result value
    value = evaluate_line(line[r[0] + 1:r[1]])
    padding = [None] * (r[1] - r[0])
    # pad so ranges in outer still make sense
    return line[:r[0]] + [value] + padding + line[r[1] + 1:]


def evaluate_line(line):
    # evaluate a line with no brackets
    # First, collapse plusses, then eval
    line = [item for item in line if item is not None]
    new_line = []
    last_no = None
    i = 0
    while i < len(line):
        char = line[i]
        if char == '+':
            last_no += int(line[i+1])
            i += 2
        elif char == '*':
            new_line += [last_no, char]
            last_no = None
            i += 1
        elif isinstance(char, int):
            last_no = char
            i += 1
        else:
            raise
    if last_no is not None:
        new_line += [last_no]
    return eval(''.join(map(str, new_line)))


def find_closure(line):
    # idx is the index of the opening bracket
    depth = 0
    for i, char in enumerate(line):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == 0 and i != 0:
            return i


async def parse_lines_1(lines):
    tasks = [parse_line(line) for line in lines if line]
    return await asyncio.gather(*tasks)


async def parse_lines_2(lines):
    tasks = [parse_line_2(line) for line in lines if line]
    return await asyncio.gather(*tasks)


def main():
    start_time = time.time()
    with open('input_18.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    results = asyncio.run(parse_lines_1(lines))
    part_1 = sum(results)
    print(f"Part One: {part_1}")
    results = asyncio.run(parse_lines_2(lines))
    part_2 = sum(results)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
