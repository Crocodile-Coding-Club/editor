import pygame, sys # import pygame and sys
from random import * # import random library
import colorsys # import colorsys library to convert color code
from pygame.locals import * # import pygame modules
import json

class Engine:

    def __init__(self, file):

        self.files = self.loadFile(file)
        self.name = self.getName(self.files)
        self.height = self.getHeight(self.files)
        self.width = self.getWidth(self.files)
        self.tiles_type = self.getTilesType(self.files)
        self.tiles_name = self.getTilesName(self.files)
        self.tiles_id = self.getTilesId(self.files)
        self.tiles = None
    
    def loadFile(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
        return data

    def getName(self, file):
        return self.files['name']

    def getHeight(self, file):
        return self.files['height']

    def getWidth(self, file):
        return self.files['width']

    def getTiles(self, file):
        tiles_list = self.files['tiles']
        new_tiles_list = []
        for tile in tiles_list:
            tile = tile.split("#")
            new_tiles_list.append(Tile(self.tiles_name[tile[0]], self.tiles_type[tile[0]], int(tile[3]), int(tile[4]), tile[1], tile[2], tile[5], (int(tile[6]), int(tile[7]), int(tile[8]))))
        return new_tiles_list

    def organizeTile(self):
        organizedTile = {}
        new_tiles = []
        for tile in self.tiles:
            if tile.getLayer() in organizedTile.keys():
                organizedTile[tile.getLayer()].append(tile)
            else:
                organizedTile[tile.getLayer()] = [tile]
        key = 0
        for i in range(len(organizedTile)):
            while str(key) not in organizedTile.keys():
                key = key +1
            new_tiles = new_tiles + organizedTile[str(key)]
            key = key + 1
        return new_tiles
    
    def getTilesType(self, file):
        return self.files['tiles_type']
    
    def getTilesName(self, file):
        return self.files['tiles_name']
    
    def getTilesId(self, file):
        return self.files['tiles_id']

    def setTiles(self, tiles):
        self.tiles = tiles

class Tile:

    def __init__(self, name, texture, x, y, layer, collision, entity, colkey):
        self.name = name
        self.texture = pygame.image.load(texture).convert()
        self.layer = layer
        self.collision = collision
        self.entity = entity
        if entity == "0":
            self.x = x*16
            self.y = y*16
        else:
            self.x = x
            self.y = y
        if colkey != (256, 256, 256):
            self.texture.set_colorkey(colkey)

    def draw(self, surface):
        surface.blit(self.texture, (self.x, self.y))
        
    def getLayer(self):
        return self.layer

##### DEBUG ######

def test():
    clock = pygame.time.Clock() # set up the clock
    pygame.init() # initiate pygame
    Map = Engine("test.json")
    pygame.display.set_caption(Map.name) # set the window name
    WINDOW_SIZE = (Map.width, Map.height) # set up window size
    screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
    display = pygame.Surface((320,320))
    Map.setTiles(Map.getTiles(Map.files))

    while True:
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                pygame.quit() # stop pygame
                sys.exit() # stop script
        Map.setTiles(Map.organizeTile())
        for tile in Map.tiles:
            tile.draw(display)
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update() # update display
        clock.tick(60) # maintain 60 fps

test()