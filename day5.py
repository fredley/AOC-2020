import asyncio
import time


async def compute_id(seat):
    return seat[0] * 8 + seat[1]


async def find_seat(line):
    lower_row = 0
    upper_row = 127
    lower_col = 0
    upper_col = 7
    for char in line:
        if char == 'F':
            upper_row -= (1 + upper_row - lower_row) // 2
        elif char == 'B':
            lower_row += (1 + upper_row - lower_row) // 2
        elif char == 'L':
            upper_col -= (1 + upper_col - lower_col) // 2
        elif char == 'R':
            lower_col += (1 + upper_col - lower_col) // 2
    return (upper_row, upper_col)


async def find_free_seat(inpt):
    tasks = [asyncio.ensure_future(find_seat(line)) for line in inpt.split("\n") if line]
    taken_seats = await asyncio.gather(*tasks)
    id_tasks = [compute_id(seat) for seat in taken_seats]
    ids = sorted(await asyncio.gather(*id_tasks))
    print(f"Part One: {ids[-1]}")
    prev_seat_id = None
    for seat_id in ids:
        if prev_seat_id is not None and prev_seat_id != seat_id - 1:
            print(f"Part Two: {prev_seat_id}")
            return
        prev_seat_id = seat_id


def main():
    start_time = time.time()
    with open('input_5.txt') as f:
        puzzle_input = f.read()
    asyncio.get_event_loop().run_until_complete(find_free_seat(puzzle_input))
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
