# Project4
Growing Fish Game

## How to Play
The player controls a small fish by arrow keys to move up, down, left, and right eating smaller fishes and avoiding larger fishes. If player collide with a smaller fish, the player character gets bigger, and if player collide with a bigger fish, it  loses a life point. Three life points are given, and the game ends when player loses it all.

## Player Sprite and Control
1-1. Player initialize
```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size_W = 30
        self.size_H = 22
        self.image = pygame.transform.scale(L_player_img, (self.size_W, self.size_W))
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
```
I’ve chosen a size of 30x22 for player and set the transparent color as BLACK using set_colorkey to remove black rectangle around the image. And I located it at the center of the game window. Facing variable is to flip player character according to the x direction and speedx and speedy is to make it move. Hiding properties is to make player invisible for seconds when player loses a life point.

1-2. Movement and control
```python
def update(self):
    if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
        self.hidden = False
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
```
It makes player reappear one second after death.
```python
    self.speedx = 0
    self.speedy = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        self.speedx = -6
        if self.facing == 'right':
            self.image = pygame.transform.scale(L_player_img, (self.size_W, self.size_H))
        self.facing = 'left'
    if keys[pygame.K_RIGHT]:
        self.speedx = 6
        if self.facing == 'left':
            self.image = pygame.transform.scale(R_player_img, (self.size_W, self.size_H))
        self.facing = 'right'
    if keys[pygame.K_UP]:
        self.speedy = -6
    if keys[pygame.K_DOWN]:
        self.speedy = 6
```
When player press arrow keys, the character moves according to the key. ‘self.speedx = 0 / self.speedy=0’ makes the character stop when keys are UP.
```python
    self.rect.x += self.speedx
    self.rect.y += self.speedy

    if (self.rect.x + self.size_W) > WIDTH:
        self.rect.x = WIDTH - self.size_W
    if self.rect.x < 0:
        self.rect.x = 0
    if self.rect.y < 0:
        self.rect.y = 0
    if (self.rect.y + self.size_H) > HEIGHT:
        self.rect.y = HEIGHT - self.size_H
```
It allows the player to stay inside the game window.

## Enemy Sprites
```python
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(fish_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 80)
        self.rect.bottom = random.randrange(HEIGHT - self.rect.height)
        self.speedy = random.randrange(-2, 2)
        self.speedx = random.randrange(-5, -1)
        self.last_update = pygame.time.get_ticks()
```
The enemy fishes should not pop out of the middle of the screen. Therefore, I set randrange from window width to width+80, so fishes can appear from outside of the game window.
```python
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
```
I wanted fished to move by x direction mainly, so set the speedx larger than speedy. 
```python
        if self.rect.bottom < -10 or self.rect.top > HEIGHT + 10 or self.rect.right < -10 or self.rect.left > WIDTH + 10:
            self.kill()
            newfish()
```
If the fish goes offscreen, I just delete it and respawn new fish.

## Collision
I made collision detection by AABB(collide_rect) because the fishes are almost rectangle shaped.  If player collide with smaller fish, the eating sound plays, grows up and gets 50 scores. If player collide with bigger fish, the die sound plays, gets invisible  and loses a live point.
