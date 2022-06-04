import pygame

PIPE = pygame.image.load('resources/Pipe.png')
GROUND_SURFACE = pygame.image.load('resources/ground.png')


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, x_pos, height):
        super().__init__()
        if type == 'down':
            self.image = pygame.transform.scale(PIPE.convert_alpha(), (40, height))
            self.rect = self.image.get_rect(midbottom=(x_pos, 380))
        elif type == 'up':
            self.pipe = pygame.transform.scale(PIPE.convert_alpha(), (40, height))
            self.image = pygame.transform.rotate(self.pipe, 180)
            self.rect = self.image.get_rect(midtop=(x_pos, 0))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class Borders(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'down':
            self.image = GROUND_SURFACE.convert()
            self.rect = self.image.get_rect(topleft=(0, 380))
        elif type == 'up':
            self.image = PIPE.convert()
            self.rect = self.image.get_rect(bottomleft=(0, 0))
