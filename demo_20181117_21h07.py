# World of isotiles
# Author: nicolas.bredeche(at)sorbonne-universite.fr
#
# Started: 2018-11-17
# purpose: basic code for teaching artificial life ecological simulation at SU (2i013 Projet, Vie Artificielle).
# licence: CC-BY-SA
#
# Ressources used during development:
# - credits for assets: https://www.kenney.nl/assets/isometric-blocks (Isometric Blocks by  Kenney Vleugels)
# - https://stackoverflow.com/questions/20629885/how-to-render-an-isometric-tile-based-world-in-python
#
# Random bookmarks:
# - https://stackoverflow.com/questions/43196126/how-do-you-scale-a-design-resolution-to-other-resolutions-with-pygame
# - http://www-cs-students.stanford.edu/~amitp/game-programming/grids/

import pygame
from pygame.locals import *
import sys
import datetime
from random import *
import math

###

pygame.init()

screenWidth = 1000
screenHeight = 700

screen = pygame.display.set_mode((screenWidth, screenHeight), DOUBLEBUF)

pygame.display.set_caption('World of Isotiles')

FPSCLOCK = pygame.time.Clock()

###

# spritesheet-specific -- as stored on the disk ==> !!! here, assume 128x111 with 64 pixels upper-surface !!!
# Values will be updated *after* image loading and *before* display starts
tileTotalWidth = 111  # width of tile image
tileTotalHeight = 128 # height of tile image
tileVisibleHeight = 64 # height "visible" part of the image, i.e. top part without subterranean part

scaleMultiplier = 0.5

def loadImage(filename):
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidth*scaleMultiplier), int(tileTotalHeight*scaleMultiplier)))
    return image

tileType = [
    loadImage('assets/isometric-blocks/PNG/Platformer tiles/platformerTile_48.png'), # grass
    loadImage('assets/isometric-blocks/PNG/Platformer tiles/platformerTile_33.png'), # brick
    loadImage('assets/isometric-blocks/PNG/Abstract tiles/abstractTile_12.png'), # blue grass (?)
    loadImage('assets/isometric-blocks/PNG/Abstract tiles/abstractTile_09.png') # grey brock
]

# re-scale reference image size -- must be done *after* loading sprites
tileTotalWidth = tileTotalWidth * scaleMultiplier  # width of tile image, as stored in memory
tileTotalHeight = tileTotalHeight * scaleMultiplier # height of tile image, as stored in memory
tileVisibleHeight = tileVisibleHeight * scaleMultiplier # height "visible" part of the image, as stored in memory

heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight

###

terrainMap = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

heightMap = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 2, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 2, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

###

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 3*tileTotalHeight # border. Could be 0.

# set scope of displayed tiles
xVisibleTileStart = 0
xVisibleTileEnd = len(terrainMap)
yVisibleTileStart = 0
yVisibleTileEnd = len(terrainMap[0])

addNoise = True

###

def initWorld( it = 0 ):
    for yTile in range(yVisibleTileEnd-yVisibleTileStart):
        for xTile in range(xVisibleTileEnd-xVisibleTileStart):
            # assume: north-is-upper-right

            noise = 0
            if addNoise == True: # add sinusoidal noise on height positions
                noise = math.sin(it/23+yTile) * math.sin(it/7+xTile) * heightMultiplier/10 + math.cos(it/17+yTile+xTile) * math.cos(it/31+yTile) * heightMultiplier
                noise = math.sin(it/199) * noise
            height = (heightMap[xTile+yVisibleTileStart][yTile+yVisibleTileStart]+1) * heightMultiplier + noise

            xScreen = xScreenOffset + xTile * tileTotalWidth / 2 - yTile * tileTotalWidth / 2
            yScreen = yScreenOffset + yTile * tileVisibleHeight / 2 + xTile * tileVisibleHeight / 2 - height
            screen.blit( tileType[terrainMap[xTile+yVisibleTileStart][yTile+yVisibleTileStart]] , (xScreen, yScreen))
            #screen.blit( tileType[terrainMap[randint(0,14)][randint(0,15)]] , (xScreen, yScreen))

###

timestamp = datetime.datetime.now().timestamp()

initWorld()
print ("initWorld:",datetime.datetime.now().timestamp()-timestamp)
timestamp = datetime.datetime.now().timestamp()

it = 0

userExit = False

while userExit == False:

    pygame.draw.rect(screen, (0,0,0), (0, 0, screenWidth, screenHeight), 0)
    #pygame.display.update()

    initWorld(it)

    it += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                userExit = True

    pygame.display.flip()
    FPSCLOCK.tick(120) # recommended: 30 fps

fps = it / ( datetime.datetime.now().timestamp()-timestamp )
print ("Stop.", fps,"per seconds")

pygame.quit()
sys.exit()
