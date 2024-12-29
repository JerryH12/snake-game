"""
Snake med Turtle.
Webbsida:
https://medium.com/@wepypixel/step-by-step-guide-python-code-for-snake-game-development-3e0ec9f7522e

Idén är att använda bredd-först algoritm för att spela Snake. Spelplanen är indelad i 900 rutor.
Övre vänstra hörnet ruta 0 och 899 nere till höger. För att köra algoritmen skapas en graf med noder
där man söker efter kortaste vägen.


"""

import turtle
import time
import random
import copy
from random import choice

# Simple node structure with useful properties.
class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.root = None
 
# Create a graph
class Graph: 
    def __init__(self):     
        self.vertices = set()
        self.edges = set()
              
        # the screen is going to be represented by 30x30 or 900 vertices.
        for i in range(900):
            self.vertices.add(i)

        # each edge is a tuple with two connections.
        
        # create horizontal edges.
        for i in range(30):
            for j in range(29):
                self.edges.add((i*30+j, i*30+j+1))
                
        # create vertical edges.
        for i in range(29):
            for j in range(30):
                self.edges.add((i*30+j, (i+1)*30+j))
                
        self.adjacency_list={}
        
        # with each vertex as the key, create an empty list.
        for vertex in self.vertices:
            self.adjacency_list[vertex]=[]
        
        # append adjacent vertices to the list.
        for edge in self.edges:
            v1 = edge[0] # the vertex connected to one side of the edge.
            v2 = edge[1] # the vertex connected to the other side of the edge.
            self.adjacency_list[v1].append(v2)
            self.adjacency_list[v2].append(v1)
            
    def adjacency_list_copy(self):
        return copy.deepcopy(self.adjacency_list)

# shortest path algorithm
def BFS(adjacency_list, root, target):  
    visited = set() # store visited nodes in a set.
    Q = [Node(root)] # create a node object and add to the queue.
    visited.add(root)
    
    while len(Q) > 0:
        v = Q.pop(0) # take the first element out of the queue.
        
        if v.key == target: # Find the shortest path between root and target.
            return v
        
        # visit each child vertex of v that isn't visited already.
        for w in adjacency_list[v.key]:
            if w not in visited:
                visited.add(w)
                current = Node(w) # create a node object.
                current.parent = v # keep a reference for back tracking.
                Q.append(current) # add node object to the end of the queue.
 

delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")

# equivalent of 30x30 squares 
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, -100)
head.direction = "Stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 0)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

G = Graph()

game_on = True

# Functions
def coordinates_to_index(xcor, ycor):
    x = 300 + xcor # Zero from the left side of the screen
    y = 300 - ycor # Zero from the top of the screen
    x_index = int(x / 20)
    y_index = int(y / 20)
    index = y_index * 30 + x_index
    return index

def go_up():
    head.direction = "up"

def go_down():
    head.direction = "down"

def go_left():
    head.direction = "left"

def go_right():
    head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# calculate search path
def new_search_path(adjacency_list):
     head_v = head.position() # returns a 2D vector with head position.
     food_v = food.position() # returns a 2D vector with food position.
     
     # extract coordinates
     head_x = int(head_v[0])
     head_y = int(head_v[1])   
     food_x = int(food_v[0])
     food_y = int(food_v[1])
     
     head_pos = coordinates_to_index(head_x, head_y)
     food_pos = coordinates_to_index(food_x, food_y)
     
     path = BFS(adjacency_list, food_pos, head_pos)
         
     return path

def update_adjacency_list():
    
    # Make a copy of the original list and change the copy.
    adjacency_list = G.adjacency_list_copy()
    for s in segments:
        segment_v = s.position() # 2D vector
        x = int(segment_v[0])
        y = int(segment_v[1])
        segment_pos = coordinates_to_index(x, y)
        
        # Remove locations that the snake is occupying.
        adjacency_list[segment_pos].clear()
        
    return adjacency_list

def random_food_location():
    
    # Avoid the same location as the snake 
    occupied_locations = []
    xcor = int(head.xcor())
    ycor = int(head.ycor())
    occupied_locations.append(coordinates_to_index(xcor, ycor))
    
    for segment in segments:
        x = int(segment.xcor())
        y = int(segment.ycor())
        occupied_locations.append(coordinates_to_index(x, y))
        
    index = choice([i for i in range(0, 900) if i not in occupied_locations])
    
    # Index to coordinates
    x_col = float(index % 30) 
    y_row = (index - x_col) / 30
    
    x_pos = x_col * 20 - 300
    y_pos = 300 - y_row * 20
    
    if x_pos < -280:
        x_pos = -280
    if x_pos > 280:
        x_pos = 280
    if y_pos < -280:
        y_pos = -280
    if y_pos > 280:
        y_pos = 280
        
    food.goto(x_pos, y_pos)
    
def on_quit():
    global game_on
    game_on = False

wn._root.protocol("WM_DELETE_WINDOW", on_quit) 

adjacency_list = G.adjacency_list_copy()
path = new_search_path(adjacency_list)

# Main game loop
while game_on:
    wn.update()
    
    adjacency_list = update_adjacency_list()
    
    if path != None:         
        if path.parent is None: # Reached the goal
                  
            random_food_location() # New food somewhere on the screen
            
            # Add a segment to the snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            path = new_search_path(update_adjacency_list())
            
            # Shorten the delay
            delay -= 0.001

            # Increase the score
            score += 10

            if score > high_score:
                high_score = score

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
         
        if path != None:
            if path.parent is not None: # Continue towards the goal
                node = path.parent
            
                if node.key == path.key - 1:
                    go_left()
                
                if node.key == path.key + 1:
                    go_right()
                
                if node.key == path.key - 30:
                    go_up()
                
                if node.key == path.key + 30:
                    go_down()
                
                path = node
                
    # Check for a collision with the border
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        
       
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "Stop"
        
        random_food_location() # Place food somewhere on the screen
        
        path = new_search_path(update_adjacency_list())

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
        
    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    
    move()

    # Check for a collision with the body
    
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    
    path = new_search_path(update_adjacency_list())
    
    time.sleep(delay)  

turtle.bye()

  