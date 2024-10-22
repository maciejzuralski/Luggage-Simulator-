import random

import pygame as pg


class Flight:
    def __init__(self, flights, starting_airport, destination_airport):
        self.flights = flights
        self.position = pg.Vector2(starting_airport.getPosition())
        self.starting_airport = starting_airport
        self.destination_airport = destination_airport
        self.luggage_number = random.randint(100, 350)
        self.luggage = []

    def update(self, t):
        self.position = self.position.move_towards(self.destination_airport.getPosition(), 10)
        if (self.position.x == self.destination_airport.position.x and
                self.position.y == self.destination_airport.position.y):
            self.destination_airport.add_luggage_for_issuing(self.luggage)
            self.destination_airport.flight_arrival(self, t)
            self.flights.remove(self)

    def render(self, screen):
        pg.draw.circle(screen, (0, 255, 0), self.position, 3)

    def getLuggageNumber(self):
        return self.luggage_number
