import random
from noise import pnoise2
#had to turn all that AI stuff off. too much noise. i only needed it to figure out terrain generation anyways + i dont know what its doing sometimes. so it doesnt matter if my code is not top tier. as long as i know what tf its doing im happy.  

# this is how many rows and colums will be fed into our functions. it serves as both a map and the paper for the map. 
rows, cols = 20, 40 

#pretty self explanatory.
def StartGame():
  print("Welcome to the Golf Game!")
  print("You have to hit the ball in the hole in the least number of strokes using the dice we give you.")
  print("Good luck!")
  print("Press any key to start the game.")
  input()
  print("Game started!")




def GeneratePerlinTerrain(rows, cols, scale=10.0):
    terrain = []
    for y in range(rows):
        row = []
        for x in range(cols):
            value = pnoise2(x / scale, y / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=42)# ask the ai what any of this does i dont know
            if value < -0.05:
                row.append('#')  # Sand
            elif value < 0.05:
                row.append('~')  # water
            else:
                row.append('.')  # fairway
            
        terrain.append(row)
        
    return terrain 
#what we've essentialy done is create a function that takes a certain amount of rows and cols. it creates a list that creates an amount of lists equal to the amount of rows we give it. the cols parameter is more the amount of values in each list. as for scale? idk gimme like 6 minutes. im kinda just figuring out how cool everything is since i turned the ai off. 


game_terrain = GeneratePerlinTerrain(rows, cols)

#lol ive always found my paranoia with coding funny. yes peter the list in game terrain is the same in place ball. all you're doing in placeball() is just changing one of the values to a ball...you could do it all in the same function pretty much. 
def PlaceBall(game_terrain, rows, cols):
    ball_col = random.randint(0, cols - 1)
    ball_row = rows - 1
    game_terrain[ball_row][ball_col] = '⚪'
    return game_terrain, ball_row, ball_col

#need to get the values out of the function somehow.
game_terrain, ball_row, ball_col =  PlaceBall(game_terrain, rows, cols) 

# im only using parameter cols because i dont need to go deep in the list. i just need to place a random hole in one of the first lists. the col is the amount of values in the each list so im just placing one hole there. man i wish i didnt start off using ai for this. id be so excited
def PlaceHole(game_terrain, cols): 
    hole_row = random.randint (0, 2)
    hole_col = random.randint(0,cols - 1 )
    game_terrain[hole_row][hole_col] = '🕳️'
    return game_terrain, hole_col, hole_row

game_terrain, hole_col, hole_row = PlaceHole(game_terrain, cols)
for row in game_terrain:
     print(' '.join(row))



#ok im on my own now, no ai, nothing. thug it out. 
#i want the parameter of my list form of game terrain because i need to manipulate it for movement. we are gonna be using logic from place ball too. so i need rows, col i think
def GameLogic(game_terrain, rows, cols):
  not_in_hole = True
  internal_ball_row = ball_row
  internal_ball_col = ball_col
  space_left_up = internal_ball_row 
  space_left_right = cols - internal_ball_col - 1
  space_left_down = rows - ball_row - 1
  need_to_roll_dice = True

  while not_in_hole:
    if need_to_roll_dice:
      roll_dice = random.randint(1, 6)  # we roll the dice
      print(f'you rolled a {roll_dice}!!') #self explanmatory
      moves_left = roll_dice #we start off moves left with the number we rolled.
    else:
      moves_left = moves_left #bruh all i had to do was tell it "hey man if theres no need to roll the dice just use moves left instead rather than roll dice data. stupid."
    movement_query = input("how do you want to move the ball? (up, down, left, right)")#basic question
    if movement_query == "up":
      movement_up = int(input("How many spaces do you want to move the ball up?"))#we save the amount to movement up
      if movement_up > moves_left: #if the movement up is greater than the moves left we tell them they cant move that far and we move on to the next iteration of the loop
        print(f'you only have {roll_dice} moves so you cannot move that far')
      elif movement_up > space_left_up:# if the movement up is greater than the space left up we tell them they cant move that far and we move on to the next iteration of the loop
        print(f'you went out of bounds. remember you only have {space_left_up} moves above')
        game_terrain[internal_ball_row][internal_ball_col] = '⚪'#only doing this because sometimes we wont be where we started and i want to make sure the ball is where it need to be. probably not needed but eh
      elif game_terrain[internal_ball_row][internal_ball_col] == game_terrain[hole_row][hole_col]: #win condition. it needs more but not right now
        print("ayyy you got it in. good job")
        not_in_hole = False
        break
      else:
        if internal_ball_col + 1 >= cols: #if the next column relative to the balls location is more than the amount of columns we still have to replace where the ball was with something so i chose what is to the left of the ball.
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col - 1]
        elif internal_ball_col - 1 <= 0:  #if the next column relative to the balls location is more than the amount of columns we still have to replace where the ball was with something so i chose what is to the right of the ball.
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1]
        else:
          
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1] #we replace the current ball location with a whatever is to its right.
          internal_ball_row = internal_ball_row - movement_up #we change the internal ball row to the current location minus the movement up.
          space_left_up = internal_ball_row #we change the space left up to the current location minus the movement up.
          game_terrain[internal_ball_row][internal_ball_col] = '⚪' #we change the new current location to a ball.
          print(f'you moved up {movement_up} spaces') #we tell them how many spaces they moved.
          moves_left = moves_left - movement_up #we subtract the movement up from moves left.
          print(f'you have {moves_left} moves left') # the math checks out so idont know why the code is being dumb
          if moves_left == 0: #if there are no moves left then we need to roll the dice again.
            need_to_roll_dice = True
          else:#otherwise dont roll the dice again.
            need_to_roll_dice = False
          for row in game_terrain:
            print(' '.join(row))
    elif movement_query == "right":
      movement_right = int(input("How many spaces do you want to move the ball right?"))#we save the amount to movement up
      if movement_right > moves_left: #if the movement up is greater than the moves left we tell them they cant move that far and we move on to the next iteration of the loop
        print(f'you only have {roll_dice} moves so you cannot move that far')
      elif movement_right > space_left_right:# if the movement up is greater than the space left up we tell them they cant move that far and we move on to the next iteration of the loop
        print(f'you went out of bounds. remember you only have {space_left_right} spaces to the right')
        game_terrain[internal_ball_row][internal_ball_col] = '⚪'#only doing this because sometimes we wont be where we started and i want to make sure the ball is where it need to be. probably not needed but eh
      elif game_terrain[internal_ball_row][internal_ball_col] == game_terrain[hole_row][hole_col]: #win condition. it needs more but not right now
        print("ayyy you got it in. good job")
        not_in_hole = False
        break
      else:
        
        if internal_ball_col + 1 >= cols: #if the next column relative to the balls location is more than the amount of columns we still have to replace where the ball was with something so i chose what is to the left of the ball.
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col - 1]
        elif internal_ball_col - 1 <= 0:  #if the next column relative to the balls location is more than the amount of columns we still have to replace where the ball was with something so i chose what is to the right of the ball.
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1]
        else:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1] #we replace the current ball location with a whatever is to its right.
          print(f'the internal ball col is {internal_ball_col}')
          print(f'you have {space_left_right} to move right before math')
          internal_ball_col = internal_ball_col + movement_right #we change the internal ball row to the current location minus the movement right.
          space_left_right = cols - internal_ball_col - 1 #we change the space left up to the current location minus the movement right
          print(f'you have {space_left_right} to move right')
          game_terrain[internal_ball_row][internal_ball_col] = '⚪' #we change the new current location to a ball.
          print(f'you moved right {movement_right} space/s') #we tell them how many spaces they moved.
          moves_left = moves_left - movement_right #we subtract the movement up from moves left.
          print(f'you have {moves_left} moves left') # the math checks out so idont know why the code is being dumb
          if moves_left == 0: #if there are no moves left then we need to roll the dice again.
            need_to_roll_dice = True
          else:#otherwise dont roll the dice again.
            need_to_roll_dice = False
          for row in game_terrain:
            print(' '.join(row))
    elif movement_query == "down":
      movement_down = int(input("How many spaces do you want to move the ball down?"))
      if movement_down > moves_left: #if the movement up is greater than the moves left we tell them they cant move that far and we move on to the next iteration of the loop
        print(f'you only have {roll_dice} moves so you cannot move that far')
      elif movement_down > space_left_down:# if the movement up is greater than the space left up we tell them they cant move that far and we move on to the next iteration of the loop
        print(f'you went out of bounds. remember you only have {space_left_down} spaces below')
        game_terrain[internal_ball_row][internal_ball_col] = '⚪'#only doing this because sometimes we wont be where we started and i want to make sure the ball is where it need to be. probably not needed but eh
      elif game_terrain[internal_ball_row][internal_ball_col] == game_terrain[hole_row][hole_col]: #win condition. it needs more but not right now
        print("ayyy you got it in. good job")
        not_in_hole = False
        break
      else:
        if internal_ball_col + 1 >= cols:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col - 1]
        elif internal_ball_col - 1 <= 0:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1]
        else:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1]
          internal_ball_row = internal_ball_row + movement_down
          space_left_down = internal_ball_row - 1
          game_terrain[internal_ball_row][internal_ball_col] = '⚪'
          print(f'you moved down {movement_down} spaces')
          moves_left = moves_left - movement_down
          print(f'you have {moves_left} moves left')
          if moves_left == 0:
            need_to_roll_dice = True
          else:
            need_to_roll_dice = False
          for row in game_terrain:
            print(' '.join(row))
    elif movement_query == "left":
      movement_left = int(input("How many spaces do you want to move the ball left?"))
      if movement_left > moves_left:
        print(f'you only have {roll_dice} moves so you cannot move that far')
      elif movement_left > space_left_right:
        print(f'you went out of bounds. remember you only have {space_left_right} spaces to the left')
        game_terrain[internal_ball_row][internal_ball_col] = '⚪'#only doing this because sometimes we wont be where we started and i want to make sure the ball is where it need to be. probably not needed but eh
      elif game_terrain[internal_ball_row][internal_ball_col] == game_terrain[hole_row][hole_col]: #win condition. it needs more but not right now
        print("ayyy you got it in. good job")
        not_in_hole = False
        break
      else:
        if internal_ball_col + 1 >= cols:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col - 1]
        elif internal_ball_col - 1 <= 0:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1]
        else:
          game_terrain[internal_ball_row][internal_ball_col] = game_terrain[ball_row][ball_col + 1]
          internal_ball_col = internal_ball_col - movement_left
          space_left_right = internal_ball_col
          game_terrain[internal_ball_row][internal_ball_col] = '⚪'
          print(f'you moved left {movement_left} spaces')
          moves_left = moves_left - movement_left
          print(f'you have {moves_left} moves left')
          if moves_left == 0:
            need_to_roll_dice = True
          else:
            need_to_roll_dice = False
          for row in game_terrain:
            print(' '.join(row))
    else:
      print("invalid input. please try again.")
      continue
  return game_terrain



              

            


GameLogic(game_terrain, rows, cols)










