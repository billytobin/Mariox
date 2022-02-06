
from .mobile import Mobile

import pygame
from pygame.event import Event


class Player(Mobile):
   def __init__(self, imageName, position):
      super().__init__(imageName, position)

      self._jumpTime = 0.5
      self._vSpeed = 50
      self._jSpeed = 100

      self._nFrames = 2
      self._framesPerSecond = 2

      self._nFramesList = {
         "walking": 4,
         "falling": 4,
         "jumping": 1,
         "standing": 2
      }

      self._rowList = {
         "walking": 1,
         "jumping": 2,
         "falling": 4,
         "standing": 0
      }

      self._framesPerSecondList = {
         "walking": 8,
         "standing": 2,
         "jumping": 1,
         "falling": 8
      }

      self._state = PlayerState()
      self.transitionState("falling")

   def updateVelocity(self, seconds):
       super().updateVelocity(seconds)

       if self._state.getState() == "standing":
            self._velocity.y = 0
       elif self._state.getState() == "jumping":
            self._velocity.y = -self._jSpeed
            self._jumpTimer -= seconds
            if self._jumpTimer < 0:
                self._state.manageState("fall", self)
       elif self._state.getState() == "falling":
            self._velocity.y += self._jSpeed * seconds

   
   def handleEvent(self, event: Event):
      if event.type == pygame.KEYDOWN:
            
         if event.key == pygame.K_UP:
            self._state.manageState("jump", self)
            
         elif event.key == pygame.K_LEFT:
            self._state.manageState("left", self)
            
         elif event.key == pygame.K_RIGHT:
            self._state.manageState("right", self)
      
      elif event.type == pygame.KEYUP:
            
         if event.key == pygame.K_UP:
            self._state.manageState("fall", self)
            
         elif event.key == pygame.K_LEFT:
            self._state.manageState("stopleft", self)
            
         elif event.key == pygame.K_RIGHT:
            self._state.manageState("stopright", self)
   
   def collideGround(self, yClip):
      self._state.manageState("ground", self)
      self._position.y -= yClip
    
   
  
class PlayerState(object):
    def __init__(self, state="falling"):
        self._state = state

        self._movement = {
            "left": False,
            "right": False
        }

        self._lastFacing = "right"

    def isMoving(self):
        return True in self._movement.values()

    def isGrounded(self):
        return self._state == "walking" or self._state == "standing"

    def getFacing(self):
        if self._movement["left"] == True:
            self._lastFacing = "left"
        elif self._movement["right"] == True:
            self._lastFacing = "right"

        return self._lastFacing

    def manageState(self, action: str, player: Player):
        if action in self._movement.keys():
            if self._movement[action] == False:
                self._movement[action] = True
                if self._state == "standing":
                    player.transitionState("walking")

        elif action.startswith("stop") and action[4:] in self._movement.keys():
            direction = action[4:]
            if self._movement[direction] == True:
                self._movement[direction] = False
                allStop = True
                for move in self._movement.keys():
                    if self._movement[move] == True:
                        allStop = False
                        break

                if allStop and self._state not in ["falling", "jumping"]:
                    player.transitionState(self._state)

        elif action == "jump" and self._state == "standing":
            self._state = "jumping"
            player.transitionState(self._state)

        elif action == "fall" and self._state != "falling":
            self._state = "falling"
            player.transitionState(self._state)

        elif action == "ground" and self._state == "falling":

            self._state = "standing"

            if self.isMoving():
                player.transitionState("walking")
            else:
                player.transitionState(self._state)

    def getState(self):
        return self._state

      
   