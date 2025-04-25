import socket
import socketserver
import struct
import json


class Multiplayer:
  def __init__(self):
    self.terrain = " "

  
  def NetworkPreReq(self):
    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversocket.bind(('localhost', 6969))
    self.serversocket.listen(2)
    self.connection = self.serversocket.accept()[0]
  # def ReceiveMovementDirection(self):
  #   self.NetworkPreReq()
  #   while True:
  #     connection, address = self.serversocket.accept()
  #     buf = connection.recv(99999)
  def ReceiveTerrain(self) -> list:
    buf = self.connection.recv(9999)
    self.terrain = json.loads(buf.decode("utf-8"))

  def ReceiveDice(self) -> list:
    buf = int.from_bytes(self.connection.recv(1))
    self.dice = buf
    print(f'you rolled a {self.dice}')
    
  def sending(self):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 6970))
    direction = input("what direction do you want to move?")
    clientsocket.send(direction.encode("utf-8"))
    
  def TerrainRefiner(self) -> list:
    
    json_list = self.terrain
    # regular_list = json.loads(json_list)

    for row in json_list:
       print(' '.join(row))

  def GameLoop(self) -> list:
    self.NetworkPreReq()
    while True:
      self.ReceiveTerrain()
      self.TerrainRefiner()
      self.ReceiveDice()
      self.sending()
      

    
    



    
    
    
test = Multiplayer()
test.GameLoop()