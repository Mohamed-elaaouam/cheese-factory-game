
import pygame
import sys
import threading
from player import Player
from sprite import Sprite
import time
import copy
from constants import *
      
 
def load_asset():
    """Only loads the image in the thread, does not modify it."""
 
    
    try:
        # Game.loaded_image =   # ✅ Safe (loading)
        Game.assets[OVEN]=pygame.image.load(IMG_PATH+"oven.png")
        Game.assets[GARBAGE]=pygame.image.load(IMG_PATH+"Garbage.png")
        Game.assets[TRAIL]=pygame.image.load(IMG_PATH+"trail.png")
        Game.assets[HAND_CLOSED]=pygame.image.load(IMG_PATH+"hand_closed.png")
        Game.assets[HAND_OPEN]=pygame.image.load(IMG_PATH+"hand_open.png")
        Game.assets[MACHINE_BASE]=pygame.image.load(IMG_PATH+"machine_base.png")
        Game.assets[PROD_LINE]=pygame.image.load(IMG_PATH+"prod_line.png")
        Game.assets[BAD_CHEESE]=pygame.image.load(IMG_PATH+"bad_cheese.png")
        Game.assets[CHEESE]=pygame.image.load(IMG_PATH+"cheese.png")
        Game.assets[BG1]=pygame.image.load(IMG_PATH+"bg.png")

        Game.assets[PACKAGING]=pygame.image.load(IMG_PATH+"packaging.png")

        Game.assets[PACKAGED_CHEESE]=pygame.image.load(IMG_PATH+"pk_cheese.png")

        Game.assets[HAND]=pygame.image.load(IMG_PATH+"hand.png")

        Game.assets[BAD_PK_CHEESE]=pygame.image.load(IMG_PATH+"bad_pk_cheese.png")
        
        Game.assets[HAND]=[pygame.image.load(IMG_PATH+"hand10001.png"),
                           pygame.image.load(IMG_PATH+"hand10002.png"),
                           pygame.image.load(IMG_PATH+"hand10003.png"),
                           pygame.image.load(IMG_PATH+"hand10004.png")
                           ]

        

        

        
        if(len(Game.assets)):
            
            pygame.event.post(pygame.event.Event(ASSETS_LOADED_EVENT)) 

        else:print('retrying')
            
        
    except  Exception as e :print(e)
    


threading.Thread(target=load_asset).start()      
      
class Game:
    loaded_image=None
    currentScreen=LOADING_SCREEN
    assets={}
    
    def __init__(self):
        pygame.init()
        self.armRect=None
        self.title=GAME_TITLE
        self.width=GAME_WIDTH*GAME_SCALE
        self.height=GAME_HEIGHT*GAME_SCALE
        self.transparent=TRANSPARENT
        self.player=None
        self.isGameOver=False
        self.button=pygame.image.load('assets/UI/button.png')   
        self.dialog=pygame.image.load('assets/UI/dialog.png')    
        self.font=pygame.font.Font(FONT_ANTA, 32) 
        self.fontLarge=pygame.font.Font(FONT_ANTA, 64) 
        self.isSliding=False
        self.isFlashingPoint=False
        self.running=True
        self.levelTimer=LEVEL_TIME
        self.score=0
        self.garbage=None
        self.replayButton=None
        self.menuButton=None

        self.levelProgress=0
        self.productionBarWidth=self.width*0.2

        self.packagedCheesePool=[]
        self.reservedPackagedCheesePool=[]

        self.packaging=None
        self.hand=None
        self.timer=0
        self.cheese_reserve=[]
        self.quitButton=None

        self.machine_base=None
        self.oven=None

        self.cheese_pool=[]
        # self.currentScreen=LOADING_SCREEN
        self.productionLine=None
        self.btRect=None
        # self.loaded_image=None
        
        sys.setrecursionlimit(10000000)
        self.surface = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_TITLE)
       
        # pygame.mouse.set_system_cursor(11)
      
    def update(self):
                    self.timer+=1
                    if self.timer%60==0 and self.running:
                      
                         self.levelTimer-=1
                         if self.levelTimer<=0:
                              self.levelTimer=0
                    
                    match Game.currentScreen:
                        case "MENU_SCREEN":
                                self.drawMenuScreen()
                                
                        case "GAME_SCREEN":
                                
                                
                                if self.running:
                                 self.drawGameScreen()

                                 self.drawHud()
                                pass
                        case "LOADING_SCREEN":
                            buttonText=self.font.render("Loading", False, 'white')
                            # pygame.draw.rect(self.surface,'green', self.btRect,2,3)
                            buttonTextRect=buttonText.get_rect()
                            buttonTextRect.centerx= self.width*0.5
                            buttonTextRect.centery= self.height*0.3
                            self.surface.blit(buttonText,buttonTextRect)
                            
                 
                 
                    if self.running:
                       pygame.display.update() 
                    self.clock.tick(60)
    def draw(self):
                self.surface.fill(self.transparent)
    
    def scaleAssets(self):
        for asset in Game.assets:

            if type(Game.assets[asset]) in (list,tuple):
                scaledFrames=[]
                for frame in Game.assets[asset]:
                       
                        
                        scaled_frame=pygame.transform.scale_by(frame,GAME_SCALE)
                        scaledFrames.append(scaled_frame)
                        
                Game.assets[asset]=scaledFrames
              
                
            else:
                scaled_asset=pygame.transform.scale_by(Game.assets[asset],GAME_SCALE)
                Game.assets[asset]=scaled_asset
        # print(Game.assets)
            # print(Game.assets[asset])
        self.initGame()
    # def createCheese(self):
    def restoreCheese(self):
         self.player.position={'x':self.width*0.18,'y':self.height*0.05}
         for cheese in self.cheese_pool:
              self.cheese_reserve.append(cheese)
         self.cheese_pool=[]

         for cheese in self.cheese_reserve:
              cheese.rect.x=self.oven.rect.x
              cheese.rect.y= self.oven.rect.y+10

              cheese.position['x']= self.oven.rect.x
              cheese.position['y']= self.oven.rect.y+10
         for pk in self.packagedCheesePool:
               self.reservedPackagedCheesePool.append(pk)
         self.packagedCheesePool=[]

         for cheese in self.reservedPackagedCheesePool:
                     
                cheese.position['x']=self.packaging.rect.x
                cheese.position['y']=self.packaging.rect.y
                cheese.rect.x=self.packaging.rect.x
                cheese.rect.y= self.packaging.rect.y
              
        
            #   print(self.cheese_reserve.index(cheese))
              
                
    def initGame(self):
        # machine
        self.machine_base=Sprite(Game.assets[MACHINE_BASE])
        self.machine_base.rect.x=0
        self.machine_base.rect.y=self.height*0.05
    # self.surface.blit(Game.assets[OVEN],(prod_rect.bottomleft[0],prod_rect.y- Game.assets[OVEN].get_height()))
        self.productionLine=Sprite(Game.assets[PROD_LINE])
        self.productionLine.rect.x=self.width*0.18
        self.productionLine.rect.y=self.height-self.productionLine.height 
        # oven
        self.oven=Sprite(Game.assets[OVEN])
        self.oven.rect.x=self.productionLine.rect.bottomleft[0]
        self.oven.rect.y=self.productionLine.rect.y- self.oven.height

        #packaging
        self.packaging=Sprite(Game.assets[PACKAGING])
        self.packaging.rect.x=self.productionLine.rect.bottomright[0]
        self.packaging.rect.y=self.height- self.packaging.height 
        # hand
        # self.hand=Sprite(Game.assets[HAND])
        # self.hand.totalFrames=len(Game.assets[HAND])

        self.player=Player( Game.assets[HAND],self)
        self.player.totalFrames=len(Game.assets[HAND])

   

        
        #cheese pool       
        for i in range(0,TOTAL_CHEESE):
            # cheese
            cheese=Sprite(Game.assets[CHEESE],CHEESE)
            cheese.position['x']= self.oven.rect.x
            cheese.position['y']= self.oven.rect.y+10
            cheese.platform=self.productionLine

            self.cheese_reserve.append(cheese)

            packagedCheese=Sprite(Game.assets[PACKAGED_CHEESE],PACKAGED_CHEESE)
            packagedCheese.surface=pygame.transform.rotate(packagedCheese.surface,-60)
            packagedCheese.position['x']=self.packaging.rect.x
            packagedCheese.position['y']=self.packaging.rect.y
            packagedCheese.isSliding=True
            # packagedCheese.rect.x=self.packaging.rect.x
            # packagedCheese.rect.y= self.packaging.rect.y
            

            self.reservedPackagedCheesePool.append(packagedCheese)


            if i%2==0:
               badcheese=Sprite(Game.assets[BAD_CHEESE],BAD_CHEESE)
               badcheese.position['x']= self.oven.rect.x
               badcheese.position['y']= self.oven.rect.y+10
               badcheese.platform=self.productionLine
               self.cheese_reserve.append(badcheese)

               badchhesepk=Sprite(Game.assets[BAD_PK_CHEESE],BAD_PK_CHEESE)
               badchhesepk.surface=pygame.transform.rotate(badchhesepk.surface,-60)
               badchhesepk.position['x']=self.packaging.rect.x
               badchhesepk.position['y']=self.packaging.rect.y
               badchhesepk.isSliding=True

               self.reservedPackagedCheesePool.append(badchhesepk)
      

        self.garbage=Sprite(Game.assets[GARBAGE],GARBAGE)
        
        self.garbage.rect.x=self.width*0.002
        self.garbage.rect.y=self.height-self.garbage.height
        # schedules cheese spawn 

        #changing screen
        pygame.event.post(pygame.event.Event(CHANGE_SCREEN_EVENT,{SCREEN_TYPE:MENU_SCREEN}))



        

                

    def drawGameScreen(self):
        self.surface.blit(Game.assets[BG1],(0,0))
        # pygame.draw.rect(self.surface,'green',Game.assets[MACHINE_BASE].get_rect() ,2,4)

        # prod_rect=self.surface.blit(Game.assets[PROD_LINE],(self.width*0.18,self.height- Game.assets[PROD_LINE].get_height() ))
        

        # self.surface.blit(Game.assets[OVEN],(prod_rect.bottomleft[0],prod_rect.y- Game.assets[OVEN].get_height()))
        
        self.machine_base.update(self.surface)
        self.player.update(self.surface)

        self.productionLine.update(self.surface)
        
        
        for cheese in self.cheese_pool:
             

              cheese.update(self.surface)
        for cheese in self.cheese_pool:
              if cheese.isOutOfProductionLine(self.productionLine)[0] :
                    reserveCheese=self.cheese_pool.pop(self.cheese_pool.index(cheese))
                    self.cheese_reserve.append(reserveCheese)
                    if cheese.isOutOfProductionLine(self.productionLine)[1]:
                        spriteType=None
                        if cheese.spriteType==CHEESE:
                          spriteType=PACKAGED_CHEESE
                        else:
                          spriteType=BAD_PK_CHEESE
                        pygame.event.post(pygame.event.Event(SPAWN_PACKAGE_EVENT,{SPRITE_TYPE:spriteType}))
              if cheese.rect.colliderect(self.garbage.rect):
                   reserveCheese=self.cheese_pool.pop(self.cheese_pool.index(cheese))
                   self.cheese_reserve.append(reserveCheese)
                   points=0
                   if cheese.spriteType==CHEESE:
                        points=-2
                        
                   else:
                        points=1
                   pygame.event.post(pygame.event.Event(FLASH_POINTS_EVENT,{POINTS:points}))
                   
                        

                            
                           

        for pk_cheese in self.packagedCheesePool:
            if pk_cheese.isOutOfProductionLine()[0] :
                    reserveCheese=self.packagedCheesePool.pop(self.packagedCheesePool.index(pk_cheese))
                    self.reservedPackagedCheesePool.append(reserveCheese)
                    
                    if pk_cheese.spriteType==PACKAGED_CHEESE:
                         self.levelProgress+=self.productionBarWidth*0.1
                         self.score+=5

                    else:
                         self.levelProgress-=self.productionBarWidth*0.1
                         self.score-=2
                         
                    if self.levelProgress<0:
                         self.levelProgress=0
                    elif self.levelProgress>=self.productionBarWidth:
                         self.levelProgress=self.productionBarWidth*0.98  

                    
                    

                         
            pk_cheese.update(self.surface)

        self.packaging.update(self.surface)
        self.oven.update(self.surface)
        self.garbage.update(self.surface)


   
        

    def drawMenuScreen(self):
                # rendering title

                titletxt=self.fontLarge.render("Cheese Factory", True, 'white')
                # titletxt=pygame.transform.scale_by(titletxt,1.8)
                titleRect=titletxt.get_rect()
                titleRect.centerx=self.width*0.5
                titleRect.centery=self.height*0.34
                self.surface.blit(titletxt,titleRect)

                # rendering playButton
                self.btRect=self.button.get_rect()
                self.btRect.centerx=self.width*0.5
                self.btRect.y=self.height*0.42

                
                buttonText=self.font.render("Start", False, 'white')
                # pygame.draw.rect(self.surface,'green', self.btRect,2,3)
                buttonTextRect=buttonText.get_rect()
                buttonTextRect.centerx= self.btRect.centerx
                buttonTextRect.centery= self.btRect.centery
                
                self.surface.blit(self.button, self.btRect)
                self.surface.blit(buttonText,buttonTextRect)


                # rendering quitbutton
                self.quitRect=self.button.get_rect()
                self.quitRect.centerx=self.width*0.5
                self.quitRect.y=self.height*0.42+self.btRect.height+20
                
                self.quitButton=Sprite(self.button.__copy__() )
                self.quitButton.rect.centerx=self.quitRect.centerx
                self.quitButton.rect.centery=self.quitRect.centery

                self.quitButton.update(self.surface)
                quittext=self.font.render("Quit", False, 'white')
                quittextrect=quittext.get_rect()
                quittextrect.centerx= self.quitRect.centerx
                quittextrect.centery= self.quitRect.centery

                self.surface.blit(quittext,quittextrect)
                



    def drawHud(self):
         productionBar=pygame.Rect(self.width*0.75,self.height*0.02,self.productionBarWidth,self.height*0.04)

         progress=pygame.Rect(self.width*0.751,self.height*0.025,self.width*0.19,self.height*0.035)
         progress.width=self.levelProgress

       
        #  productionBar.clamp
        #  pygame.draw.rect(self.surface,'red',productionBar,1,1)


        #  self.surface.fill('blue',progress)

         
         timer=Sprite(self.font.render("Time: "+str(self.levelTimer), True, 'white'))
         timer.rect.x=progress.x
         timer.rect.y=progress.bottom+15
         self.surface.blit(timer.surface,timer.rect)

         score=Sprite(self.font.render("Score: "+str(self.score), True, 'white'))
         score.rect.x=progress.x
         score.rect.y=progress.top
         self.surface.blit(score.surface,score.rect)
         if self.score<0:
                         self.score=0

         if self.isFlashingPoint:
              self.rew_Pen_User(self.flashPoint)
         if self.levelTimer<=0 :
              dialog=Sprite(self.dialog)
              self.isGameOver=True
              dialog.rect.centerx=self.width*0.5
              dialog.rect.centery=self.height*0.5
              
              yourScore=Sprite(self.font.render('Your Score:'+str(self.score), True, 'white'))
              replay=Sprite(self.font.render('Replay', True, 'white'))
              menu=Sprite(self.font.render('Menu', True, 'white'))
              
              yourScore.rect.centerx=dialog.rect.centerx
              yourScore.rect.centery=dialog.rect.y+dialog.height*0.2
              
              replay.rect.centerx=dialog.rect.centerx
              replay.rect.centery=dialog.rect.y+dialog.height*0.45

              menu.rect.centerx=dialog.rect.centerx
              menu.rect.centery=dialog.rect.y+dialog.height*0.66

              self.replayButton=replay
              self.menuButton=menu
              
              dialog.update(self.surface)
              yourScore.update(self.surface)
              menu.update(self.surface)
              replay.update(self.surface)
              
            #   pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
              pygame.time.set_timer(pygame.event.Event(GAME_OVER_EVENT),10,1)
            #   print('triggered')
            #   self.running=False
              

         


         
         
        #  pygame.draw.rect(self.surface,'blue',progress,11,5)


    def rew_Pen_User(self,points):
         point=Sprite(self.font.render('{0:+}'.format(points), True, 'white') )
         point.rect.x=self.oven.rect.x
         point.rect.y=self.oven.rect.y-50
         self.surface.blit(point.surface,point.rect)
         if self.timer%120==0:
              self.isFlashingPoint=False
         
         
         
    def events(self):
     for event in pygame.event.get():
            if event.type==pygame.QUIT:sys.exit()
            
            if event.type==ASSETS_LOADED_EVENT:
                self.scaleAssets()
                print('assets transformed')
            if event.type==SPAWN_CHEESE_EVENT:
                # print('swpawing cheese')
                if(len(self.cheese_reserve))!=0:
                    # self.cheese_pool[0].isMoving=True
                    pool_cheese=self.cheese_reserve.pop()
                    pool_cheese.position['x']= self.oven.rect.x
                    pool_cheese.rect.x= pool_cheese.position['x']
                    pool_cheese.rect.y= self.oven.rect.y+10
                    pool_cheese.isPickedUp=False
                    # pass
                    pool_cheese.isMoving=True
                    pool_cheese.isAffectedByGv=True
                    
                    self.cheese_pool.append(pool_cheese)
                #   self.cheese_pool[0].isAffectedByGv=True
                #   self.cheese_pool[0].platform=self.productionLine

            if event.type==SPAWN_PACKAGE_EVENT:
                  
                  if(len(self.reservedPackagedCheesePool))!=0:
                     for pch in self.reservedPackagedCheesePool:
                          if event.dict[SPRITE_TYPE]==pch.spriteType:
                            index=self.reservedPackagedCheesePool.index(pch)
                            packagedCheese=self.reservedPackagedCheesePool.pop(index)
                            packagedCheese.position['x']=self.packaging.rect.x
                            packagedCheese.position['y']=self.packaging.rect.y
                            packagedCheese.rect.x=self.packaging.rect.x
                            packagedCheese.rect.y= self.packaging.rect.y
                    
                            self.packagedCheesePool.append(packagedCheese)
                            break
                     
                    # self.cheese_pool[0].isMoving=True
            
            if event.type==CHANGE_SCREEN_EVENT:
                 
                 screen=event.dict[SCREEN_TYPE]
                 if screen==GAME_SCREEN:
                        self.restoreCheese()
                        pygame.time.set_timer(SPAWN_CHEESE_EVENT,1000)
                        self.levelTimer=LEVEL_TIME
                        self.score=0
                        
                        # self.levelTimer=pygame.time.Clock().get_time()

                 Game.currentScreen=screen
                 self.running=True
            if event.type==FLASH_POINTS_EVENT:
                 self.isFlashingPoint=True
                 self.flashPoint=event.dict[POINTS]
                 self.score+=event.dict[POINTS]
            if event.type==GAME_OVER_EVENT:
                 print('game overr')

                 pygame.time.set_timer(SPAWN_CHEESE_EVENT,0)
                 self.running=False
        
            if event.type==pygame.MOUSEMOTION:
                   pass
                   
            if event.type==pygame.MOUSEBUTTONUP:
                  pass
                              
            if event.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] :
                # self.running=True
                
                try:
                      if  self.btRect.collidepoint(pygame.mouse.get_pos()) and Game.currentScreen==MENU_SCREEN:
                        
                        pygame.event.post(pygame.event.Event(CHANGE_SCREEN_EVENT,{SCREEN_TYPE:GAME_SCREEN}))
                except:
                    pass
                try:

                      if  self.replayButton.rect.collidepoint(pygame.mouse.get_pos()) and Game.currentScreen==GAME_SCREEN:
                        
                         pygame.event.post(pygame.event.Event(CHANGE_SCREEN_EVENT,{SCREEN_TYPE:GAME_SCREEN}))
                    
                except:pass
                try:
                      
                      if  self.menuButton.rect.collidepoint(pygame.mouse.get_pos()) and Game.currentScreen==GAME_SCREEN:
                         
                         pygame.event.post(pygame.event.Event(CHANGE_SCREEN_EVENT,{SCREEN_TYPE:MENU_SCREEN}))

                except Exception as e:
                    print(e)
                    pass
                try:
                      
                      if  self.quitButton.rect.collidepoint(pygame.mouse.get_pos()) and Game.currentScreen==MENU_SCREEN:
                         quit()
                         
                        
                except Exception as e:
                    print(e)
                    pass

                        #  print('switching to gamescreen')                 

            
            if event.type==pygame.KEYDOWN:
                 
                 if event.key==pygame.K_RIGHT or event.key==pygame.K_d:  
                     self.player.isSlidingRight=True
                    #   self.isSliding=True

                      
                 if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                        self.player.isSlidingLeft=True

                      
                 if event.key==pygame.K_UP  or event.key==pygame.K_w:
                       pass
                 if event.key==pygame.K_DOWN  or event.key==pygame.K_s:
                        pass  
                 if event.key in [pygame.K_SPACE,pygame.K_x]:
                       self.player.isPickingUp=True
                    #up events 
            if event.type==pygame.KEYUP:
                 
                 if event.key==pygame.K_RIGHT or event.key==pygame.K_d:  
                            self.player.isSlidingRight=False

                 if event.key in [pygame.K_SPACE,pygame.K_x]:
                       self.player.isPickingUp=False
                      
                 if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                        self.player.isSlidingLeft=False

                      
                 if event.key==pygame.K_UP  or event.key==pygame.K_w:
                       pass
                 if event.key==pygame.K_DOWN  or event.key==pygame.K_s:
                        pass   
    
    





















