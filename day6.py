import asyncio
from collections import defaultdict
import string
import time


async def count_answers(line):
    return len(set(line).difference(" ", "\n"))


async def sum_questions(lines):
    tasks = [asyncio.ensure_future(count_answers(line)) for line in lines if line]
    return sum(await asyncio.gather(*tasks))


async def count_all_answers(line):
    results = None
    rows = line.split("\n")
    for row in rows:
        if not row:
            continue
        if results is None:
            results = set(row)
        else:
            results = results.intersection(row)
    return len(results)


async def sum_all_questions(lines):
    tasks = [asyncio.ensure_future(count_all_answers(line)) for line in lines if line]
    return sum(await asyncio.gather(*tasks))


def main():
    start_time = time.time()
    with open('input_6.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n\n")
    part_1 = asyncio.get_event_loop().run_until_complete(sum_questions(lines))
    print(f"Part One: {part_1}")
    part_2 = asyncio.get_event_loop().run_until_complete(sum_all_questions(lines))
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
