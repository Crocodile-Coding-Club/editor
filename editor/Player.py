import pygame, sys # import pygame and sys
from pygame.locals import * # import pygame modules

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill((255, 0, 0))  # rouge = joueur

    def move(self, keys, map_engine, camera, chunk_coords, solid_tiles):
        print(self.x)
        dx, dy = 0, 0
        if keys[pygame.K_z]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_q]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
            
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            dx = dx * 2
            dy = dy * 2
        
        # Collision: tester déplacement sur X
        future_rect = pygame.Rect(self.x + dx, self.y, 16, 16)
        if not any(future_rect.colliderect(tile.get_rect()) for tile in solid_tiles):
            self.x += dx

        # Collision: tester déplacement sur Y
        future_rect = pygame.Rect(self.x, self.y + dy, 16, 16)
        if not any(future_rect.colliderect(tile.get_rect()) for tile in solid_tiles):
            self.y += dy
            
        # Gestion des bords et changement de chunk uniquement si le chunk existe
        if self.x < 0:
            if map_engine.getChunk(chunk_coords[0] - 1, chunk_coords[1]):
                self.x = 320 - 1
                chunk_coords[0] -= 1
            else:
                self.x = 0
        elif self.x + 15 >= 320 and camera.x == 0:
            self.x = 320 - 16
        elif self.x >= 320:
            if map_engine.getChunk(chunk_coords[0] + 1, chunk_coords[1]):
                self.x = 0
                chunk_coords[0] += 1
            else:
                self.x = 320 - 1

        if self.y < 0:
            if map_engine.getChunk(chunk_coords[0], chunk_coords[1] - 1):
                self.y = 320 - 1
                chunk_coords[1] -= 1
            else:
                self.y = 0
        elif self.y + 15 >= 320 and camera.y == 0:
            self.y = 320 - 16
        elif self.y >= 320:
            if map_engine.getChunk(chunk_coords[0], chunk_coords[1] + 1):
                self.y = 0
                chunk_coords[1] += 1
            else:
                self.y = 320 - 1
        
        print(camera.x)

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
        
    def draw_with_camera(self, surface, camera):
        draw_rect = camera.apply(pygame.Rect(self.x, self.y, 16, 16))
        surface.blit(self.sprite, draw_rect)