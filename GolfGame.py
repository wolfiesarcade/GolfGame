import random
#we need a function that will start the game. it will print a welcome message and instructions for the game
def StartGame():
  print("Welcome to the Golf Game!")
  print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
  print("Good luck!")
  print("Press any key to start the game.")
  input()
  print("Game started!")

#we need a fuction that will simulate rolling a dice. it will return a random number between 1 and 6
def RollDice():
  return random.randint(1, 6)

# we need to creata function that will create a grid. it will use list comprehension t create a 2D list of '.' characters
def CreateGrid(rows, cols):
  grid = [['.' for _ in range(cols)] for _ in range(rows)]
  return grid
#we neeed to create a function that will place the ball in the last row of the grid. it will place the ball in a random column
def PlaceBall(grid, rows, cols):
    ball_col = random.randint(0, cols - 1)
    grid[rows - 1][ball_col] = 'o'
    return grid

#we need to create a function that will place the hole in the second row of the grid. it will place the hole in a random column
def Hole(grid, cols):
    hole_col = random.randint(0, cols - 1)
    hole_row = random.randint(0, 2)
    grid[hole_row][hole_col] = 'H'
    return grid


# i need to create movement logic for the ball. the player will likely have to decide to split the points rolled by the dice. so if they get a 5, they can move the ball 5 spaces or move it 3 spaces and then 2 spaces. the player will have to decide how to split the points

# i need to create a function that will check if the ball is in the hole. if the ball is in the hole, the game will end and the player will win

# i need to create a function that will check if the ball is out of bounds. if the ball is out of bounds, the player will lose the game

# i need to creat a way to color rows and columns of the grid. the colors will decide of they are in sand or grass. the ball will move slower in sand than in grass

rows = random.randint(10, 20)
cols = random.randint(5, 10)

StartGame()
grid = CreateGrid(rows, cols)
grid = PlaceBall(grid, rows, cols)
grid = Hole(grid, cols)

for row in grid:
    print(' '.join(row))

