import pygame
import math
import random
from pygame import mixer


pygame.init()
WIDTH = 800
HEIGHT = 600
COLOR = (255,255,255)
# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)
x_coordinate = 200
y_coordinate = 236
def game_over_text(x,y):
    text = over_font.render("GAME OVER!!!",True,(0,0,0))
    screen.blit(text, (x,y))



# Background Image
Background_Image = pygame.image.load("Background_Img.jpg")
def background(x,y):
    screen.blit(Background_Image, (x,y))

# Player
player_Img = pygame.image.load("Player_Img.png")
player_x = 360
player_y = 500
player_x_change = 0


enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

# Multiple Enemies
num_of_enemies = 4

# Enemy
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("monster.png"))
    enemy_x.append(random.randint(0,740))
    enemy_y.append(random.randint(0,50))
    enemy_x_change.append(0.5)
    enemy_y_change.append(10)

# Bullet
bullet_Img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 2
bullet_state = "ready"

# Collision

def is_collision(Enemy_X, Enemy_Y, Bullet_X, Bullet_Y):
    distance = math.sqrt(math.pow(Enemy_X-Bullet_X,2) + math.pow(Enemy_Y- Bullet_Y,2))
    if distance < 20:
        return True
    return False



def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_Img,(x + 15,y-10))

font = pygame.font.Font("freesansbold.ttf", 40)
text_x = 10
text_y = 10
score_value = 0
def show_font(x,y):
    score = font.render("Score Value: " + str(score_value),True, (0,0,255))
    screen.blit(score, (x,y))

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders Game".upper())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change= -1
            elif event.key == pygame.K_RIGHT:
                player_x_change = 1
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    Bullet_Sound = mixer.Sound("laser.wav")
                    Bullet_Sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    screen.fill(COLOR)
    background(0,0)
    screen.blit(player_Img,(player_x,player_y))

    player_x += player_x_change

    if player_x > 740:
        player_x = 740

    elif player_x < 0:
        player_x = 0
    for i in range(num_of_enemies):
        if enemy_x[i] > 740:
            enemy_x_change[i]= -0.5
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] < 0:
            enemy_x_change[i] = 0.5
            enemy_y[i] += enemy_y_change[i]

        if enemy_y[i] > 450:
            for j in range(num_of_enemies):
                enemy_y[j] = 1000
            game_over_text(x_coordinate,y_coordinate)
            break






        collision = is_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            enemy_x[i] = random.randint(0, 740)
            enemy_y[i] = random.randint(0, 50)
            bullet_y = 500
            bullet_state = "ready"
            score_value += 1
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
        screen.blit(enemy_img[i], (enemy_x[i], enemy_y[i]))
        enemy_x[i] += enemy_x_change[i]


    if bullet_state == "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

    if bullet_y < 0:
        bullet_y = 500
        bullet_state = "ready"
    show_font(text_x, text_y)
    pygame.display.update()
pygame.quit()
