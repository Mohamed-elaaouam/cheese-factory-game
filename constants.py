

import pygame


GAME_WIDTH=1247
GAME_HEIGHT=666
GAME_TITLE="Cheese Factory"
GAME_SCALE=0.77
# GAME_SCALE=0.55
TRANSPARENT=(0,0,0,0)
CURSOR_POINTER=11

# screens
MENU_SCREEN='MENU_SCREEN'
GAME_SCREEN='GAME_SCREEN'
LOADING_SCREEN="LOADING_SCREEN"


# events
ASSETS_LOADED_EVENT = pygame.event.custom_type()
SPAWN_CHEESE_EVENT=pygame.event.custom_type()
SPAWN_PACKAGE_EVENT=pygame.event.custom_type()
CHANGE_SCREEN_EVENT=pygame.event.custom_type()
FLASH_POINTS_EVENT=pygame.event.custom_type()
GAME_OVER_EVENT=pygame.event.custom_type()

# assets names
OVEN="oven"
GARBAGE="garbage"
HAND_OPEN="HAND_OPEN"
CHEESE="CHEESE"
HAND_CLOSED="HAND_CLOSED"
MACHINE_BASE="MACHINE_BASE"
PACKAGED_CHEESE="PACKAGED_CHEESE"
PROD_LINE="PROD_LINE"
TRAIL="TRAIL"
BAD_CHEESE="BAD_CHEESE"
BAD_PK_CHEESE="BAD_PK_CHEESE"

BG1="bg.png"
PACKAGING="PACKAGING"
HAND="HAND"
# paths
IMG_PATH='assets/img/'
FONT_ANTA='assets/font/Anta/Anta-Regular.ttf'
FONT_COINY='assets/font/Coiny/Coiny-Regular.ttf'
SPRITE_TYPE="SPRITE_TYPE"
SCREEN_TYPE="SCREEN_TYPE"

POINTS="points"
LEVEL_TIME=60
TOTAL_CHEESE=7