import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "sea.jpg"))
background_rect = background.get_rect()
L_player_img = pygame.image.load(path.join(img_dir, "player.png"))
R_player_img = pygame.transform.flip(L_player_img, True, False)
lives_img = pygame.transform.scale(L_player_img, (40, 29))
lives_img.set_colorkey(BLACK)
fish_images = []
for i in range(7):
    img = pygame.image.load(path.join(img_dir, "fish" + str(i+1) + ".png"))
    fish_images.append(img)
for i in range(3):
    img = pygame.image.load(path.join(img_dir, "fish1.png"))
    fish_images.append(img)

all_sprites = pygame.sprite.Group()
fishes = pygame.sprite.Group()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newfish():
    f = Fish()
    all_sprites.add(f)
    fishes.add(f)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(L_player_img, (30, 22))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.facing = 'left'
        self.rect.centerx = WIDTH / 2
        self.rect.centery= HEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.lives = 3

    def update(self):
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT / 2

        self.speedx = 0
        self.speedy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -6
            self.image = pygame.transform.scale(L_player_img, (self.rect.width, self.rect.height))
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.speedx = 6
            self.image = pygame.transform.scale(R_player_img, (self.rect.width, self.rect.height))
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.speedy = -6
        if keys[pygame.K_DOWN]:
            self.speedy = 6

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right > (WIDTH + self.rect.width / 2):
            self.rect.right = WIDTH + self.rect.width / 2
        if self.rect.x < -self.rect.width / 2:
            self.rect.x = -self.rect.width / 2
        if self.rect.y < -self.rect.height / 2:
            self.rect.y = -self.rect.height / 2
        if self.rect.bottom > (HEIGHT + self.rect.height / 2):
            self.rect.bottom = HEIGHT + self.rect.height / 2
    
    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(fish_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randrange(HEIGHT - self.rect.height)
        self.speedy = random.randrange(-2, 2)
        self.speedx = random.randrange(-5, 5)

        if self.speedx < 0:
            self.rect.x = random.randrange(WIDTH + 10, WIDTH + 80)
        elif self.speedx > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x = random.randrange(-80, -10)
        else:
            self.speedx = random.randrange(-5, -1)
            self.rect.x = random.randrange(WIDTH, WIDTH + 80)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < -10 or self.rect.top > HEIGHT + 10 or self.rect.right < -10 or self.rect.left > WIDTH + 10:
            self.kill()
            newfish()

def main():
    # initialize pygame and create window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Growing Fish Game")
    clock = pygame.time.Clock()

    # Load all game sounds
    eating_sound = pygame.mixer.Sound(path.join(snd_dir, 'eating sound.mp3'))
    player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'game over.mp3'))
    pygame.mixer.music.load(path.join(snd_dir, 'Calimba - E\'s Jammy Jams.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    def show_go_screen():
        screen.blit(background, background_rect)
        draw_text(screen, "Growing Fish!", 64, WIDTH / 2, HEIGHT / 4, (4, 82, 154))
        draw_text(screen, "Arrow keys to move", 22,
                WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    # Game loop
    game_over = True
    running = True
    while running:
        if game_over:
            show_go_screen()
            game_over = False
            player = Player()
            all_sprites.add(player)
            for i in range(8):
                newfish()
            score = 0

        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()

        # check if the player has collided with any fishes
        hits = pygame.sprite.spritecollide(player, fishes, True, pygame.sprite.collide_rect_ratio(0.8))
        for hit in hits:
            if player.rect.width > hit.rect.width:
                eating_sound.play()
                player.rect.width += 5
                player.rect.height += 5
                score += 50
                newfish()
            else:
                player_die_sound.play()
                player.hide()
                player.lives -= 1

        # if the player died
        if player.lives == 0:
            player.kill()
            for fish in fishes:
                fish.kill()
            game_over = True

        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH / 2, 10, (4, 82, 154))
        draw_lives(screen, WIDTH - 140, 8, player.lives, lives_img)
        # *after* drawing everything, flip the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()