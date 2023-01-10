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
```
When player press arrow keys, the sprite moves and changes its facing direction and scale according to the key. ‘self.speedx = 0 / self.speedy=0’ makes the character stop when keys are UP.
```python
        if self.rect.right > (WIDTH + self.rect.width / 2):
            self.rect.right = WIDTH + self.rect.width / 2
        if self.rect.x < -self.rect.width / 2:
            self.rect.x = -self.rect.width / 2
        if self.rect.y < -self.rect.height / 2:
            self.rect.y = -self.rect.height / 2
        if self.rect.bottom > (HEIGHT + self.rect.height / 2):
            self.rect.bottom = HEIGHT + self.rect.height / 2
```
It allows the player to stay inside the game window. (add)I changed the code so half of the player sprite could go offscreen. This is because there was a problem that there was not enough space to avoid other fish when the size of the player sprite increased.

## Enemy Sprites
```python
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
```
First, a random value between -5 and 5 was received as speedx, and if the value was negative number(moving from right to left), the sprite would appear on the right side facing left, and if the value was positive number(moving from left to right), it would appear on the left side facing right. The enemy fishes should not pop out of the middle of the screen, so I set the coordinates should be outside offscreen.
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
```python
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
```
I made collision detection by AABB(collide_rect) because the fishes are almost rectangle shaped. If player collide with smaller fish, the eating sound plays, grows up and gets 50 scores. If player collide with bigger fish, the die sound plays, gets invisible  and loses a live point.
