import pygame, sys # import pygame and sys
from pygame.locals import * # import pygame modules

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target, engine, current_chunk):
        CHUNK_SIZE_IN_TILES = 16
        TILE_SIZE = 20
        chunk_w = CHUNK_SIZE_IN_TILES * TILE_SIZE
        chunk_h = CHUNK_SIZE_IN_TILES * TILE_SIZE

        cx, cy = current_chunk

        chunk_origin_x = cx * chunk_w
        chunk_origin_y = cy * chunk_h

        cam_x = target.x - self.width // 2
        cam_y = target.y - self.height // 2
        
        # Bord gauche
        if engine.getChunk(cx - 1, cy) is None and target.x < chunk_origin_x + self.width // 2:
            cam_x = 0
        # Bord droit
        if engine.getChunk(cx + 1, cy) is None and target.x > 160:
            cam_x = 0
        # Bord haut
        if engine.getChunk(cx, cy - 1) is None and target.y < chunk_origin_y + self.height // 2:
            cam_y = 0
        # Bord bas
        if engine.getChunk(cx, cy + 1) is None and target.y > 160:
            cam_y = 0
            
        self.x = cam_x
        self.y = cam_y

    def apply(self, obj_rect):
        return obj_rect.move(-self.x, -self.y)