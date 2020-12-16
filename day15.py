import time
from collections import defaultdict


def play_until(numbers, turns):
    init = True
    prev_spoken = defaultdict(list)
    previous = None
    turn = 0
    while turn < turns:
        turn += 1
        if init:
            n = numbers[turn - 1]
            previous = n
            prev_spoken[n].append(turn)
            if turn == len(numbers):
                init = False
            continue
        # Consider previous
        if len(prev_spoken[previous]) == 1:
            n = 0
        else:
            n = prev_spoken[previous][0] - prev_spoken[previous][1]
        if prev_spoken.get(n) is None:
            prev_spoken[n] = (turn, )
        else:
            prev_spoken[n] = (turn, prev_spoken[n][0])
        previous = n
    return n


def main():
    start_time = time.time()
    with open('input_15.txt') as f:
        puzzle_input = f.read().strip()
    numbers = list(map(int, puzzle_input.split(",")))
    part_1 = play_until(numbers, 2020)
    print(f"Part One: {part_1}")
    part_2 = play_until(numbers, 30000000)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
