import pygame as pg
import random
import string
import uuid
from worker import Worker
from flight import Flight
from luggage import Luggage


def generate_unique_ICAO(length=4):
    characters = string.ascii_uppercase + string.digits
    unique_id = ''
    for _ in range(length):
        unique_id += random.choice(characters)
    return unique_id


class Airport:
    def __init__(self, screen_size, flights: list[Flight]):
        # access to flights array
        self.flights = flights

        # airport unique ICAO code
        self.ICAO = generate_unique_ICAO()

        # position on map
        self.position = pg.Vector2(random.randint(0, screen_size[0]),
                                   random.randint(0, screen_size[1]))

        # number of max new travelers in 30 min
        self.rate_of_travelers = random.randint(10, 100)
        # bigger airports have bigger radius on map
        self.radius = int(self.rate_of_travelers / 10) + 1

        # starting airport sorting room error rate, range 0.1% - 0.2%
        self.sorting_error_rate = random.random() * 0.001 + 0.001

        # generate workers
        self.workers = [Worker() for _ in range(5)]
        self.now_working = random.choice(self.workers)

        # number of luggage that are waiting for flight
        self.luggage_waiting = []

        # luggage that are waiting for issuing
        self.luggage_for_issuing = []

        # how many luggage in last 3 hours
        self.how_may_luggage = [50, 50, 50, 50, 50, 50]

        self.workers_to_exel()
        self.workers_to_txt()

    def workers_to_exel(self):
        buffer = ''
        for worker in self.workers:
            buffer += (str(worker.id) + ',' +
                       worker.name + ',' +
                       worker.surname + ',' +
                       self.ICAO + ',' +
                       'Obsługa klienta\n')

        with open('worker_exel.txt', 'a') as file:
            file.write(buffer)

    def workers_to_txt(self):
        buffer = ''
        for worker in self.workers:
            buffer += (str(worker.id) + ',' +
                       worker.name + ',' +
                       worker.surname + ',' +
                       self.ICAO + '\n')

        with open('worker.txt', 'a') as file:
            file.write(buffer)

    def create_new_flight(self, airports, t):
        # choice destination
        destination = self
        while destination == self:
            destination = random.choice(airports)

        new_flight = Flight(self.flights, self, destination, t)
        new_flight.luggage = self.luggage_waiting[:new_flight.luggage_number]
        self.luggage_waiting = self.luggage_waiting[new_flight.luggage_number:]

        buffer_complain = ''
        buffer_client = ''
        for luggage in new_flight.luggage:
            luggage.arrival_airport = destination.ICAO
            luggage.acceptance_worker_id = self.now_working.id
            luggage.flight = new_flight.name

            # chance that luggage will go missing
            if (random.random() * 100 < self.sorting_error_rate +
                    self.now_working.error_rate +
                    luggage.sorting_t / 80):
                b1, b2 = self.missing_luggage(luggage)
                buffer_complain += b1
                buffer_client += b2
                new_flight.luggage.remove(luggage)

        with open('complaint.txt', 'a') as file:
            file.write(buffer_complain)
        with open('client.txt', 'a') as file:
            file.write(buffer_client)
        self.flights.append(new_flight)

    def missing_luggage(self, luggage):
        return str(uuid.uuid4()) + luggage.complain() + 'Zgubiony|opis\n', luggage.client()

    def issuing_to_long(self, luggage):
        return str(uuid.uuid4()) + luggage.complain() + 'Zbyt długi czas oczekiwania|opis\n', luggage.client()

    def damaged_luggage(self, luggage):
        return str(uuid.uuid4()) + luggage.complain() + 'Uszkodzony|opis\n', luggage.client()

    def add_new_luggage(self, t):
        new_luggage = [Luggage(t, self.ICAO) for _ in range(random.randint(0, self.rate_of_travelers))]
        return new_luggage

    def flight_arrival(self, flight, t):
        buffer_luggage = ''
        buffer_complain = ''
        buffer_client = ''
        self.how_may_luggage[0] += len(flight.luggage)

        # issuing_t = random.random() * (len(flight.luggage) ** 2) / 2040
        issuing_t = random.random() * sum(self.how_may_luggage) / 10
        damaging_r = random.random() * len(flight.luggage)

        for luggage in flight.luggage:
            luggage.issuing_worker_id = self.now_working.id
            luggage.arrival_t = t
            luggage.issuing_t = issuing_t

            if random.random() * 30000 < damaging_r:
                b1, b2 = self.damaged_luggage(luggage)
                buffer_complain += b1
                buffer_client += b2
            if random.random() * 400 < issuing_t - 20:
                b1, b2 = self.issuing_to_long(luggage)
                buffer_complain += b1
                buffer_client += b2

            buffer_luggage += luggage.luggage(True)
            buffer_client += luggage.client()

        with open('luggage.txt', 'a') as file:
            file.write(buffer_luggage)
        with open('complaint.txt', 'a') as file:
            file.write(buffer_complain)
        with open('client.txt', 'a') as file:
            file.write(buffer_client)

    def update(self, airports, t):
        # new 30 min
        self.how_may_luggage.pop()
        self.how_may_luggage.insert(0, 0)

        # chance for a new flight departure
        while random.random() < len(self.luggage_waiting) / 500:
            self.create_new_flight(airports, t)

        # generate new luggage
        self.luggage_waiting.extend(self.add_new_luggage(t))

    def render(self, screen):
        pg.draw.circle(screen, (0, 0, 0), self.position, self.radius)
        font = pg.font.Font(None, 14)
        text = font.render(self.ICAO, True, (0, 0, 0))
        textPosition = text.get_rect(centerx=self.position[0], y=self.position[1] + self.radius + 2)
        screen.blit(text, textPosition)

    def getPosition(self):
        return self.position

    def add_luggage_for_issuing(self, luggage):
        self.luggage_for_issuing.extend(luggage)

    def add_sorting_error_rate(self, error):
        self.sorting_error_rate += error

        if self.sorting_error_rate <= 0:
            self.sorting_error_rate -= error
