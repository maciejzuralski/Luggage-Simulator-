import random
import pygame as pg
import time

from airport import Airport
from datetime import datetime, timedelta


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    screen_size = (800, 800)
    flights = []

    airports = [Airport(screen_size, flights) for _ in range(random.randint(5, 10))]

    pg.init()
    screen = pg.display.set_mode(screen_size)
    pg.display.set_caption("Airport Simulation")

    t = datetime(2000, 1, 1, 0, 0, 0)

    run = True
    while run:

        for airport in airports:
            # random change sorting_error_rate
            airport.add_sorting_error_rate(random.random() * 0.0001)
            # random worker for day
            airport.now_working = random.choice(airport.workers)

        # whole loop equals 1 day, and one loop pass equals 30 min
        for min_30 in range(48):

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            # update
            for airport in airports:
                airport.update(airports, t)
            for flight in flights:
                flight.update(t)

            screen.fill((255, 255, 255))  # Fill the screen with black

            # Display
            for airport in airports:
                airport.render(screen)
            for flight in flights:
                flight.render(screen)

            pg.display.update()  # Update the display
            t += timedelta(minutes=30)  # adding 30 minutes to datetime
            time.sleep(0.1)    # optional sleep

    pg.quit()
