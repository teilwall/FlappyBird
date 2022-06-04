import pygame

BIRD = pygame.image.load('resources/FlappyBirdResized.png')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = BIRD.convert_alpha()
        self.image = pygame.transform.rotozoom(player_image, 0, 0.12)
        self.rect = self.image.get_rect(midbottom=(80, 250))
        self.gravity = 0

        # self.jump_sound = pygame.mixer.Sound('sounds/wing.wav')
        # self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -2.2
            # self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.25
        self.rect.y += self.gravity

    def update(self):
        self.player_input()
        self.apply_gravity()
        if self.rect.y >= 357 or self.rect.y < -2:
            self.rect.y = 200
            self.gravity = 0
