import pygame
from sys import exit
from random import randint

BIRD = pygame.image.load('resources/FlappyBirdResized.png')
PIPE = pygame.image.load('resources/Pipe.png')
SKY_SURFACE = pygame.image.load('resources/Sky.png')
GROUND_SURFACE = pygame.image.load('resources/ground.png')

FONT = 'resources/PixelType.ttf'
FPS = 60


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
        self.gravity += 0.2
        self.rect.y += self.gravity

    def update(self):
        self.player_input()
        self.apply_gravity()
        if self.rect.y >= 357 or self.rect.y < -2:
            self.rect.y = 200
            self.gravity = 0


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


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False) or pygame.sprite.spritecollide(player.sprite, border_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()
test_font = pygame.font.Font(FONT, 50)
game_active = False
start_time = 0
score = 0
# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

border_group = pygame.sprite.Group()
border_group.add(Borders('down'))
border_group.add(Borders('up'))

sky_surface = pygame.transform.scale(SKY_SURFACE.convert(), (800, 380))
ground_surface = GROUND_SURFACE.convert()

# Intro screen
player_stand = pygame.transform.rotozoom(BIRD, 0, 0.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('FlappyBird', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press enter to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                x = randint(900, 1100)
                h = randint(40, 240)
                obstacle_group.add(Obstacle('down', x, h))
                obstacle_group.add(Obstacle('up', x, 280-h))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0, 0))

        border_group.draw(screen)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = display_score()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(FPS)
