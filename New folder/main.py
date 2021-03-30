import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()


screen = pygame.display.set_mode((800, 600)) #set window screen
pygame.display.set_caption("Alien invasion by Ujjwol") #set caption

#background music
mixer.music.load("background.mp3")
mixer.music.play(-1)


icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

score = 0
lives = 0

# player
playerimg = pygame.image.load("space-invaders.png")
playerimg = pygame.transform.scale(playerimg, (70, 70))
playerX = 380
playerY = 510
playerx_change = 0


# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10


for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy2.png"))
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(0,20))
    enemyX_change.append(0.7)
    enemyY_change.append(0)


#bullets
bulletimg = pygame.image.load("pixel_laser_red.png")
bulletimg = pygame.transform.scale(bulletimg, (60, 60))
bulletX = 0
bulletY = 510
bulletX_change = 0
bulletY_change = 0.7
bullet_state = "ready"

font = pygame.font.Font('freesansbold.ttf', 20)


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+6, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + (math.pow(enemyY-bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


def scoreboard():

    text = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 5))


# def testing_gameover(enemyX, enemyY, playerX, playerY):
#     gameover = math.sqrt(math.pow(enemyX-playerX,2) + (math.pow(enemyY-playerY,2)))
#     if gameover:
#         return True
#     else:
#         False

# def gameOver_score():
#     game = font.render('Lives : ' + str(score), True, (255, 255, 255))
#     screen.blit(game, (750, 5))

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.9
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)           

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

       
    playerX += playerx_change

    # adding boundries to playerX
    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 730
    

    for i in range(num_of_enemies):
        # gameover_text = testing_gameover(enemyX[i], enemyY[i], playerX, playerY)
        # if gameover_text:
        #     lives += 1
        #     if lives == 3:
        #         running = False
        enemyX[i] += enemyX_change[i]
        # enemy movement
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += 50
        elif enemyX[i] >= 730:
            enemyX_change[i] = -0.5
            enemyY[i] += 50

        enemy(enemyX[i], enemyY[i], i)

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletX = playerX
            bulletY = 510
            bullet_state = "ready"
            enemyX[i] = random.randint(0,730)
            enemyY[i] = random.randint(0,20)
            score += 1
        


    # bullet movement
    if bulletY <= 0:
        bulletY = 510
        bullet_state = "ready"
    if bullet_state == "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    
    scoreboard()
    player(playerX, playerY)
    enemy(enemyX[i], enemyY[i], i)
    pygame.display.update()

