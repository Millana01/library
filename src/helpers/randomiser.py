from random import randint


def generate_numbers(count: int = 11) -> str:
    numbers_list = [randint(0, 9) for n in range(0, count)]
    return "".join(str(x) for x in numbers_list)
