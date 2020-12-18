from collections import defaultdict
import time


def parse_state(inpt):
    layer = defaultdict(dict)
    for y, row in enumerate(inpt.split("\n")):
        for x, char in enumerate(row):
            layer[x][y] = char
    return {0: layer, 'generations': 0, 'min_x': 0, 'max_x': x, 'min_y': 0, 'max_y': y}


def count_hyper_world(world):
    total = 0
    for w in range(-1 * world['generations'], world['generations'] + 1):
        world[w]['generations'] = world['generations']
        total += count_world(world[w])
    return total


def count_world(world):
    total = 0
    for z in range(-1 * world['generations'], world['generations'] + 1):
        total += count_layer(world[z])
    return total


def count_layer(layer):
    total = 0
    for col in layer.values():
        for point in col.values():
            total += 1 if point == '#' else 0
    return total


def run_world(world, n):
    for _ in range(n):
        world = step_world(world)
    return world


def step_world(world):
    generation = world['generations'] + 1
    new_world = {
        'generations': generation,
        'min_x': world['min_x'] - 1,
        'max_x': world['max_x'] + 1,
        'min_y': world['min_y'] - 1,
        'max_y': world['max_y'] + 1
    }
    for z in range(-1 * generation, generation + 1):
        new_world[z] = defaultdict(dict)
        for x in range(new_world['min_x'], new_world['max_x'] + 1):
            for y in range(new_world['min_y'], new_world['max_y'] + 1):
                new_world[z][x][y] = compute_cell(world, z, x, y)
    return new_world


def compute_cell(world, z, x, y):
    alive = 0
    currently_alive = None
    for dz in range(-1, 2):
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dz == dy == dx == 0:
                    currently_alive = world.get(z, {}).get(x, {}).get(y) == '#'
                    continue
                alive += 1 if world.get(z + dz, {}).get(x + dx, {}).get(y + dy) == '#' else 0
    return '#' if (currently_alive and alive in {2, 3}) or (not currently_alive and alive == 3) else '.'


def run_hyper_world(world, n):
    hyper_world = {
        'generations': world['generations'],
        'min_x': world['min_x'],
        'max_x': world['max_x'],
        'min_y': world['min_y'],
        'max_y': world['max_y'],
        0: world
    }
    for _ in range(n):
        hyper_world = step_hyper_world(hyper_world)
    return hyper_world


def step_hyper_world(world):
    new_world = {
        'generations': world['generations'] + 1,
        'min_x': world['min_x'] - 1,
        'max_x': world['max_x'] + 1,
        'min_y': world['min_y'] - 1,
        'max_y': world['max_y'] + 1
    }
    for w in range(-1 * new_world['generations'], new_world['generations'] + 1):
        new_world[w] = {}
        for z in range(-1 * new_world['generations'], new_world['generations'] + 1):
            new_world[w][z] = defaultdict(dict)
            for x in range(new_world['min_x'], new_world['max_x'] + 1):
                for y in range(new_world['min_y'], new_world['max_y'] + 1):
                    new_world[w][z][x][y] = compute_hyper_cell(world, w, z, x, y)
    return new_world


def compute_hyper_cell(world, w, z, x, y):
    alive = 0
    currently_alive = None
    for dw in range(-1, 2):
        for dz in range(-1, 2):
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dw == dz == dy == dx == 0:
                        currently_alive = world.get(w, {}).get(z, {}).get(x, {}).get(y) == '#'
                        continue
                    alive += 1 if world.get(w + dw, {}).get(z + dz, {}).get(x + dx, {}).get(y + dy) == '#' else 0
    return '#' if (currently_alive and alive in {2, 3}) or (not currently_alive and alive == 3) else '.'


def main():
    start_time = time.time()
    with open('input_17.txt') as f:
        puzzle_input = f.read().strip()
    state = parse_state(puzzle_input)
    part_1 = count_world(run_world(state, 6))
    print(f"Part One: {part_1}")
    part_2 = count_hyper_world(run_hyper_world(state, 6))
    print(f"Part Two: {part_2}")
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
