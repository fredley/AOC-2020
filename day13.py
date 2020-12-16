import time


def find_next_bus(timestamp, busses):
    best_next_time = timestamp
    best_next_bus = None
    for bus in busses:
        if bus == 'x':
            continue
        bus_no = int(bus)
        next_time = bus_no - (timestamp % bus_no)
        if next_time < best_next_time:
            best_next_time = next_time
            best_next_bus = bus_no
    return best_next_bus * best_next_time


def solve_busses(busses):
    """
    Find a number n such that N is a multiple of b1, N - 27 is a multiple of 41

    N % 37 == 0, N % 41 == 27, N % 457 == 37

    High dimensional intersection?

    FInd highest and test??
    """
    offset = 0
    ns = []
    mods = []
    for bus in busses:
        if bus == 'x':
            offset -= 1
            continue
        ns.append(int(bus))
        mods.append(offset)
        offset -= 1
    return chinese_remainder(ns, mods)


def chinese_remainder(ns, mods):
    accumulator = 0
    product = 1
    for n in ns:
        product *= n
    for n, mod in zip(ns, mods):
        p = product // n
        accumulator += mod * multiplicative_inverse(p, n) * p
    return accumulator % product


def multiplicative_inverse(a, b):
    if b == 1:
        return 1
    b0 = b
    x0, x1 = 0, 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def main():
    start_time = time.time()
    with open('input_13.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    timestamp = int(lines[0])
    busses = lines[1].split(",")
    part_1 = find_next_bus(timestamp, busses)
    print(f"Part One: {part_1}")
    part_2 = solve_busses(busses)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
