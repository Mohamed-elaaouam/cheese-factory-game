from Game import *


game=Game()

def animationLoop():
    game.events()
    game.draw()
    game.update()
    animationLoop()




animationLoop()
