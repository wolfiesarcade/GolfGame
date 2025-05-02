import socket
import json


class Multiplayer:
  def __init__(self):
    self.terrain = " "
    self.player = 0
    self.parcount = 0

  
  def NetworkPreReq(self):
    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversocket.bind(('localhost', 6969))
    self.serversocket.listen(1)  # Only one connection for now
    self.connection, _ = self.serversocket.accept()  # Only accept once

  def ReceiveTerrain(self) -> list:
    buf = self.connection.recv(9999)
    self.terrain = json.loads(buf.decode("utf-8"))
    
  def ReceiveMovementCost(self) -> str:
    if self.player % 2 == 0:
      self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.serversocket.bind(('localhost', 6971))
      self.serversocket.listen(1)
      conn, _ = self.serversocket.accept()
      buf = conn.recv(1024)
      direction = buf.decode("utf-8")
      print(direction)
      conn.close()
      self.serversocket.close()
    else:
      pass
    
  def ReciveSpacesMoved(self) -> str:
    if self.player % 2 == 0:
      self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.serversocket.bind(('localhost', 6972))
      self.serversocket.listen(1)
      conn, _ = self.serversocket.accept()
      buf = conn.recv(1024)
      spaces_moved = buf.decode("utf-8")
      print(spaces_moved)
      conn.close()
      self.serversocket.close()
    else:
      pass
    
  def ReceiveDice(self) -> list:
    dice = int.from_bytes(self.connection.recv(1))
    if self.player % 2 == 0:
      self.dice = dice
      print(f'you rolled a {self.dice}')
    else:
      pass
    
  def DistributeDirection(self):

    if self.player % 2 == 0:
      clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      clientsocket.connect(('localhost', 6970))
      direction = input("what direction do you want to move?")
      clientsocket.send(direction.encode("utf-8"))
    else:
      print("waiting for player 1")
    
  def TerrainRefiner(self) -> list:
    json_list = self.terrain
    # regular_list = json.loads(json_list)
    for row in json_list:
       print(' '.join(row))
       
  def ParCount(self) -> int:
    print (f'Your current par count is {self.parcount}')
    self.parcount+=1

  def GameLoop(self) -> list:
    self.NetworkPreReq()
    while True:
      # self.ReceiveMovementCost()
      self.player+=1
      self.ReceiveTerrain()
      self.TerrainRefiner()
      self.ReceiveDice()
      self.ReceiveMovementCost()
      self.DistributeDirection()
      self.ReciveSpacesMoved()
      self.ParCount()
      

    
    



    
    
    
test = Multiplayer()
test.GameLoop()