import asyncio
import time

MEM = {}
MASK = 0


async def parse_line(line):
    if line.startswith('mem'):
        parts = line.split('[')[1].split(']')
        return ('s', int(parts[0]), format(int(parts[1][3:]), "036b"))
    return ('m', line.split(' = ')[1])


async def parse_lines(lines):
    tasks = [parse_line(line) for line in lines if line]
    return await asyncio.gather(*tasks)


def process_instructions(instructions):
    global MASK
    for instruction in instructions:
        if instruction[0] == 'm':
            MASK = instruction[1]
        else:
            MEM[instruction[1]] = apply_mask(instruction[2])
    return sum(MEM.values())


def apply_mask(value):
    output = ''
    for i, c in enumerate(MASK):
        if c == '1':
            output += '1'
        elif c == '0':
            output += '0'
        else:
            output += value[i]
    return int(output, 2)


def process_memory(instructions):
    global MASK
    for instruction in instructions:
        if instruction[0] == 'm':
            MASK = instruction[1]
        else:
            addresses = apply_mem_mask(instruction[1])
            for address in addresses:
                MEM[address] = int(instruction[2], 2)
    return sum(MEM.values())


def apply_mem_mask(address):
    code = format(address, '036b')
    addresses = ['']
    for i, c in enumerate(MASK):
        new_addresses = []
        if c == '1':
            for a in addresses:
                new_addresses.append(a + '1')
                a += '1'
        elif c == '0':
            for a in addresses:
                new_addresses.append(a + code[i])
        else:
            for a in addresses:
                new_addresses.append(a + '1')
                new_addresses.append(a + '0')
        addresses = new_addresses
    return map(to_int, addresses)


def to_int(i):
    return int(i, 2)


def main():
    global MEM
    start_time = time.time()
    with open('input_14.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    instructions = asyncio.run(parse_lines(lines))
    part_1 = process_instructions(instructions)
    print(f"Part One: {part_1}")
    MEM = {}
    part_2 = process_memory(instructions)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
