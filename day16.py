import asyncio
import time


async def get_error_rate(rule_lines, ticket_lines):
    rules = await asyncio.gather(*[parse_rule(rule_line) for rule_line in rule_lines.split("\n")])
    tickets = await asyncio.gather(*[parse_ticket(ticket_line) for ticket_line in ticket_lines.split("\n")[1:]])
    errors = await asyncio.gather(*[get_ticket_error_rate(ticket, rules) for ticket in tickets])
    valid_tickets = [ticket for ticket, score in errors if score == 0]
    error_rate = sum(error[1] for error in errors)
    return (
        error_rate, rules,
        valid_tickets
    )


async def parse_rule(rule_line):
    name, ranges = rule_line.split(": ")
    output_ranges = []
    for r in ranges.split(" or "):
        lower, upper = r.split("-")
        output_ranges.append((int(lower), int(upper)))
    return name, output_ranges


async def parse_ticket(ticket_line):
    return list(map(int, ticket_line.split(",")))


def is_valid(ticket, rules):
    valid = False
    for n in ticket:
        valid = False
        for rule in rules:
            for r in rule[1]:
                if r[0] <= n <= r[1]:
                    valid = True
                    break
            if valid:
                break
    return valid


async def get_ticket_error_rate(ticket, rules):
    error = 0
    for n in ticket:
        valid = False
        for rule in rules:
            for r in rule[1]:
                if r[0] <= n <= r[1]:
                    valid = True
                    break
            if valid:
                break
        else:
            error += n
    return ticket, error


def value_valid(value, rule):
    return any(r[0] <= value <= r[1] for r in rule[1])


async def get_departure_score(rules, valid_tickets, your_ticket):
    rule_positions = {rule[0]: set() for rule in rules}
    positions = range(len(valid_tickets[0]))

    for position in positions:
        for rule in rules:
            if all(value_valid(ticket[position], rule) for ticket in valid_tickets):
                rule_positions[rule[0]].add(position)

    final_positions = {}

    for _ in range(len(positions)):
        for rule, positions in rule_positions.items():
            if len(positions) == 1:
                final_position = list(positions)[0]
                final_positions[rule] = final_position
                for s in rule_positions.values():
                    if final_position in s:
                        s.remove(final_position)
                break

    checksum = 1
    for rule, value in final_positions.items():
        if rule.startswith('departure '):
            checksum *= your_ticket[0][value]
    return checksum


def main():
    start_time = time.time()
    with open('input_16.txt') as f:
        puzzle_input = f.read().strip()
    rule_lines, your_ticket, nearby_tickets = puzzle_input.split("\n\n")
    part_1, rules, valid_tickets = asyncio.run(get_error_rate(rule_lines, nearby_tickets))
    print(f"Part One: {part_1}")
    _, _, your_tickets = asyncio.run(get_error_rate(rule_lines, your_ticket))
    valid_tickets.extend(your_tickets)
    part_2 = asyncio.run(get_departure_score(rules, valid_tickets, your_tickets))
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
