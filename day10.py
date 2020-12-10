import asyncio
import time


async def parse_int(s):
    return int(s)


async def parse_ints(lines):
    tasks = [asyncio.create_task(parse_int(line)) for line in lines if line]
    return await asyncio.gather(*tasks)


async def jolts(lines):
    adapters = sorted(await parse_ints(lines))
    prev1 = -999
    plus_1 = 0
    plus_3 = 0
    for adapter in adapters:
        if adapter == prev1 + 1:
            plus_1 += 1
        else:
            plus_3 += 1
        prev1 = adapter
    return (plus_1 + 1) * plus_3, adapters


def find_all(adapters):
    return find_upto(adapters[::-1])


FIND_CACHE = {}


def find_upto(adapters):
    """A reversed list of adapters, find the ways to get up to the last point, recursively"""
    first = adapters[0]
    cache = FIND_CACHE.get(first)
    if cache:
        return cache
    if len(adapters) == 1:
        if first >= 4:
            FIND_CACHE[first] = 0
            return 0
        FIND_CACHE[first] = 1
        return 1
    if len(adapters) == 2:
        if first <= 3:
            FIND_CACHE[first] = 2
            return 2
        FIND_CACHE[first] = 1
        return 1
    third = adapters[2]
    if len(adapters) == 3:
        ways = 0
        if first == 3:
            FIND_CACHE[first] = 4
            return 4
        if first - third <= 3:
            ways += find_upto(adapters[2:])
        ways += find_upto(adapters[1:])
        FIND_CACHE[first] = ways
        return ways
    fourth = adapters[3]
    ways = find_upto(adapters[1:])
    if first - third <= 3:
        ways += find_upto(adapters[2:])
    if first - fourth <= 3:
        ways += find_upto(adapters[3:])
    FIND_CACHE[first] = ways
    return ways


def main():
    start_time = time.time()
    with open('input_10.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    part_1, adapters = asyncio.run(jolts(lines))
    print(f"Part One: {part_1}")
    part_2 = find_all(adapters)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
