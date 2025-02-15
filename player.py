from sprite import Sprite

from constants import *
class Player(Sprite):
    def __init__(self,surface,game):
        super().__init__(surface)
    
        
        self.game=game
        self.position={'x':self.game.width*0.18,'y':self.game.height*0.05}
     
        self.rect.x=self.position['x']
        self.timer=0
        self.rect.y=self.position['y']
        self.playPickupAnimitaion=False

    
        self.velocity={'x':4,'y':0}

        self.isPickingUp=False
        self.isSlidingLeft=False
        self.isSlidingRight=False
       
        
       
    # def draw(self,main_surface):
    #     # super().draw(main_surface)
        
    #     pass
    def animate(self):
         if self.playPickupAnimitaion:
            if self.timer%10==0:
               self.currentFrame+=1

               if self.currentFrame>3 and self.isPickingUp :
                  self.currentFrame=3
                  self.playPickupAnimitaion=False
               elif self.currentFrame>3 and not self.isPickingUp:
                  self.currentFrame=0
                  self.playPickupAnimitaion=False
         else:
              self.currentFrame=0
                    
            
         self.surface=self.frames[self.currentFrame]
         self.rect=self.surface.get_rect()


        
    def handlPickUp(self):
        self.timer+=1
        for cheese in self.game.cheese_pool:
                cheese.isPickedUp=False
                # pass
                cheese.isMoving=True
                cheese.isAffectedByGv=True


        for cheese in self.game.cheese_pool:
            if self.rect.colliderect(cheese) and self.isPickingUp :
                

                cheese.isMoving=False
                cheese.isAffectedByGv=False
                cheese.position['x']=self.rect.bottomleft[0]
                cheese.position['y']=self.frames[1].get_rect().bottomleft[1]

                cheese.isPickedUp=True
                cheese.rect.x=cheese.position['x']
                cheese.rect.y=cheese.position['y']
               
                break
                
            
                

       
        if  self.isPickingUp and not self.playPickupAnimitaion:

            self.playPickupAnimitaion=True
  
                # self.surface=pygame.transform.scale_by(self.surface,[1,1.01])

    def update(self,main_surface):

       

        self.handlPickUp()
        self.animate()
        
        self.rect.x=self.position['x']
        self.rect.y=self.position['y']
        
        
        if self.isSlidingRight  and self.rect.centerx<self.game.machine_base.rect.bottomright[0]:
            # print()
            # print(self.game.assets[MACHINE_BASE].x)
            self.position['x']+=self.velocity['x']
        
        if self.isSlidingLeft and self.rect.centerx>self.game.width*0.053:
            
            self.position['x']-=self.velocity['x']
   
        super().update(main_surface)
        pass
    