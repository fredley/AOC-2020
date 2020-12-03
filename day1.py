import asyncio
import time


async def get_int(s):
    return int(s)


async def get_ints(strs):
    for s in strs:
        if s:
            yield await get_int(s)


async def parse_ints(inpt):
    return [i async for i in get_ints(inpt.split("\n"))]


async def get_splits(ints):
    for idx, i in enumerate(ints):
        yield i, ints[idx + 1:]


async def test_number(n, ns):
    for test in ns:
        if n + test == 2020:
            return n * test


async def test_splits(n, n2, ns):
    for test in ns:
        if n + n2 + test == 2020:
            yield n * n2 * test


async def test_number_2(n, ns):
    async for n2, nss in get_splits(ns):
        async for test in test_splits(n, n2, nss):
            if test:
                return test


async def find_2020_multiplier(inpt):
    ints = await parse_ints(inpt)
    found_first = False
    found_second = False
    async for n, ns in get_splits(ints):
        result = await test_number(n, ns)
        if result:
            print(f"Part One: {result}")
            found_first = True
        result2 = await test_number_2(n, ns)
        if result2:
            print(f"Part Two: {result2}")
            found_second = True
        if found_first and found_second:
            return


def main():
    start_time = time.time()
    with open('input_1.txt') as f:
        puzzle_input = f.read()
    asyncio.get_event_loop().run_until_complete(find_2020_multiplier(puzzle_input))
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
