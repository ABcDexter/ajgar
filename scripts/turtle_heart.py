# trying out my second ever Programming language
import turtle
import time

s = turtle.Screen()    # Create a screen object
s.bgcolor("black")     # Set the background color of the screen to black

t = turtle.Turtle()    # Turtle object
t.speed(1)             # slow speed
t.color("red", "pink") # Set pen and fill colors 
t.begin_fill()         # Begin filling the shape, fill is done once it is a closed shape
t.left(50)             # Turn the turtle left by 50 degrees
t.forward(115)         # Move the turtle forward by 115 units
t.circle(45, 200)      # Draw a circle with radius 45 and extent 200 degrees
t.left(221)            # Turn the turtle left by 221 degrees
t.circle(45, 200)      # Draw another circle with radius 45 and extent 200 degrees
t.forward(115)         # Move the turtle forward by 115 units
t.end_fill()           # End filling the shape, the shape is now filled with the fill color
time.sleep(1)          # Wait for 1 second before closing the window
t.hideturtle()         # Hide the turtle cursor

time.sleep(5)          # Wait for 5 seconds before closing the window