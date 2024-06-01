import random


def choice_items(items: list) -> list:
    result = []
    for _ in range(4):
        item = random.choice(items)
        if item not in result:
            result.append(item)
    return result
