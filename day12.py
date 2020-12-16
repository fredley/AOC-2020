import asyncio
import time

EAST = (0, 1)
WEST = (0, -1)
NORTH = (-1, 0)
SOUTH = (1, 0)

TURNS = (NORTH, EAST, SOUTH, WEST)

DIRECTIONS = {
    'N': NORTH,
    'S': SOUTH,
    'W': WEST,
    'E': EAST
}


async def parse_line(line):
    return (line[0], int(line[1:]))


async def parse_lines(lines):
    tasks = [parse_line(line) for line in lines if line]
    return await asyncio.gather(*tasks)


def process_directions(directions):
    pos = (0, 0)
    facing = EAST
    for direction in directions:
        if direction[0] == 'F':
            pos = move_forward(pos, facing, direction[1])
        elif direction[0] in {'L', 'R'}:
            facing = turn(facing, direction)
        else:
            pos = move_lateral(pos, direction)
    return abs(pos[0]) + abs(pos[1])


def move_forward(pos, facing, amount):
    return (pos[0] + facing[0] * amount, pos[1] + facing[1] * amount)


def turn(facing, direction):
    facing_before = TURNS.index(facing)
    clockwise = {'L': -1, 'R': 1}[direction[0]]
    return TURNS[(facing_before + clockwise * (direction[1] // 90)) % len(TURNS)]


def move_lateral(pos, direction):
    move = DIRECTIONS[direction[0]]
    return (pos[0] + move[0] * direction[1], pos[1] + move[1] * direction[1])


def process_waypoints(directions):
    ship_pos = (0, 0)
    waypoint_pos = (-1, 10)  # relative?
    for direction in directions:
        if direction[0] == 'F':
            ship_pos = move_to_waypoint(ship_pos, waypoint_pos, direction[1])
        elif direction[0] in {'L', 'R'}:
            waypoint_pos = rotate_waypoint(ship_pos, waypoint_pos, direction)
        else:
            waypoint_pos = move_lateral(waypoint_pos, direction)
    return abs(ship_pos[0]) + abs(ship_pos[1])


def move_to_waypoint(ship_pos, waypoint_pos, times):
    return (ship_pos[0] + waypoint_pos[0] * times, ship_pos[1] + waypoint_pos[1] * times)


def rotate_waypoint(ship_pos, waypoint_pos, direction):
    clockwise = {'L': -1, 'R': 1}[direction[0]]
    times = direction[1] // 90
    for _ in range(times):
        waypoint_pos = (waypoint_pos[1] * clockwise, waypoint_pos[0] * -1 * clockwise)
    return waypoint_pos


def main():
    start_time = time.time()
    with open('input_12.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    directions = asyncio.run(parse_lines(lines))
    part_1 = process_directions(directions)
    print(f"Part One: {part_1}")
    part_2 = process_waypoints(directions)
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
