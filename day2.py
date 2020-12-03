import asyncio
import time


async def find_invalid_password(line):
    parts = line.split(" ")
    min_max = parts[0].split("-")
    min_n = int(min_max[0])
    max_n = int(min_max[1])
    letter = parts[1][0]
    return 1 if min_n <= len([l for l in parts[2] if l == letter]) <= max_n else 0


async def find_invalid_password_2(line):
    parts = line.split(" ")
    min_max = parts[0].split("-")
    min_n = int(min_max[0])
    max_n = int(min_max[1])
    letter = parts[1][0]
    try:
        letter_1 = parts[2][min_n - 1]
    except Exception:
        letter_1 = "-"
    try:
        letter_2 = parts[2][max_n - 1]
    except Exception:
        letter_2 = "-"
    return 1 if (letter_1 == letter or letter_2 == letter) and letter_1 != letter_2 else 0


async def find_invalid_passwords(puzzle_input):
    p1_tasks = []
    p2_tasks = []
    lines = puzzle_input.split("\n")
    for line in lines:
        if line:
            p1_tasks.append(asyncio.ensure_future(find_invalid_password(line)))
            p2_tasks.append(asyncio.ensure_future(find_invalid_password_2(line)))
    print(f"Part One: {sum(await asyncio.gather(*p1_tasks))}")
    print(f"Part Two: {sum(await asyncio.gather(*p2_tasks))}")


def main():
    start_time = time.time()
    with open('input_2.txt') as f:
        puzzle_input = f.read()
    asyncio.get_event_loop().run_until_complete(find_invalid_passwords(puzzle_input))
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
