import pygame, sys # import pygame and sys
from random import * # import random library
import colorsys # import colorsys library to convert color code
from pygame.locals import * # import pygame modules
import json

class Case:
    def __init__(self, x, y, x_col, y_col):
        self.x = x
        self.y = y
        self.x_col = x_col
        self.y_col = y_col
        self.operated = False
        self.value = 0

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.box_col.collidepoint(event.pos):
            self.operated = not self.operated
            self.value = (self.value+1)%2

    def draw(self, screen):
        # j'ai rien compris à ton histoire de coeff du coup pour changer les collisions c'est à la main
        self.box_col = pygame.Rect(self.x_col, self.y_col, 15*(600/256), 15*(600/256))
        self.box_draw = pygame.Rect(self.x, self.y, 15, 15)
        if not self.operated:
            pygame.draw.rect(screen, (0,0,0), self.box_draw, 1)
        else:
            pygame.draw.rect(screen, (0,0,0), self.box_draw, 0)

class InputBoxNum:
    def __init__(self, x, y, width, height, value, police_size, lim_input, x_col, y_col):
        self.x = x
        self.y = y
        self.x_col = x_col
        self.y_col = y_col
        self.width = width
        self.height = height
        self.selected = False
        self.color = (0,0,0)
        self.value = value
        self.text = str(value)
        self.police_size = police_size
        self.lim_input = lim_input

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.color = (0,0,255)
            else:
                self.color = (0,0,0)
                self.text = str(self.value)

        if event.type != pygame.KEYDOWN or self.color == (0,0,0):
            return 

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            if len(self.text) < 39:
                if event.unicode in ["0","1","2","3","4","5","6","7","8","9"] and len(self.text)<self.lim_input:
                    self.text += event.unicode
                if event.key == pygame.K_RETURN:
                    self.selected = False
                    self.value = int(self.text)
                    self.color = (0,0,0)

    def draw(self, screen):
        self.draw_surface = pygame.Rect(self.x, self.y, self.width, self.height)
        # j'ai rien compris à ton histoire de coeff du coup pour changer les collisions c'est à la main
        self.input_box = pygame.Rect(self.x_col, self.y_col, self.width*(600/256), self.height*(600/256))
        pygame.draw.rect(screen, (255,255,255), self.draw_surface, 0)
        pygame.draw.rect(screen, self.color, self.draw_surface, 1)
        
        self.font = pygame.font.SysFont("arial", self.police_size)
        txt_surface = self.font.render(self.text, 1, (0,0,0))
        screen.blit(txt_surface, (self.draw_surface.x+3, self.draw_surface.y+1))

class Chunk:
    
    def __init__(self, engine, x, y, tiles):
        self.engine = engine
        self.x = x
        self.y = y
        self.tiles_list = tiles
        self.tiles = None

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

        self.layer_inputbox = InputBoxNum(131, 62, 20, 20, 1, 15, 2, 1055, 145)
        self.collision_case = Case(200, 65, 1220, 150)
        self.is_entity_case = Case(135, 110, 1065, 260)
        self.colkey_input_r = InputBoxNum(180, 110, 22, 15, 0, 10, 3, 1173, 260)
        self.colkey_input_g = InputBoxNum(203, 110, 22, 15, 0, 10, 3, 1227, 260)
        self.colkey_input_b = InputBoxNum(226, 110, 22, 15, 0, 10, 3, 1282, 260)
    
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

def register(file, chunks):
    with open(file, 'r') as f:
        old_data = json.load(f)
    new_data = {
        "name": old_data["name"],
        "width": old_data["width"],
        "height": old_data["height"],
        "chunks": chunks,
        "tiles_type": old_data["tiles_type"],
        "tiles_id": old_data["tiles_id"],
        "tiles_name": old_data["tiles_name"],
    }
    with open(file, 'w') as f:  
        json.dump(new_data, f, indent = 2)
    return new_data

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
        
    def getLayer(self):
        return self.layer

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
    WINDOW_SIZE = (Map.width+600, Map.height)
    screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
    canvas = pygame.Surface((320,320))
    editor = pygame.Surface((256,320)) 
    police = pygame.font.SysFont("verdana",50)
    parameter_police = pygame.font.SysFont("verdana",35)
    test_print = True
    page_selectionner = 0
    
    #Selected tile, layer, collision, entity, colkey
    selected_tile = None
    #A Faire à selectionner grâce à des entrées et des boutons
    selected_layer = Map.layer_inputbox.value
    selected_collision = Map.collision_case.value
    selected_entity = Map.is_entity_case.value
    selected_colkey = (Map.colkey_input_r.value, Map.colkey_input_g.value, Map.colkey_input_b.value)
    chunk_selected = [0, 0]
    
    while True:
        selected_layer = Map.layer_inputbox.value
        selected_collision = Map.collision_case.value
        selected_entity = Map.is_entity_case.value
        selected_colkey = (Map.colkey_input_r.value, Map.colkey_input_g.value, Map.colkey_input_b.value)
        chunk = Map.getChunk(chunk_selected[0], chunk_selected[1])
        if chunk == None:
            chunk = Chunk(Map, chunk_selected[0], chunk_selected[1], [])
            Map.addChunk(chunk)
        chunk.setTiles(chunk.getTiles())
        canvas.fill((0,0,0))
        canvas_mouse_coords = convert_mouse_coords_canvas(pygame.mouse.get_pos(), WINDOW_SIZE)
        pressed = pygame.mouse.get_pressed()
        if selected_tile != None and canvas_mouse_coords[0] < 20 and canvas_mouse_coords[1] < 20:
            if pressed[0]:
                chunk.addTile(Tile(selected_tile.name, selected_tile.texture_path, canvas_mouse_coords[0], canvas_mouse_coords[1], selected_layer, selected_collision, selected_entity, selected_colkey))
            
        #Canvas
        chunk.setTiles(chunk.organizeTile())
        for tile in chunk.tiles:
            tile.draw(canvas)
        canvas_surf = pygame.transform.scale(canvas, (Map.width, Map.height))
        screen.blit(canvas_surf, (0, 0))
        
        #Editor
        editor.fill((20, 120, 255))
        editor_title = police.render("EDITOR", 1 ,(255,255,255))
        layer_text = parameter_police.render("layer", 1 ,(0,0,0))
        collision_text = parameter_police.render("collision", 1 ,(0,0,0))
        entity_text = parameter_police.render("entity", 1 ,(0,0,0))
        colkey_text = parameter_police.render("colkey", 1 ,(0,0,0))
        chunk_text = parameter_police.render("chunk", 1 ,(0,0,0))
        selected_x_chunk_text = parameter_police.render("x: " + str(chunk_selected[0]), 1 ,(0,0,0))
        selected_y_chunk_text = parameter_police.render("y: " + str(chunk_selected[1]), 1 ,(0,0,0))
        page_actuel = 0
        pages = {}
        ligne = 0
        colonne = 0
        for tile_id in Map.getId():
            colonne += 1
            if colonne > 5:
                colonne = 1
                ligne += 1
                if ligne > 7:
                    ligne = 0
                    page_actuel += 1
            if str(page_actuel) in pages:
                pages[str(page_actuel)][ligne].append(Map.getId()[tile_id])
            else:
                pages[str(page_actuel)] = [[Map.getId()[tile_id]],
                                           [],
                                           [],
                                           [],
                                           [],
                                           [],
                                           [],
                                           []]
        #Event
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                pygame.quit() # stop pygame
                sys.exit() # stop script
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if page_selectionner > 0:
                        page_selectionner -= 1
                if event.key == K_RIGHT:
                    if str(page_selectionner + 1) in pages:
                        page_selectionner += 1
                if event.key == K_z:
                    if chunk_selected[1] > 0:
                        chunk_selected[1] -= 1
                if event.key == K_s:
                    chunk_selected[1] += 1
                if event.key == K_q:
                    if chunk_selected[0] > 0:
                        chunk_selected[0] -= 1
                if event.key == K_d:
                    chunk_selected[0] += 1
                if event.key == K_UP:
                    Map.setChunksListbyChunks()
                    data_new = register("test.json", Map.getChunksList())
                    Map.setFile(data_new)
            Map.layer_inputbox.update(event)
            Map.collision_case.update(event)
            Map.is_entity_case.update(event)
            Map.colkey_input_r.update(event)
            Map.colkey_input_g.update(event)
            Map.colkey_input_b.update(event)
        editor_tiles_rect = []
        editor_tiles = []
        for ligne in range(len(pages[str(page_selectionner)])):
            for colonne in range(len(pages[str(page_selectionner)][ligne])):
                if pages[str(page_selectionner)][ligne][colonne] != None:
                    editor_tiles_rect.append(Rect(colonne*16 + (20 + colonne), ligne*16 + (50 + ligne), 16, 16))
                    editor_tiles.append(Tile(Map.getNames()[pages[str(page_selectionner)][ligne][colonne]], Map.getTypes()[pages[str(page_selectionner)][ligne][colonne]], colonne*16 + (20 + colonne), ligne*16 + (50 + ligne), 0, 0, 0, (256, 256, 256)))
        
        for tile in editor_tiles:
            tile.draw(editor)
        
        Map.layer_inputbox.draw(editor)
        Map.collision_case.draw(editor)
        Map.is_entity_case.draw(editor)
        Map.colkey_input_r.draw(editor)
        Map.colkey_input_g.draw(editor)
        Map.colkey_input_b.draw(editor)

        mouse_coords = convert_mouse_coords(pygame.mouse.get_pos(), WINDOW_SIZE)
        cursor_tile_detected = detect_block_at_x_y(mouse_coords, editor_tiles_rect)
        if cursor_tile_detected is not None:
            type_of_block = get_type_of_block_by_tile(cursor_tile_detected, editor_tiles)
            if pressed[0]:
                selected_tile = type_of_block
        editor_surf = pygame.transform.scale(editor, (600, Map.height))
        
        screen.blit(editor_surf,(Map.width, 0))
        screen.blit(editor_title, (Map.width + 220, 30))
        screen.blit(layer_text, (Map.width + 290, 100))
        screen.blit(collision_text, (Map.width + 415, 100))
        screen.blit(entity_text, (Map.width + 290, 210))
        screen.blit(colkey_text, (Map.width + 440, 210))
        screen.blit(chunk_text, (Map.width + 440, 320))
        screen.blit(selected_x_chunk_text, (Map.width + 400, 360))
        screen.blit(selected_y_chunk_text, (Map.width + 400, 390))

        pygame.display.update() # update display
        clock.tick(60) # maintain 60 fps

test()