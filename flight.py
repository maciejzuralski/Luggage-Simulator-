import random
import string
import uuid
import pygame as pg


def generate_unique_code():
    unique_id = ''
    for _ in range(3):
        unique_id += random.choice(string.ascii_uppercase)
    for _ in range(4):
        unique_id += random.choice(string.digits)
    return unique_id


class Flight:
    def __init__(self, flights, starting_airport, destination_airport, t):
        self.flights = flights
        self.name = generate_unique_code()
        self.position = pg.Vector2(starting_airport.getPosition())
        self.starting_airport = starting_airport
        self.destination_airport = destination_airport
        self.luggage_number = random.randint(100, 350)
        self.departure_t = t
        self.luggage = []

    def flight_to_csv(self, t):
        buffer = (self.name + ',' +
                  random.choice(['Rayaner', 'Wizzar', 'Lot']) + ',' +
                  self.starting_airport.ICAO + ',' +
                  self.destination_airport.ICAO + ',' +
                  self.destination_airport.ICAO + ',' +
                  str(len(self.luggage)) + ',' +
                  str(random.randint(1000, 9999)) + ',' +
                  str(self.departure_t) + ',' +
                  str(t) + '\n')
        with open('flight_exel.txt', 'a') as file:
            file.write(buffer)

    def update(self, t):
        self.position = self.position.move_towards(self.destination_airport.getPosition(), 10)
        if (self.position.x == self.destination_airport.position.x and
                self.position.y == self.destination_airport.position.y):
            self.destination_airport.add_luggage_for_issuing(self.luggage)
            self.destination_airport.flight_arrival(self, t)

            self.flight_to_csv(t)

            self.luggage = None
            self.flights.remove(self)

    def render(self, screen):
        pg.draw.circle(screen, (0, 255, 0), self.position, 3)

    def getLuggageNumber(self):
        return self.luggage_number
