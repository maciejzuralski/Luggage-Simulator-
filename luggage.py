import random
import string
import uuid

from datetime import datetime, timedelta


def generate_name(length=10):
    # first letter uppercase, rest lowercase
    word = random.choice(string.ascii_uppercase)
    for _ in range(length - 1):
        word += random.choice(string.ascii_lowercase)
    return word


class Luggage:
    def __init__(self, t, departure_airport):
        # client
        self.client_id = uuid.uuid4()
        self.client_name = generate_name(random.randint(5, 15))
        self.client_surname = generate_name(random.randint(10, 20))
        # worker
        self.acceptance_worker_id = None
        self.issuing_worker_id = None

        # luggage
        self.id = uuid.uuid4()
        self.flight = ''
        self.departure_airport = departure_airport
        self.arrival_airport = ''
        self.mass = random.random() * 18 + 2
        # datatime
        self.acceptance_t = t - timedelta(minutes=random.randint(0, 30))
        self.arrival_t = ''
        # in minutes
        self.sorting_t = random.randint(1, 20)
        self.issuing_t = ''

    def luggage(self, reclaimed):
        return (str(self.id) + '|' +
                str(self.client_id) + '|' +
                str(self.acceptance_worker_id) + '|' +
                str(self.issuing_worker_id) + '|' +
                str(self.mass) + '|' +
                random.choice(['A', 'B', 'C']) + '|' +
                self.departure_airport + '|' +
                self.arrival_airport + '|' +
                self.flight + '|' +
                str(self.acceptance_t) + '|' +
                str(self.acceptance_t + timedelta(minutes=self.sorting_t)) + '|' +
                str(self.arrival_t) + '|' +
                str(self.arrival_t + timedelta(minutes=self.issuing_t)) + '|' +
                str(reclaimed) + '\n')

    def arrive(self, t):
        self.arrival_t = t
        self.issuing_t = random.randint(1, 20)

    def complain(self):
        if self.issuing_t is not '':
            return ('|' + str(self.client_id) + '|' +
                str(self.id) + '|' +
                str(self.arrival_t + timedelta(minutes=self.issuing_t + 5)) + '|')
        else:
            return ('|' + str(self.client_id) + '|' +
                    str(self.id) + '|' +
                    str(None) + '|')

    def client(self):
        return str(self.client_id) + '|' + self.client_name + '|' + self.client_surname + '|1|1\n'
