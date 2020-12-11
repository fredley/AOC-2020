import asyncio
from collections import defaultdict
import time


async def parse_line(y, line, seating_map):
    for x, seat in enumerate(line):
        seating_map[x][y] = seat


async def parse_map(lines):
    seating_map = defaultdict(dict)
    await asyncio.gather(*[parse_line(idx, line, seating_map) for idx, line in enumerate(lines) if line])
    return seating_map


def count_occupied(seating_map):
    return sum([sum([1 for y in col.values() if y == '#']) for col in seating_map.values()])


def get_state(seating_map):
    return str(seating_map)


def iterate_1(seating_map):
    width = len(seating_map.keys())
    height = len(seating_map[0].keys())
    new_map = defaultdict(dict)
    for x in range(width):
        for y in range(height):
            current_state = seating_map[x][y]
            if current_state == '.':
                new_map[x][y] = '.'
                continue
            adjacent_occupied = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    if seating_map.get(x + i, {}).get(y + j) == '#':
                        adjacent_occupied += 1
            if current_state == 'L' and adjacent_occupied == 0:
                new_map[x][y] = '#'
            elif current_state == '#' and adjacent_occupied >= 4:
                new_map[x][y] = 'L'
            else:
                new_map[x][y] = seating_map[x][y]
    # render_map(new_map)
    return new_map


def find_occupied_in_dir(seating_map, x, y, i, j):
    pos_x = x + i
    pos_y = y + j
    while True:
        seat = seating_map.get(pos_x, {}).get(pos_y)
        if seat is None:
            return 0
        if seat == '#':
            return 1
        if seat == 'L':
            return 0
        else:
            pos_x += i
            pos_y += j


def iterate_2(seating_map):
    width = len(seating_map.keys())
    height = len(seating_map[0].keys())
    new_map = defaultdict(dict)
    for x in range(width):
        for y in range(height):
            current_state = seating_map[x][y]
            if current_state == '.':
                new_map[x][y] = '.'
                continue
            adjacent_occupied = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    adjacent_occupied += find_occupied_in_dir(seating_map, x, y, i, j)
            if current_state == 'L' and adjacent_occupied == 0:
                new_map[x][y] = '#'
            elif current_state == '#' and adjacent_occupied >= 5:
                new_map[x][y] = 'L'
            else:
                new_map[x][y] = seating_map[x][y]
    # render_map(new_map)
    return new_map


def render_map(seating_map):
    width = len(seating_map.keys())
    height = len(seating_map[0].keys())
    for y in range(height):
        for x in range(width):
            print(seating_map[x][y], end="")
        print()
    print()


def find_stable_state(seating_map, iter_fn):
    seen_states = set()
    while True:
        seating_map = iter_fn(seating_map)
        state = get_state(seating_map)
        if state in seen_states:
            break
        seen_states.add(state)
    return count_occupied(seating_map)


def main():
    start_time = time.time()
    with open('input_11.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    seating_map = asyncio.run(parse_map(lines))
    part_1 = find_stable_state(seating_map, iterate_1)
    print(f"Part One: {part_1}")
    part_2 = find_stable_state(seating_map, iterate_2)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
