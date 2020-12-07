import asyncio
import time

BAGS = {}


class Bag:
    def __init__(self, colour, adjective):
        self.colour = colour
        self.adjective = adjective
        self.children = {}

    def __str__(self):
        return f"{self.colour} {self.adjective}"

    def add_child(self, bag, quantity):
        self.children[bag] = quantity

    def equals(self, other):
        return self.colour == other.colour and self.adjective == other.adjective

    def recursive_contains_bag(self, bag):
        for child in self.children.keys():
            if child.equals(bag):
                return True
            elif child.recursive_contains_bag(bag):
                return True
        return False

    def recursive_count_contents(self):
        count = 0
        for child, quantity in self.children.items():
            count += child.recursive_count_contents() * quantity
        return count + 1


def get_or_create_bag(name):
    if name not in BAGS:
        adjective, colour = name.split(" ")
        BAGS[name] = Bag(colour, adjective)
    return BAGS[name]


async def parse_bag(line):
    first_bag, contents = line.split(" bags contain ")
    bag = get_or_create_bag(first_bag)
    if contents == 'no other bags.':
        return
    for content in contents.split(","):
        number, adjective, colour, _ = content.strip().split(" ")
        sub_bag = get_or_create_bag(adjective + " " + colour)
        bag.add_child(sub_bag, int(number))


async def build_bag_tree(lines):
    tasks = [asyncio.ensure_future(parse_bag(line)) for line in lines if line]
    await asyncio.gather(*tasks)

    tasks = [asyncio.ensure_future(find_shiny_gold(bag)) for bag in BAGS.values()]
    print(f"Part One: {sum(await asyncio.gather(*tasks))}")
    print(f"Part Two: {BAGS['shiny gold'].recursive_count_contents() - 1}")


async def find_shiny_gold(bag):
    if bag.recursive_contains_bag(BAGS['shiny gold']):
        return 1
    return 0


def main():
    start_time = time.time()
    with open('input_7.txt') as f:
        puzzle_input = f.read()
    lines = puzzle_input.split("\n")
    asyncio.get_event_loop().run_until_complete(build_bag_tree(lines))
    print(f"Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
