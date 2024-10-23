import random
import pygame as pg
import time

from airport import Airport
from datetime import datetime, timedelta

DISPLAY = False


def reset_file(name):
    with open(name, 'w') as file:
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    screen_size = (800, 800)
    flights = []

    reset_file('client.txt')
    reset_file('complaint.txt')
    reset_file('flight_exel.txt')
    reset_file('worker.txt')
    reset_file('worker_exel.txt')
    reset_file('luggage.txt')

    airports = [Airport(screen_size, flights) for _ in range(random.randint(7, 9))]

    pg.init()
    screen = pg.display.set_mode(screen_size)
    pg.display.set_caption("Airport Simulation")

    t = datetime(2000, 1, 1, 0, 0, 0)

    run = True
    pause = False
    while run:

        if pause:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN and event.key == pg.K_n:
                    pause = False
        else:
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
                    if event.type == pg.KEYDOWN and event.key == pg.K_p:
                        pause = True
                        print("PAUSE")

                # update
                for airport in airports:
                    airport.update(airports, t)
                for flight in flights:
                    flight.update(t)

                if DISPLAY:
                    screen.fill((255, 255, 255))  # Fill the screen with black
                    # Display
                    for airport in airports:
                        airport.render(screen)
                    for flight in flights:
                        flight.render(screen)

                    pg.display.update()  # Update the display
                    time.sleep(0.1)    # optional sleep

                t += timedelta(minutes=30)  # adding 30 minutes to datetime

    pg.quit()
