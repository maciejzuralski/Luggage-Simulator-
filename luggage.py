import random
import string
import uuid

from datetime import datetime, timedelta


def generate_name(length=10):
    # first letter uppercase, rest lowercase
    word = ''.join(random.choice(string.ascii_uppercase))
    word.join(random.choice(string.ascii_lowercase) for _ in range(length - 1))
    return word


class Luggage:
    def __init__(self, t, departure_airport):
        # client
        self.client_id = uuid.uuid4()
        self.client_name = generate_name(random.randint(5, 15))
        self.client_surname = generate_name(random.randint(10, 20))

        # luggage
        self.id = uuid.uuid4()
        self.reclaim = True
        self.flight = None
        self.departure_airport = departure_airport
        self.arrival_airport = None
        # datatime
        self.acceptance_t = t - timedelta(minutes=random.randint(0, 30))
        self.arrival_t = None
        # in minutes
        self.sorting_t = random.randint(1, 20)

    def arrive(self, t):
        self.arrival_t = t
        self.issuing_t = random.randint(1, 20)
