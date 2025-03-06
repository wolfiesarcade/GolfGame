import random
from noise import pnoise2
class GolfCourse:
  def __init__(self, row: int, col: int, ballrow: int, ballcol: int):
    self.row = row #the amount of rows.
    self.col = col #the amount of colums.
    self.ball_col = ballcol
    self.ball_row = ballrow
    self.terrain: list = []
    self.terrain_original: list = []
    
  def GenerateGolfCourse(self, scale=10.0) -> list:
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
        
  def GetOriginalTerrain(self, row, col) -> list:
     return self.terrain_original[self.ball_row][self.ball_col]
  
  def GetTerrain(self) -> list:
     return self.terrain
     
  def PlaceHole(self) -> tuple: 
    hole_row = random.randint(0, 2)
    hole_col = random.randint(self.col - 3, self.col - 1)
    self.terrain[hole_row][hole_col] = '🕳️'
    return hole_row, hole_col

  def GetCourseRowAndCol(self) -> int:
     return self.col, self.row
  
  def SetBallPos(self): #we set the ball position on a large golfcourse as our starting point
    self.terrain[self.ball_row][self.ball_col] = '⚪'
    
        
class GolfBall:
  def __init__(self, row):
     self.row = row
  
  def PlaceBall(self) -> int :
    ball_row: int = self.row - 1
    ball_col = random.randint(0, 9)
    return ball_col, ball_row

# class GolfClub: this seems super obselete because golfclubs dont have dice...but like in the video you sent me the club was a pencil that was a dice. so maybe.... i put the dice in this class? but it seems more like game logic hence my decicion. 
#   def __init__(self, dice):
#      self.dice_result = dice
#   # def Stroke(self) -> str:
#   #   #we replace the current ball location with whatever is in the original list

#   #   #we tell them how many spaces they moved.
#   #   return direction

  
class GameLogic:
  def __init__(self, GolfBall, GolfCourse):
      print("Welcome to the Golf Game!")
      print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
      print("Good luck!")
      print("Game started!")
      game_row: int = 20
      game_col: int = 40
      self.ball = GolfBall(game_row) #get golfball value
      self.ball_col, self.ball_row = self.ball.PlaceBall()#insert golfball values into variables we can access
      self.course = GolfCourse(game_row, game_col, self.ball_row, self.ball_col)#insert variables 
      self.courseterrain = self.course.GetTerrain()

      

  def Dice(self) -> int:
     self.dice_result =  random.randint(1,6)
     print(f'you rolled a {self.dice_result}')

  def Movement(self) -> str:
    direction = input("how do you want to move the ball? (up, down, left, right)")
    self.courseterrain[self.ball_row][self.ball_col] = self.courseterrain_original[self.ball_row][self.ball_col] #replace ball with original terrain
    print(f'you moved {direction} {self.dice_result} spaces') 
    if direction == "up": 
      self.ball_row = self.ball_row - self.dice_result
      #we change the ball row in this class to the current location minus the dice roll result.
    elif direction == "down":
      self.ball_row = self.ball_row + self.dice_result
      #we change the internal ball row to the current location plus the dice result.
    elif direction == "left":
      self.ball_col = self.ball_col - self.dice_result
    elif direction == "right": 
      self.ball_col = self.ball_col + self.dice_result
      #we change the internal ball column to the current location plus the dice result.
    else:
      print('invalid direction')    
    self.courseterrain[self.ball_row][self.ball_col] = '⚪'  
    return direction
    
      
    #space_left_up = self.ball_position_row
    #we change the space left up to the current location minus the movement up.
  
    


  def GetHoleRowAndCol(self) -> int:
     self.hole_row, self.hole_col = self.course.PlaceHole()
     return self.hole_row, self.hole_col #its weird and dirty i know but it kept being called in wincondition so i had to put it here.

  def WinCondition(self) -> bool:
     if self.ball_row == self.hole_row and self.ball_col == self.hole_col:
        print("you winnnnnnnnn!!!!!!!!!!!")
        return False
     else:
        return True
      
  def TerrainRefiner(self) -> list:
     for row in self.courseterrain:
      print(' '.join(row))
      
  def GameLoop(self) -> list:    
    self.course.GenerateGolfCourse() #create the terrain
    self.hole_row, self.hole_col = self.course.PlaceHole()
    self.course.SetBallPos()
    #place the ball and the hole
    self.TerrainRefiner() #refine it from its list format using joins
    while self.WinCondition():
      self.Dice()
      self.Movement()
      # self.BallMoverandReplace()
      self.TerrainRefiner()



game = GameLogic(GolfBall, GolfCourse)
game.GameLoop()
    
