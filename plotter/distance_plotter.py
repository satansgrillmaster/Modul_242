import math
import turtle
from PIL import Image


class DistancePlotter:
    def __init__(self, num_distances, distances):
        self.num_distances = num_distances
        self.distances = distances
        self.angle_step = 360 / num_distances
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.screen = turtle.Screen()  # Get the turtle screen
        self.right_distances = []
        self.left_distances = []

    def calculate_coordinates(self, distances):
        angle_step = 360 / len(distances)
        left_coordinates = []
        right_coordinates = []

        for i, distance in enumerate(distances):
            angle = i * angle_step
            try:
                x = distance[0] * math.cos(math.radians(angle))
                y = distance[0] * math.sin(math.radians(angle))
                left_coordinates.append((x, y))
                self.left_distances.append(distance[0])
            except:
                x = distance[1] * math.cos(math.radians(angle))
                y = distance[1] * math.sin(math.radians(angle))
                right_coordinates.append((x, y))
                self.right_distances.append(distance[1])

        return left_coordinates, right_coordinates

    def shoelace_formula(self, coordinates):
        n = len(coordinates)
        area = 0

        for i in range(n):
            j = (i + 1) % n
            area += coordinates[i][0] * coordinates[j][1]
            area -= coordinates[j][0] * coordinates[i][1]

        area = abs(area) / 2
        return area

    def draw(self, coordinates):
        self.turtle.goto(coordinates[0])
        self.turtle.pendown()
        for coord in coordinates[1:]:
            self.turtle.goto(coord)
        self.turtle.goto(coordinates[0])
        self.turtle.penup()

    def draw_center_to_first_point(self, coordinates):
        self.turtle.goto(0, 0)
        self.turtle.pendown()
        self.turtle.pencolor("green")
        self.turtle.goto(coordinates[0])
        self.turtle.penup()
        self.turtle.pencolor("black")  # Reset the pen color to black

    def draw_directions(self):
        self.turtle.penup()
        self.turtle.goto(-370, 0)
        self.turtle.write("3m", font=("Arial", 16, "bold"))
        self.turtle.goto(370, 0)
        self.turtle.write("3m", font=("Arial", 16, "bold"))
        self.turtle.goto(0, 370)
        self.turtle.write("3m", font=("Arial", 16, "bold"))
        self.turtle.goto(0, -370)
        self.turtle.write("3m", font=("Arial", 16, "bold"))

    def draw_axes(self):
        self.turtle.penup()
        self.turtle.pencolor("black")
        self.turtle.goto(-350, 0)
        self.turtle.pendown()
        self.turtle.goto(350, 0)
        self.turtle.penup()
        self.turtle.goto(0, -350)
        self.turtle.pendown()
        self.turtle.goto(0, 350)
        self.turtle.penup()

    def save_as_png(self, filename):
        cv = turtle.getcanvas()
        cv.postscript(file=filename, colormode="color")
        try:
            img = Image.open(filename)
            img.save("test.png")
        except ImportError:
            print("PIL library not installed, saved as .eps")

    def calculate_and_draw(self, distances):
        left_coordinates, right_coordinates = self.calculate_coordinates(distances)
        area_left = self.shoelace_formula(left_coordinates)
        area_right = self.shoelace_formula(right_coordinates)
        print("Fläche links:", area_left)
        print("Fläche rechts:", area_right)

        first_distance = distances[0]
        last_distance = distances[180]
        print("Erste Distanz:", first_distance[0])
        print("Letzte Distanz:", last_distance[1])

        left_min_distance = min(distance for distance in self.left_distances)
        right_min_distance = min(distance for distance in self.right_distances)
        print("Kleinste Distanz links:", left_min_distance)
        print("Kleinste Distanz rechts:", right_min_distance)

        self.draw_axes()  # Draw the coordinate system
        self.draw(left_coordinates)
        self.draw_center_to_first_point(left_coordinates)  # Add this line to draw the green line
        self.draw(right_coordinates)
        self.draw_center_to_first_point(right_coordinates)  # Add this line to draw the green line
        self.draw_directions()  # Draw the directions
        # self.save_as_png("output")  # Save the output as a PNG file
        self.screen.mainloop()  # Remove the exit_on_click function and use mainloop() to keep the window open
