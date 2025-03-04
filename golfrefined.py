import random
from noise import pnoise2
class GolfCourse:
  
  def __init__(self):
    self.row = 20 #the amount of rows
    self.col = 40 #the amount of colums. id rather do it this way because its cleaner
    self.terrain: list = []
    self.terrain_original: list = []
    
    
  def GenerateGolfCourse(self, scale=10.0):
    for y in range(self.row):
        row = []
        for x in range(self.col):
            value = pnoise2(x / scale, y / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=42)# ask the ai what any of this does i dont know
            if value < -0.05:
                row.append('#')  # Sand
            elif value < 0.05:
                row.append('~')  # water
            else:
                row.append('.')  # fairway
        self.terrain.append(row)
        self.terrain_original.append(row.copy())  # Append a copy of the row to terrain_original
        
        
  def PlaceHole(self): 
    self.hole_row = random.randint (0, 2)
    self.hole_col = random.randint(self.col-3,self.col-1)
    self.terrain [self.hole_row][self.hole_col] = '🕳️'
        
        
class GolfBall:
  def __init__(self, course):
      self.course = course
  
  def PlaceBall(self):
    self.ball_col = random.randint(0, 9)
    self.ball_row: int = self.course.row - 1
    self.course.terrain[self.ball_row][self.ball_col] = '⚪'
  
  
  def BallPosition(self):
     self.ball_position_row = self.ball_row
     self.ball_position_col = self.ball_col    
  

  
class GolfClub:
  def __init__(self, ball, course):
    self.ball = ball
    self.course = course
  def Stroke(self, dice_result):
    self.course.terrain[self.ball.ball_position_row][self.ball.ball_position_col] = self.course.terrain_original[self.ball.ball_position_row][self.ball.ball_position_col]
    #we replace the current ball location with whatever is in the original list
    direction = input("how do you want to move the ball? (up, down, left, right)")
    if direction == "up": 
      self.ball.ball_position_row = self.ball.ball_position_row - self.dice_result
      #we change the internal ball row to the current location minus the dice roll result.
    elif direction == "down":
      self.ball.ball_position_row = self.ball.ball_position_row + self.dice_result
      #we change the internal ball row to the current location plus the dice result.
    elif direction == "left":
      self.ball.ball_position_col = self.ball.ball_position_col - self.dice_result
    elif direction == "right": 
      self.ball.ball_position_col = self.ball.ball_position_col + self.dice_result
      #we change the internal ball column to the current location plus the dice result.
    else:
      print('invalid direction')      
      
    #space_left_up = self.ball_position_row
    #we change the space left up to the current location minus the movement up.
    self.course.terrain[self.ball.ball_position_row] [self.ball.ball_position_col] = '⚪'   
    #we change the new current location to a ball.
    print(f'you moved {direction} {self.dice_result} spaces') 
    #we tell them how many spaces they moved.

  
  
class GameLogic:
  def __init__(self):
      print("Welcome to the Golf Game!")
      print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
      print("Good luck!")
      input("Press any key to start the game.")
      print("Game started!")
  
      self.course = GolfCourse()
      self.ball = GolfBall(self.course)
      self.club = GolfClub(self.ball, self.course)

  def Dice(self):
     self.dice_result =  random.randint(1,6)
     print(f'you rolled a {self.dice_result}')
         
  def WinCondition(self):
     if self.ball.ball_position_row == self.course.hole_row and self.ball.ball_position_col == self.course.hole_col:
        print("you winnnnnnnnn!!!!!!!!!!!")
        return False
     else:
        return True
      
  def TerrainRefiner(self):
     for row in self.course.terrain:
      print(' '.join(row))
      
  def GameLoop(self):    
    self.course.GenerateGolfCourse() #create the terrain
    self.ball.PlaceBall()#place the ball and the hole
    self.course.PlaceHole()
    self.TerrainRefiner() #refine it from its list format using joins
    while self.WinCondition():
      self.Dice()
      self.club.Stroke(self.dice_result)
      self.TerrainRefiner()




game = GameLogic()
game.GameLoop()
    