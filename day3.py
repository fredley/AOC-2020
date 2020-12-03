import asyncio
import time


async def find_trees_encountered(inpt, slope):
    lines = inpt.split("\n")
    x = 0
    trees = 0
    width = len(lines[0])
    for line in lines:
        if x != int(x):
            x += slope
            continue
        if not line:
            continue
        char = line[int(x) % width]
        if char == '#':
            trees += 1
        x += slope
    return trees


async def find_trees_for_all_slopes(inpt):
    p2_tasks = []
    for slope in [1, 3, 5, 7, 0.5]:
        p2_tasks.append(asyncio.ensure_future(find_trees_encountered(inpt, slope)))
    results = await asyncio.gather(*p2_tasks)
    p2_result = 1
    for result in results:
        p2_result *= result
    return p2_result


def main():
    start_time = time.time()
    with open('input_3.txt') as f:
        puzzle_input = f.read()
    part_1 = asyncio.get_event_loop().run_until_complete(find_trees_encountered(puzzle_input, 3))
    print(f"Part One: {part_1}")
    part_2 = asyncio.get_event_loop().run_until_complete(find_trees_for_all_slopes(puzzle_input))
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
