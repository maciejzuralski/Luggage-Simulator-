import pygame as pg
import random
import string

from worker import Worker
from flight import Flight
from luggage import Luggage


def generate_unique_ICAO(length=4):
    characters = string.ascii_uppercase + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(length))
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

        # starting airport sorting room error rate, range 0.1% - 0.4%
        self.sorting_error_rate = random.random() * 0.003 + 0.001

        # generate workers
        self.workers = [Worker() for _ in range(5)]
        self.now_working = random.choice(self.workers)

        # number of luggage that are waiting for flight
        self.luggage_waiting = []

        # luggage that are waiting for issuing
        self.luggage_for_issuing = []

    def create_new_flight(self, airports):
        # choice destination
        destination = self
        while destination == self:
            destination = random.choice(airports)

        new_flight = Flight(self.flights, self, destination)
        new_flight.luggage = self.luggage_waiting[:new_flight.luggage_number]
        self.luggage_waiting = self.luggage_waiting[new_flight.luggage_number:]

        self.flights.append(new_flight)

    def missing_luggage(self, luggage):
        print("M " + str(luggage.id))

    def add_new_luggage(self):
        new_luggage = [Luggage() for _ in range(random.randint(0, self.rate_of_travelers))]
        for luggage in new_luggage:
            # chance that luggage go missing
            if random.random() < self.sorting_error_rate + self.now_working.error_rate:
                # self.missing_luggage(luggage)
                new_luggage.remove(luggage)
        return new_luggage

    def update(self, airports):
        self.luggage_waiting.extend(self.add_new_luggage())

        # chance for a new flight departure
        while random.random() < len(self.luggage_waiting) / 500:
            self.create_new_flight(airports)

        #

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
