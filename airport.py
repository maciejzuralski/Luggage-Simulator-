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

        # starting airport sorting room error rate, range 0.1% - 0.2%
        self.sorting_error_rate = random.random() * 0.001 + 0.001

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

        for luggage in new_flight.luggage:
            luggage.arrival_airport = destination.ICAO

            # chance that luggage will go missing
            if (random.random() < self.sorting_error_rate +
                    self.now_working.error_rate +
                    luggage.sorted_dt_in_minutes / 80):
                # self.missing_luggage(luggage)
                new_flight.luggage.remove(luggage)

        self.flights.append(new_flight)

    def missing_luggage(self, luggage):
        pass

    def issuing_to_long(self, luggage):
        pass

    def add_new_luggage(self, t):
        new_luggage = [Luggage(t, self.ICAO) for _ in range(random.randint(0, self.rate_of_travelers))]
        return new_luggage

    def flight_arrival(self, flight, t):
        issuing_t = random.random() * (len(flight.luggage) ** 2) / 2040
        for luggage in flight.luggage:
            luggage.arrival_t = t
            luggage.issuing_t = issuing_t
            if random.random() * 30 < issuing_t - 30:
                self.issuing_to_long(luggage)

        flight.luggage = None

    def update(self, airports, t):
        # chance for a new flight departure
        while random.random() < len(self.luggage_waiting) / 500:
            self.create_new_flight(airports)

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
