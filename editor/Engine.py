import pygame, sys # import pygame and sys
from random import * # import random library
import colorsys # import colorsys library to convert color code
from pygame.locals import * # import pygame modules
from Player import Player
from Camera import Camera
import json

class Chunk:
    
    def __init__(self, engine, x, y, tiles):
        self.engine = engine
        self.x = x
        self.y = y
        self.tiles_list = tiles
        self.tiles = None
        self.tiles_loaded = False

    def setTiles(self, tiles):
        self.tiles = tiles
        
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
            while key not in organizedTile.keys():
                key = key +1
            new_tiles = new_tiles + organizedTile[key]
            key = key + 1
        return new_tiles
    
    def getList(self):
        return self.tiles_list

    def getTiles(self):
        tiles_list = self.getList()
        new_tiles_list = []
        for tile in tiles_list:
            tile = tile.split("#")
            new_tiles_list.append(Tile(self.engine.tiles_name[tile[0]], self.engine.tiles_type[tile[0]], int(tile[3]), int(tile[4]), int(tile[1]), tile[2], tile[5], (int(tile[6]), int(tile[7]), int(tile[8]))))
        return new_tiles_list
    
    def getTilesList(self):
        return self.tiles_list
    
    def addTile(self, tile):   # id#layer#collision#x#y#entity#colkey
        new_tile = str(self.engine.getId()[tile.texture_path])
        new_tile = new_tile + "#" + str(tile.layer)
        new_tile = new_tile + "#" + str(tile.collision)
        new_tile = new_tile + "#" + str(tile.x)
        new_tile = new_tile + "#" + str(tile.y)
        new_tile = new_tile + "#" + str(tile.entity)
        new_tile = new_tile + "#" + str(tile.colkey[0])
        new_tile = new_tile + "#" + str(tile.colkey[1])
        new_tile = new_tile + "#" + str(tile.colkey[2])
        #detect if tile exist in the same coord and layer
        detected = False
        for tile_map in self.tiles:
            if tile_map.x//16 == tile.x and tile_map.y//16 == tile.y and tile_map.layer == tile.layer:
                detected = tile_map     
        if detected is False:
            self.tiles_list.append(new_tile)
        else:
            for tile_map in self.tiles_list:
                tile_test = tile_map.split("#")
                tile_test_layer = int(tile_test[1])
                tile_test_x = int(tile_test[3])
                tile_test_y = int(tile_test[4])
                if tile_test_x == tile.x and tile_test_y == tile.y and tile_test_layer == tile.layer:
                    self.tiles_list.remove(tile_map)
            self.tiles.remove(detected)
            self.tiles_list.append(new_tile)
        self.setTiles(self.getTiles())
        self.tiles_loaded = False

class Engine:

    def __init__(self, file):

        self.files = self.loadFile(file)
        self.name = self.getName(self.files)
        self.height = self.getHeight(self.files)
        self.width = self.getWidth(self.files)
        self.tiles_type = self.getTilesType(self.files)
        self.tiles_name = self.getTilesName(self.files)
        self.tiles_id = self.getTilesId(self.files)
        self.chunks_list = self.getChunksList(self.files)
        self.chunks = self.getChunks(self.files)
    
    def loadFile(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
        return data

    def setFile(self, file):
        self.files = file

    def getTypes(self):
        return self.tiles_type
    
    def getId(self):
        return self.tiles_id
    
    def getNames(self):
        return self.tiles_name
        
    def getName(self, file):
        return self.files['name']

    def getHeight(self, file):
        return self.files['height']

    def getWidth(self, file):
        return self.files['width']
    
    def getTilesType(self, file):
        return self.files['tiles_type']
    
    def getTilesName(self, file):
        return self.files['tiles_name']
    
    def getTilesId(self, file):
        return self.files['tiles_id']
    
    def getChunksList(self, file = None):
        if file == None:
            return self.chunks_list
        return self.files['chunks']
    
    def getChunks(self, file = None):
        if file != None:
            chunks = []
            for chunk in self.getChunksList():
                chunk_split = chunk.split("#")
                chunks.append(Chunk(self, int(chunk_split[1]), int(chunk_split[2]), self.getChunksList()[chunk]))
            return chunks
        else:
            return self.chunks
    
    def setChunksListbyChunks(self):
        new_chunks_list = {}
        for chunk in self.getChunks():
            if chunk.tiles_list != []:
                str_chunk = "chunk"
                str_chunk = str_chunk + "#" + str(chunk.x)
                str_chunk = str_chunk + "#" + str(chunk.y)
                new_chunks_list[str_chunk] = chunk.tiles_list
        self.chunks_list = new_chunks_list
    
    def getChunk(self, x, y):
        for chunk in self.getChunks():
            if chunk.x == x and chunk.y == y:
                return chunk
        
    def addChunk(self, chunk):
        self.chunks.append(chunk)

class Tile:

    def __init__(self, name, texture, x, y, layer, collision, entity, colkey):
        self.name = name
        self.texture_path = texture
        self.texture = pygame.image.load(texture).convert()
        self.layer = layer
        self.collision = collision
        self.entity = entity    
        self.colkey = colkey
        if entity == "0":
            self.x = x*16
            self.y = y*16
        else:
            self.x = x
            self.y = y
        if colkey[0] < 256 and colkey[1] < 256 and colkey[2] < 256:
            self.texture.set_colorkey(colkey)

    def draw(self, surface):
        surface.blit(self.texture, (self.x, self.y))
        
    def draw_with_camera(self, surface, camera, chunk_offset=(0,0)):
        draw_rect = camera.apply(pygame.Rect(self.x + chunk_offset[0], self.y + chunk_offset[1], 16, 16))
        surface.blit(self.texture, draw_rect)
        
    def getLayer(self):
        return self.layer
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)

def convert_mouse_coords(coords, screen):
    x = coords[0] - 750
    x_coef = 600 / 256
    x = x / x_coef
    y = coords[1]
    y_coef = screen[1] / 320
    y = y / y_coef
    return (round(x), round(y))

def convert_mouse_coords_canvas(coords, screen):
    x = coords[0]
    x_coef = 750 / 320
    x = x / x_coef
    y = coords[1]
    y_coef = screen[1] / 320
    y = y / y_coef
    return (round(x)//16, round(y)//16)

def detect_block_at_x_y(coords, tiles):
    coords_rect = Rect(coords[0], coords[1], 1, 1)
    for tile in tiles:
        if coords_rect.colliderect(tile):
            return tile
    return None

def get_type_of_block_by_tile(tile_detected, tiles):
    for tile in tiles:
        if tile.x == tile_detected.x and tile.y == tile_detected.y:
            return tile
        
def get_type_of_block_by_coords(coords, tiles, selected_layer):
    for tile in tiles:
        if tile.x//16 == coords[0] and tile.y//16 == coords[1] and str(selected_layer) == tile.layer:
            return tile
    return None
    
##### DEBUG ######

def test():
    clock = pygame.time.Clock()
    pygame.init()
    Map = Engine("test.json")
    pygame.display.set_caption(Map.name)
    WINDOW_SIZE = (Map.width, Map.height)
    screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
    canvas = pygame.Surface((320,320))
    police = pygame.font.SysFont("verdana",50)
    parameter_police = pygame.font.SysFont("verdana",35)
    test_print = True
    player = Player(160, 160)  # Position de départ au centre
    camera = Camera(320, 320)
    page_selectionner = 0
    
    chunk_selected = [0, 0]
    
    while True:
        canvas.fill((255,0,0))
        # CHUNKS 3x3 à dessiner autour du joueur
        chunks_to_draw = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cx = chunk_selected[0] + dx
                cy = chunk_selected[1] + dy
                chunk = Map.getChunk(cx, cy)
                if chunk is not None:
                    # Assure que les tiles sont bien préparés
                    if not chunk.tiles_loaded:
                        chunk.setTiles(chunk.getTiles())
                        chunk.setTiles(chunk.organizeTile())
                        chunk.tiles_loaded = True
                    if dx == 0 and dy == 0:
                        central_chunk = chunk
                    chunks_to_draw.append(chunk)

        # Dessin des tiles pour tous les chunks chargés
        CHUNK_SIZE_IN_TILES = 16  # à adapter selon ta config
        TILE_SIZE = 20  # taille d'une tile en pixels
        CHUNK_PIXEL_SIZE = CHUNK_SIZE_IN_TILES * TILE_SIZE
        for chunk in chunks_to_draw:
            chunk_offset = (chunk.x * CHUNK_PIXEL_SIZE - chunk_selected[0] * CHUNK_PIXEL_SIZE, chunk.y * CHUNK_PIXEL_SIZE - chunk_selected[1] * CHUNK_PIXEL_SIZE)
            for tile in chunk.tiles:
                tile.draw_with_camera(canvas, camera, chunk_offset)
        
        # Récupère les tiles solides
        solid_tiles = [tile for tile in central_chunk.tiles if tile.collision == "1"]
        
        # Mouvement Joueur
        keys = pygame.key.get_pressed()
        player.move(keys, Map, camera, chunk_selected, solid_tiles)
        camera.update(player, Map, chunk_selected)
        
        player.draw_with_camera(canvas, camera)
        
        # Affichage
        canvas_surf = pygame.transform.scale(canvas, (Map.width, Map.height))
        screen.blit(canvas_surf, (0, 0))
        
        # Event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update() # update display
        clock.tick(60) # maintain 60 fps

test()