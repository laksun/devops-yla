import time


def infinite_loop_function():
    counter = 0
    while True:
        print(f"Loop iteration: {counter}")
        time.sleep(1)
        counter += 1
