import pygame as pg
import random
import string
import uuid


def generate_name(length=10):
    # first letter uppercase, rest lowercase
    word = random.choice(string.ascii_uppercase)
    for _ in range(length - 1):
        word += random.choice(string.ascii_lowercase)
    return word


class Worker:
    def __init__(self):
        self.id = uuid.uuid4()
        self.name = generate_name(random.randint(5, 15))
        self.surname = generate_name(random.randint(10, 20))

        # error rate, range 0.1% - 0.4%
        self.error_rate = random.random() * 0.003 + 0.001
