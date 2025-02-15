import pygame
from constants import *
class Sprite:
    def __init__(self,surface,spriteType=None):
          
          self.spriteType=spriteType
          self.frames=[]
          if type(surface) in (list,tuple):
             self.frames=surface
             self.surface=self.frames[0]
             pass
          else:
               self.surface=surface

    
          self.rect=self.surface.get_rect()
          self.width=self.surface.get_width()
          self.height=self.surface.get_height()
          
          
          self.currentFrame=0
          self.isAffectedByGv=False
          self.gravity=1

          self.platform=None
          self.isVisible=True
         
          self.velocity={'x':0,'y':0}
          self.isMoving=False
          self.isSliding=False
          self.speed=1
          self.totalFrames=1
          self.isPickedUp=False
          self.position={'x':0,'y':0}

    
    def animate(self,main_surface):
            current_frame=self.surface.subsurface((2*self.surface.get_width()*0.251,
                                                   0,self.surface.get_width()*0.252,
                                                   self.surface.get_height()))
            main_surface.blit(current_frame,self.rect)  

         
    
    def draw(self,main_surface):
       
           main_surface.blit(self.surface,self.rect)  
      
    def handlGravity(self):
          if self.isAffectedByGv and not self.isPickedUp:
                self.velocity['y']+=self.gravity
                self.position['y']=self.rect.y

                self.position['y']+=self.velocity['y']

                if(self.rect.colliderect(self.platform.rect)):
                      self.velocity['y']=0
                      self.position['y']=self.platform.rect.top-self.height-0.2
                      self.rect.bottom=self.platform.rect.top
                else:
                  self.rect.y=self.position['y']

                      
                      

    def isOutOfProductionLine(self,prod=None):
          
          if prod!=None:
             if self.rect.left>=prod.rect.right:
                 return [True,True]
             
          if self.rect.left>GAME_WIDTH*GAME_SCALE:
                return [True,False]

          if self.rect.right<0:
                 return [True,False]
          if self.rect.bottom<0:
                 return [True,False] 
          if self.rect.top>GAME_HEIGHT*GAME_SCALE:  
                 return [True,False]
          
          return [False,False]


    def drawRect(self,main_surface):
          pygame.draw.rect(main_surface,"red",self.rect,2)
          
    def slide(self):pass
        
    
    def handlMove(self):
        if self.isMoving and not self.isPickedUp:
                self.velocity['x']=self.speed
                self.position['x']+=self.velocity['x']
                self.rect.x=self.position['x']
        
    def handlSlide(self):
        if self.isSliding:
            
                self.velocity['x']=0.5
                self.velocity['y']=1
                self.position['x']+=self.velocity['x']
                self.position['y']+=self.velocity['y']
            
                self.rect.x=self.position['x']
                self.rect.y=self.position['y']
    
    def update(self,main_surface):

        self.handlGravity()
        self.handlMove()
        self.handlSlide()
    
        
        
        self.draw(main_surface)
      #   self.drawRect(main_surface)
        pass