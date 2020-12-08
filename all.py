import importlib
import os
import time


def main():
    start_time = time.time()
    for i in range(1, 26):
        if os.path.exists(f"day{i}.py"):
            mod = importlib.import_module(f"day{i}")
            mod.main()
    print(f"Total Duration: {time.time() - start_time}")


if __name__ == '__main__':
    main()
