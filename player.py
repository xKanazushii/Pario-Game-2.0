from settings import *
from timerr import Timer

from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('C:/Users/User/Desktop/Pario Game/graphics/player/idle/player.png'))

        # rect
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-76, -36)
        self.hitbox_rect = self.hitbox
        self.old_rect = self.hitbox_rect.copy()

        # movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 600

        # collision
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False,'left': False, 'right': False}

        # timerr
        self.timer = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if not self.timer['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_a]:
                input_vector.x -= 1
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jump = True
            

    def move(self, dt):

        # horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        # vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timer['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.hitbox_rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        self.collision('vertical')
        
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timer['wall slide block'].activate()
                self.hitbox_rect.bottom += -1
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timer['wall slide block'].active:
                self.timer['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        self.rect.center = self.hitbox_rect.center

    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft,(self.hitbox_rect.width,2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0,self.hitbox_rect.height / 4),(2,self.hitbox_rect.height / 2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2,self.hitbox_rect.height / 4), (2,self.hitbox_rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # collision
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
    
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # left
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    
                    # right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left

                else: # vertical
                    # top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom


                    # bottom
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def update_timers(self):
        for timer in self.timer.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()