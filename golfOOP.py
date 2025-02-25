import random
from noise import pnoise2
class golf:


  print("Welcome to the Golf Game!")
  print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
  print("Good luck!")
  print("Press any key to start the game.")
  input()
  print("Game started!")


  def __init__(self):
    self.row = 20 #the amount of rows
    self.col = 40 #the amount of colums. id rather do it this way because its cleaner
    self.terrain = []
    self.terrain_original = []


  def GeneratePerlinTerrain(self, scale=10.0):
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
        
  def TerrainRefiner(self):
     for row in self.terrain:
      print(' '.join(row))
     
     
  def PlaceBall(self):
      self.ball_col = random.randint(0, 9)
      self.ball_row = self.row - 1
      self.terrain[self.ball_row][self.ball_col] = '⚪'
      return self.ball_col, self.ball_row

  
  def PlaceHole(self): 
    self.hole_row = random.randint (0, 2)
    self.hole_col = random.randint(self.col-3,self.col-1)
    self.terrain [self.hole_row][self.hole_col] = '🕳️'
  


  def Ball(self):
     self.ball_position_row = self.ball_row
     self.ball_position_col = self.ball_col

  def WinCondition(self):
     if self.ball_position_row == self.hole_row and self.ball_position_col == self.hole_col:
        print("you winnnnnnnnn!!!!!!!!!!!")
        return False
     else:
        return True
     



  def Dice(self):
     self.dice_result =  random.randint(1,6)
     
  def MoveUp(self):
    
    self.terrain[self.ball_position_row][self.ball_position_col] = self.terrain_original[self.ball_position_row][self.ball_position_col]
    #we replace the current ball location with whatever is in the original list
    self.ball_position_row = self.ball_position_row - self.dice_result
    #we change the internal ball row to the current location minus the dice roll result.
    space_left_up = self.ball_position_row
    #we change the space left up to the current location minus the movement up.
    self.terrain[self.ball_position_row] [self.ball_position_col] = '⚪'   
    #we change the new current location to a ball.
    print(f'you moved up {self.dice_result} spaces') 
    #we tell them how many spaces they moved.
  
  
  
  def MoveDown(self):
    self.terrain[self.ball_position_row][self.ball_position_col] = self.terrain_original[self.ball_position_row][self.ball_position_col]
    #we replace the current ball location with whatever is in the original list
    self.ball_position_row = self.ball_position_row + self.dice_result
    #we change the internal ball row to the current location plus the dice result.
    space_left_down = self.ball_position_row
    #we change the space left down to the current location minus the movement down.
    self.terrain[self.ball_position_row] [self.ball_position_col] = '⚪' 
    #we change the new current location to a ball.
    print(f'you moved down {self.dice_result} spaces') 
    #we tell them how many spaces they moved.

  
  def MoveLeft(self):
    self.terrain[self.ball_position_row][self.ball_position_col] = self.terrain_original[self.ball_position_row][self.ball_position_col]
    #we replace the current ball location with whatever is in the original list
    self.ball_position_col = self.ball_position_col - self.dice_result
    #we change the internal ball column to the current location minus the  dice result.
    space_left_down = self.ball_position_row
    #we change the space left down to the current location minus the movement down.
    self.terrain[self.ball_position_row] [self.ball_position_col] = '⚪' 
    #we change the new current location to a ball.
    print(f'you moved left {self.dice_result} spaces') 
    #we tell them how many spaces they moved.


  def MoveRight(self):
    self.terrain[self.ball_position_row][self.ball_position_col] = self.terrain_original[self.ball_position_row][self.ball_position_col]
    #we replace the current ball location with whatever is in the original list
    self.ball_position_col = self.ball_position_col + self.dice_result
    #we change the internal ball column to the current location plus the dice result.
    space_left_down = self.ball_position_row
    #we change the space left down to the current location minus the movement down.
    self.terrain[self.ball_position_row] [self.ball_position_col] = '⚪' 
    #we change the new current location to a ball.
    print(f'you moved right {self.dice_result} spaces') 
    #we tell them how many spaces they moved.
   



  def Movement(self):
     movement_query = input("how do you want to move the ball? (up, down, left, right)")
     return movement_query
  def GameLogic(self):
     self.GeneratePerlinTerrain() #create the terrain
     self.PlaceBall()#place the ball and the hole
     self.PlaceHole()
     self.TerrainRefiner()#refine it from its list format using joins
     self.Ball() #why the hell doesnt the game work without this. i thought with initializing golf() it initialized all its methods. 
     while self.WinCondition():
        self.Dice()#roll the dice already
        print(f'you rolled a {self.dice_result}')#tell me what i rolled
        direction = self.Movement()
        if direction == "up":
           self.MoveUp()
           self.TerrainRefiner()
           self.WinCondition()
        elif direction == "down":
           self.MoveDown()
           self.TerrainRefiner()
        elif direction == "left":
           self.MoveLeft()
           self.TerrainRefiner()
        elif direction == "right":
           self.MoveRight()
           self.TerrainRefiner()
           
#checklist
#need to add error handling for when player goes out of bounds. 
#need to add terrain penalties
#need to add the amount of strokes
#need to figure out if the way i setup the ball and the hole is fair




        



  # def GameStarter(self):
  #    self.GeneratePerlinTerrain()

  #    self.TerrainRefiner()
     
     
startgame = golf()
startgame.GameLogic()

     


#dude OOP is like the coolest way to write code. its so cleannnnnnnnnnnnnn.

