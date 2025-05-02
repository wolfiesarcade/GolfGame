import random
import socket
import json

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
     
class Multiplayer():
  def __init__(self):
    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversocket.bind(('localhost', 6969))  # Only connect once here
    self.serversocket.listen(1)
    self.connection, _ = self.serversocket.accept()

  def DistributeTerrain(self, terrain):
    data = json.dumps(terrain)
    encoded = data.encode("utf-8")
    self.connection.send(encoded)
    
  def DistributeDice(self, diceresult):
    diceroll = diceresult.to_bytes(1, byteorder='big')
    self.connection.sendall(diceroll)

  def DistributeMovementcost(self, movementcost, playernumber):
    if playernumber % 2 == 0:
      serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serversocket.bind(('localhost', 6971))
      serversocket.listen(1)
      conn, _ = serversocket.accept()
      conn.send(movementcost.encode("utf-8"))
  
  def DistributeSpacesMoved(self, spacesmoved, playernumber):
    if playernumber % 2 == 0:
      serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serversocket.bind(('localhost', 6972))
      serversocket.listen(1)
      conn, _ = serversocket.accept()
      conn.send(spacesmoved.encode("utf-8")) 
                
  def Receive_direction(self, playernumber) -> str:
    if playernumber % 2 == 0:
      self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.serversocket.bind(('localhost', 6970))
      self.serversocket.listen(1)
      conn, _ = self.serversocket.accept()
      buf = conn.recv(1024)
      direction = buf.decode("utf-8")
      print(direction)
      conn.close()
      self.serversocket.close()
      return direction
    
class GameLogic:
  def __init__(self, GolfBall, GolfCourse):
      print("Welcome to the Golf Game!")
      print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
      print("Good luck!")
      print("Game started!")
      game_row: int = 20
      game_col: int = 40
      self.parcount = 0
      self.player = 0
      self.course = GolfCourse(game_row, game_col)#changed the order of things. first, make the course, 
      self.course.GenerateGolfCourse() #generate terrain, 
      self.ball = GolfBall(game_row) #make ball, 
      self.course.SetBallPos(self.ball.row, self.ball.col)#place ball, 
      self.hole_row, self.hole_col = self.course.PlaceHole()#place hole, 
      self.multiplayer = Multiplayer()
      self.TerrainRefiner() #print refined terrain using joins. should prevent data from being overwritten this way.

  def Dice(self) -> int:
     self.dice_result =  random.randint(1,6)
     print(f'you rolled a {self.dice_result}')
     
  def ParCount(self) -> int:
    self.parcount+=1
    print (f'Your current par count is {self.parcount}')
    
  
  def MovementCost(self):
    self.movementcostmessage = ' '
    if self.course.GetOriginalTerrain(self.ball.row,self.ball.col) == '#':
      sand_math = self.dice_result // 2
      self.dice_result = int(sand_math)
      self.movementcostmessage='your movement is divided by 2 because you are in sand'
      print(self.movementcostmessage)
    elif self.course.GetOriginalTerrain(self.ball.row,self.ball.col) == '~':
      water_math = self.dice_result // 3
      self.dice_result = int(water_math)
      self.movementcostmessage='your movement is divided by 3 because you are in water'
      print(self.movementcostmessage)
    else:
      self.dice_result //= 1
      # print(math)
      # self.dice_result = math(int)


  def Movement(self, p2direction) -> str:
    if self.player % 2 == 0:
      print("how do you want to move the ball? (up, down, left, right)")
      print(p2direction)
      direction = p2direction
    else:
      direction = input("how do you want to move the ball? (up, down, left, right)")
    self.course.ReplaceTerrain(self.ball.row, self.ball.col) #setter method is easier to read
    self.spacesmoved = f'you moved {direction} {self.dice_result} spaces'
    print(self.spacesmoved)
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
      self.player+=1
      self.multiplayer.DistributeTerrain(self.course.terrain)
      self.Dice() #random movement modifier
      self.multiplayer.DistributeDice(self.dice_result)
      self.ParCount()# par counter
      self.MovementCost()# duh
      self.multiplayer.DistributeMovementcost(self.movementcostmessage, self.player)
      self.Movement(self.multiplayer.Receive_direction(self.player)) #movement decided based on direction input
      self.multiplayer.DistributeSpacesMoved(self.spacesmoved, self.player)
      self.TerrainRefiner() #print the resulting change to the terrain and ball location
      # self.multiplayer.Distribute(self.course.terrain) #opushes each row to the client

game = GameLogic(GolfBall, GolfCourse)
game.GameLoop()
    
#figure out par average