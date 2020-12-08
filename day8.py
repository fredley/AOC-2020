import time


def decode_instruction(line):
    instruction, number = line.split(" ")
    return instruction, int(number.replace("+", ""))


def build_instruction_list(lines):
    return [decode_instruction(line) for line in lines if line]


def compute_until_loop(ins):
    acc = 0
    ptr = 0
    used = {k: False for k in range(len(ins))}
    while True:
        if used[ptr]:
            return acc
        used[ptr] = True
        instruction, number = ins[ptr]
        if instruction == 'acc':
            acc += number
            ptr += 1
        elif instruction == 'jmp':
            ptr += number
        else:
            ptr += 1


def compute_until_term(ins):
    acc = 0
    ptr = 0
    while True:
        try:
            instruction, number = ins[ptr]
        except IndexError:
            return acc
        if instruction == 'acc':
            acc += number
            ptr += 1
        elif instruction == 'jmp':
            ptr += number
        else:
            ptr += 1


def replace_instruction(ins, idx, replacement):
    replaced_instruction = (replacement, ins[idx][1])
    return ins[:idx] + [replaced_instruction] + ins[idx + 1:]


def modify_until_success(ins):
    for i, instruction in enumerate(ins):
        if instruction[0] == 'jmp':
            modified_instructions = replace_instruction(ins, i, 'nop')
        elif instruction[0] == 'nop':
            modified_instructions = replace_instruction(ins, i, 'jmp')
        else:
            continue
        try:
            compute_until_loop(modified_instructions)
        except KeyError:
            return compute_until_term(modified_instructions)


def main():
    start_time = time.time()
    with open('input_8.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    ins = build_instruction_list(lines)
    part_1 = compute_until_loop(ins)
    print(f"Part One: {part_1}")
    part_2 = modify_until_success(ins)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
