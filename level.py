from settings import *
from sprites import Sprite , MovingSprite
from player import Player
from groups import AllSpriters

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSpriters()
        self.collision_sprites = pygame.sprite.Group()


        self.setup(tmx_map)

    def setup (self, tmx_map):
        # tiles
        for layer in ['bg', 'Terrain']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain' : groups.append(self.collision_sprites)
                

                Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups)

        # object
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

        #  moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'helicopter':
                if obj.width > obj.height: # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width,obj.y + obj.height / 2)
                else: # vartical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width,obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(self.all_sprites, start_pos, end_pos, move_dir, speed)


    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)