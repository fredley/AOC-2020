import asyncio
import time

REQUIRED_FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')


async def validate_passport(passport):
    for field in REQUIRED_FIELDS:
        if field + ':' not in passport:
            return 0
    return 1


async def validate_plus_passport(passport):
    dct = {}
    for line in passport.split("\n"):
        for phrase in line.split(" "):
            if not phrase:
                continue
            key, value = phrase.split(":")
            dct[key] = value
    try:
        if not (1920 <= int(dct['byr']) <= 2002):
            return 0
        if not (2010 <= int(dct['iyr']) <= 2020):
            return 0
        if not (2020 <= int(dct['eyr']) <= 2030):
            return 0
        height_units = dct['hgt'][-2:]
        if height_units not in ('in', 'cm'):
            return 0
        height_value = int(dct['hgt'].replace(height_units, ""))
        if height_units == 'in' and not (59 <= height_value <= 76):
            return 0
        if height_units == 'cm' and not (150 <= height_value <= 193):
            return 0
        if dct['hcl'][0] != '#' or int(dct['hcl'][1:], 16) <= 0:
            return 0
        if len(dct['hcl']) != 7:
            return 0
        if dct['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            return 0
        if len(dct['pid']) != 9 or not dct['pid'].isnumeric():
            return 0
    except KeyError as e:
        return 0
    return 1


async def count_valid_passports(inpt, fn):
    tasks = []
    for passport in inpt.split("\n\n"):
        tasks.append(asyncio.ensure_future(fn(passport)))
    return sum(await asyncio.gather(*tasks))


def main():
    start_time = time.time()
    with open('input_4.txt') as f:
        puzzle_input = f.read()
    part_1 = asyncio.get_event_loop().run_until_complete(count_valid_passports(puzzle_input, validate_passport))
    print(f"Part One: {part_1}")
    part_2 = asyncio.get_event_loop().run_until_complete(count_valid_passports(puzzle_input, validate_plus_passport))
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
