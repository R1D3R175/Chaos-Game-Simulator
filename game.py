#!/usr/bin/python

import argparse
import random
import turtle
import os

# Create argparse which takes 
# a parameter seed
# a parameter size
# a parameter points
# a parameter divider
# a parameter rolls
parser = argparse.ArgumentParser()
parser.add_argument("--seed", help="seed for random number generator", required=False, default=os.urandom(32))
parser.add_argument("--size", help="size of the grid", required=False, nargs=2, default=[800, 800], type=int)
parser.add_argument("--points", help="number of points of the polygon", required=False, default=3, type=int)
parser.add_argument("--divider", help="divider for the distance between random point and random-choosen point", required=False, default=2, type=int)
parser.add_argument("--rolls", help="number of random points to draw", required=False, default=10000000, type=int)
args = parser.parse_args()

class Game:
    def __init__(self, size, seed, points, divider, rolls):
        self._width = size[0] if size[0] % 2 == 0 else size[0] + 1
        self._height = size[1] if size[1] % 2 == 0 else size[1] + 1
        self._divider = divider
        self._rolls = rolls
        random.seed(seed)

        # Seed point
        self._seed_point = self._gen_coord() + (self._gen_color(),)

        # Generate points random coordinates
        self._points = [self._gen_points() for _ in range(points)]

        # Initialize turtle screen with self width and height
        self._screen = turtle.Screen()
        self._screen.setup(self._width, self._height)

        # Initialize turtle
        self._turtle = turtle.Turtle()
        self._turtle.hideturtle()
        self._turtle.speed(0)

    def _gen_points(self):
        """ Generates the points and assign them a color """
        x, y = self._gen_coord()
        z = self._gen_color()
        return (x, y, z)

    def _gen_color(self):
        """ Generates a random color (in hex) """
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def _gen_coord(self):
        """ Generates a random coordinate within the grid """
        return (random.randint(-(self._width / 2), self._width/2), random.randint(-(self._height / 2), self._height/2))
    
    def _draw_dot(self, x, y, color="#000000"):
        """ Draws a dot at the given x and y coordinates """
        self._turtle.penup()
        self._turtle.goto(x, y)
        self._turtle.pendown()
        self._turtle.dot(5, color)

    def _draw_starters(self):
        """ Draws the starters dots with their color and the seed point """
        for point in self._points:
            # print("[DEBUG] Drawing point: {}".format(point))
            self._draw_dot(point[0], point[1], point[2])

        self._draw_dot(self._seed_point[0], self._seed_point[1])

    def _get_new_coord(self, last_dot):
        """ Gets a new coordinate based on the last dot """
        x, y, _ = last_dot
        a, b, c = random.choice(self._points)

        # Get the new x and y coordinates
        x = int((x + a) // self._divider)
        y = int((y + b) // self._divider)

        # Return the new coordinates and the color of the point picked

        # print("[DEBUG] New coordinates: {}".format((x, y, c)))

        return (x, y, c)

    def _chaos(self):
        """ Draws the chaos """
        last_dot = self._seed_point
        for _ in range(self._rolls):
            last_dot = self._get_new_coord(last_dot)
            self._draw_dot(last_dot[0], last_dot[1], last_dot[2])
            
    def start(self):
        """ Starts the game """
        self._draw_starters()
        self._chaos()
        print("[INFO] Finished drawing chaos")
        self._screen.mainloop()

# For Debug purposes
if __name__ == '__main__':
    game = Game(args.size, args.seed, args.points, args.divider, args.rolls)
    game.start()