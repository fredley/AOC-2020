import asyncio
import time


async def parse_int(s):
    return int(s)


async def parse_ints(lines):
    tasks = [asyncio.create_task(parse_int(line)) for line in lines if line]
    return await asyncio.gather(*tasks)


async def sum_exists(n, candidates):
    for c in candidates:
        if n - c in candidates:
            return True
    return False


async def find_bad_number(lines):
    ints = await parse_ints(lines)
    for i in range(25, len(ints)):
        if await sum_exists(ints[i], set(ints[i - 25:i])):
            continue
        target = ints[i]
        break
    for starter in range(i):
        for ender in range(starter + 1, i):
            sumrange = sum(ints[starter:ender])
            if sumrange == target:
                return target, min(ints[starter:ender]) + max(ints[starter:ender])
            if sumrange > target:
                break


def main():
    start_time = time.time()
    with open('input_9.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    part_1, part_2 = asyncio.run(find_bad_number(lines))
    print(f"Part One: {part_1}")
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
