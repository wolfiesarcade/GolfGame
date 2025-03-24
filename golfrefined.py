import random
from noise import pnoise2
class GolfCourse:
  def __init__(self, row: int, col: int): #course doesn't need to know where the ball is, just set it based on inputs
    self.row = row #the amount of rows.
    self.col = col #the amount of colums.
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
        
  def GetOriginalTerrain(self, row, col) -> str:
     return self.terrain_original[row][col] 
  
  
  def ReplaceTerrain(self, row, col):
     self.terrain[row][col] = self.GetOriginalTerrain(row, col)
     
  def PlaceHole(self) -> tuple: 
    hole_row = random.randint(0, 2)
    hole_col = random.randint(self.col - 3, self.col - 1)
    self.terrain[hole_row][hole_col] = '🕳️'
    return hole_row, hole_col
  
  def SetBallPos(self, row, col): #we set the ball position on a large golfcourse as our starting point
    self.terrain[row][col] = '⚪' #use input variables instead of class variables
        
class GolfBall:
  #GolfBall now contains its own data, reducing the need for other objects to store this data
  def __init__(self, row):
     self.row = row - 1
     self.col = random.randint(0, 9)
  
class GameLogic:
  def __init__(self, GolfBall, GolfCourse):
      print("Welcome to the Golf Game!")
      print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
      print("Good luck!")
      print("Game started!")
      game_row: int = 20
      game_col: int = 40
      self.parcount = 0
      self.course = GolfCourse(game_row, game_col)#changed the order of things. first, make the course, 
      self.course.GenerateGolfCourse() #generate terrain, 
      self.ball = GolfBall(game_row) #make ball, 
      self.course.SetBallPos(self.ball.row, self.ball.col)#place ball, 
      self.hole_row, self.hole_col = self.course.PlaceHole()#place hole, 
      self.TerrainRefiner() #print refined terrain using joins. should prevent data from being overwritten this way.

  def Dice(self) -> int:
     self.dice_result =  random.randint(1,6)
     print(f'you rolled a {self.dice_result}')
     
  def ParCount(self) -> int:
    print (f'Your current par count is {self.parcount}')
    self.parcount+=1
  
  def MovementCost(self):
    if self.course.GetOriginalTerrain(self.ball.row,self.ball.col) == '#':
      sand_math = self.dice_result // 2
      print(sand_math)
      self.dice_result = int(sand_math)
      print('your movement is divided by 2 because you are in sand')
    elif self.course.GetOriginalTerrain(self.ball.row,self.ball.col) == '~':
      water_math = self.dice_result // 3
      print(water_math)
      self.dice_result = int(water_math)
      print('your movement is divided by 3 because you are in water')
    else:
      self.dice_result //= 1
      # print(math)
      # self.dice_result = math(int)
      

  def Movement(self) -> str:
    direction = input("how do you want to move the ball? (up, down, left, right)")
    self.course.ReplaceTerrain(self.ball.row, self.ball.col) #setter method is easier to read
    print(f'you moved {direction} {self.dice_result} spaces') 
    if direction == "up": 
      self.ball.row -= self.dice_result #operators instead of statements is a bit cleaner
    elif direction == "down":
      self.ball.row += self.dice_result
    elif direction == "left":
      self.ball.col -= self.dice_result
    elif direction == "right": 
      self.ball.col += self.dice_result
    else:
      print('invalid direction')
    if self.BoundsCheck(): #checking to see whether the ball values used in the array would cause an index out of bounds error, if so fixed it
      print('whoops, ball went out of bounds, setting it back within bounds...')
    self.course.SetBallPos(self.ball.row, self.ball.col)
    return direction
  
  def BoundsCheck(self) -> bool:
    if self.ball.row < 0:
      self.ball.row = 0
      return True
    elif self.ball.row >= self.course.row:
      self.ball.row = self.course.row-1
      return True
    if self.ball.col < 0:
      self.ball.col = 0
      return True
    elif self.ball.col >= self.course.col:
      self.ball.col = self.course.col-1
      return True
    return False
        

  def WinCondition(self) -> bool:
    if self.ball.row == self.hole_row and self.ball.col == self.hole_col:
      print("you winnnnnnnnn!!!!!!!!!!!")
      return False
    else:
      return True
      
  def TerrainRefiner(self) -> list:
     for row in self.course.terrain:
      print(' '.join(row))
      
  def GameLoop(self) -> list:
    #since all that stuff was done before the loop, placed it in init instead, makes more sense
    while self.WinCondition():
      self.Dice() #random movement modifier
      self.ParCount()# par counter
      self.MovementCost()# duh
      self.Movement() #movement decided based on direction input
      self.TerrainRefiner() #print the resulting change to the terrain and ball location

game = GameLogic(GolfBall, GolfCourse)
game.GameLoop()
    
#figure out par average