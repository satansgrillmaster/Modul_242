import math
import turtle
from PIL import Image
import time
from enums import QueryMethod, Table

class DistancePlotter:
    def __init__(self, num_distances, distances, db_manager):
        self.num_distances = num_distances
        self.distances = distances
        self.db_manager = db_manager
        self.angle_step = 360 / num_distances
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.screen = turtle.Screen()  # Get the turtle screen
        self.right_distances = []
        self.left_distances = []
        self.left_coordinates_init = []
        self.right_coordinates_init = []

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

    def compare_coordinates(self, coordinates1, coordinates2):
        if len(coordinates1) != len(coordinates2):
            raise ValueError("Die Länge der Koordinatensätze muss gleich sein.")

        differences = []
        for coord1, coord2 in zip(coordinates1, coordinates2):
            x_diff = abs(coord1[0] - coord2[0])
            y_diff = abs(coord1[1] - coord2[1])
            differences.append((x_diff, y_diff))
        print(differences)

        return differences

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

    def calculate_and_draw_init(self, distances):
        left_coordinates, right_coordinates = self.calculate_coordinates(distances)

        first_distance = distances[0]
        last_distance = distances[35]
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

        self.screen.update()  # Update the screen to display the drawings

    def calculate_and_draw(self, distances1, distances2):
        left_coordinates1, right_coordinates1 = self.calculate_coordinates(distances1)
        left_coordinates2, right_coordinates2 = self.calculate_coordinates(distances2)

        differences_left = self.compare_coordinates(left_coordinates1, left_coordinates2)
        differences_right = self.compare_coordinates(right_coordinates1, right_coordinates2)

        self.draw_axes()  # Draw the coordinate system

        for coord1, diff in zip(left_coordinates1, differences_left):
            color = "red" if diff[0] > 5 and diff[1] > 5 else "green"
            self.turtle.pencolor(color)
            self.turtle.goto(coord1)
            self.turtle.pendown()
            self.turtle.dot(5)
            self.turtle.penup()

        for coord1, diff in zip(right_coordinates1, differences_right):
            color = "red" if diff[0] > 5 and diff[1] > 5 else "green"
            self.turtle.pencolor(color)
            self.turtle.goto(coord1)
            self.turtle.pendown()
            self.turtle.dot(5)
            self.turtle.penup()

        self.turtle.pencolor("black")  # Reset the pen color to black
        self.draw_directions()  # Draw the directions

        self.screen.update()  # Update the screen to display the drawings



    def clear_drawing(self):
        self.turtle.clear()
        self.turtle.penup()
        self.right_distances = []
        self.left_distances = []

    def redraw(self, num_distances, distances, distances2):
        self.clear_drawing()
        self.num_distances = num_distances
        self.distances = distances
        self.angle_step = 360 / num_distances
        self.calculate_and_draw(distances, distances2)
        self.db_manager.execute_query(table_name=Table.UPDATE_SENSOR_DATA.value,
                                      query_method=QueryMethod.DELETE,
                                      values={},
                                      )

