import pygame
import math 
import random
import time

pygame.init()
clock = pygame.time.Clock()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shadow Warrior")
#its like that because this reduses lag a lot and help for better gameplay
def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha(screen)
#Models:
logo = loadify("Project/textures/logo.png")
pygame.display.set_icon(logo)
wallModel = loadify("Project/textures/wall.png")
groundModel = loadify("Project/textures/ground.png")
weaponModel = loadify("Project/textures/weapon.png")
enemyBullet = loadify("Project/textures/bullet.png")
playerBullet = loadify("Project/textures/enemyBullet.png")
crosshair = loadify("Project/textures/crosshair.png")

playerWalkAnimR = [loadify("Project/textures\walk0.png"),
loadify("Project/textures\walk1.png"),
loadify("Project/textures\walk2.png")]
playerWalkAnimL = [loadify("Project/textures\walk3.png"),
loadify("Project/textures\walk4.png"),
loadify("Project/textures\walk5.png")]


pygame.mouse.set_visible(False)
tileSize = 64
level = 0

hitParticles = []
weapons = []
removed_bullets = []    
enemies = []
backgrounds = []
walls = []
all_bullets = []

# Classes
class Particle:

    def __init__(self, x, y, velocityX, velocityY, radius, color):
        self.x = x
        self.y = y
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.radius = radius
        self.color = color
        self.lifetime = random.randrange(50, 100)

    def draw(self, screen, camx, camy):
        self.lifetime -= 1
        self.x += self.velocityX
        self.y += self.velocityY
        pygame.draw.circle(screen, self.color, (self.x - camx, self.y - camy), self.radius)

class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, camx, camy):
        screen.blit(groundModel, (self.x - camx - tileSize / 2, self.y - camy - tileSize / 2))

class Wall:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    #Check if wall collides with smth
    def collidesWith(self, other):
        return pygame.Rect(self.x, self.y, tileSize, tileSize).colliderect(other.x, other.y, tileSize-16, tileSize)
    def draw(self, camx, camy):
        screen.blit(wallModel, (self.x - camx - tileSize / 2, self.y - camy - tileSize / 2))
class Bullet:
    def __init__(self, x, y, velx, vely, isPlayer):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.isPlayer = isPlayer
    def collidesWith(self, other):
        return pygame.Rect(self.x, self.y, tileSize - 16, tileSize - 16).colliderect(other.x, other.y, tileSize-36, tileSize-36)
    def update(self):
        self.x += self.velx
        self.y += self.vely
        for wall in walls:
            if bullet.collidesWith(wall):
                removed_bullets.append(bullet)
        for i in removed_bullets:
            if i in all_bullets:
                all_bullets.remove(i)
        
    def draw(self, camx, camy):
        if (self.isPlayer):
            screen.blit(pygame.transform.smoothscale(playerBullet, (16, 16)), (self.x - camx + 5, self.y - camy + 7))
        else: screen.blit(pygame.transform.smoothscale(enemyBullet, (16, 16)), (self.x - camx + 5, self.y - camy + 7))    
class slimeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bulletSpeed = 1
        self.aliveAnimations = [loadify("Project/textures\slime_animation_0.png"),
        loadify("Project/textures\slime_animation_1.png"),
        loadify("Project/textures\slime_animation_2.png"),
        loadify("Project/textures\slime_animation_3.png"),]
        self.animationsCount = 0
        self.attackRate = 60
        self.resetOffset = 0
        self.SlimeHp = 7 + level * 2
        self.slimeCollisionDmg = 1 + level/2
        self.dmg = 1 + level / 2
        self.isAlive = True
        
        #adding offset so the enemy doesnt move directly towards the player
        self.offsetX = random.randrange(-150, 150)
        self.offsetY = random.randrange(-150, 150)
    def collidesWithAnything(self):
        for wall in walls:
            if wall.collidesWith(self):
                return True
        return False
    def healthBar(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.x - camx - 20, self.y + 40 - camy, self.SlimeHp*10 + level*2, 7))
    def collidesWith(self, other):
        return pygame.Rect(self.x, self.y, tileSize-36, tileSize-36).colliderect(other.x, other.y, tileSize-36, tileSize-36)
    
    def update(self):
        # move enemy accordingly
        if self.resetOffset == 0:
            self.offsetX = random.randrange(-400, 400)
            self.offsetY = random.randrange(-400, 400)
            self.resetOffset = random.randrange(120, 150)
        else: self.resetOffset -= 1

        if player.x + self.offsetX > self.x:
            self.x += 1
            if self.collidesWithAnything():
                self.x -= 1
            
        elif player.x + self.offsetX < self.x:
            self.x -= 1
            if self.collidesWithAnything():
                self.x += 1
            
        if player.y + self.offsetY > self.y:
            self.y += 1
            if self.collidesWithAnything():
                self.y -= 1
            
        elif player.y + self.offsetY < self.y:
            self.y -= 1
            if self.collidesWithAnything():
                self.y += 1
        self.healthBar()
    
    def attack(self):
        for i in range(random.randint(3, 5)):
            angle = random.randrange(0, 360)
            bulletSpeed_x = self.bulletSpeed * math.cos(angle) + random.uniform(-5, 5) + level/10
            bulletSpeed_y = self.bulletSpeed * math.sin(angle) + random.uniform(-5, 5) + level/10
            all_bullets.append(Bullet(self.x, self.y, bulletSpeed_x, bulletSpeed_y, False))
            
    def drawAlive(self, camx, camy):
        if self.animationsCount + 1 == 32:
            self.animationsCount = 0 
        self.animationsCount += 1 
        if self.attackRate == 0:
            self.attackRate = 60
            self.attack()
        self.attackRate -= 1
        screen.blit(pygame.transform.scale(self.aliveAnimations[self.animationsCount// 8], (32, 30)), (self.x - camx, self.y - camy))

class Weapon:
    def __init__(self, bulletSpeed, fireRate, bulletDmg):
        self.shooting = False
        self.bulletSpeed = bulletSpeed
        self.fireRate = fireRate
        self.bulletDmg = bulletDmg
        self.energy = 150
        self.i = 0

    def handle_weapons(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - width/2, mouse_y - height/2
        angle = (180/math.pi) * - math.atan2(rel_y, rel_x) 
        #draw crosshair
        screen.blit(crosshair, (mouse_x, mouse_y+5))
        #rotate and draw weapon accordingly
        if angle > 90 or angle < -90:
            player_weapon_copy = pygame.transform.rotate(pygame.transform.flip(weaponModel, True, False), angle - 180) 
        else:
            player_weapon_copy = pygame.transform.rotate(weaponModel, angle)
        screen.blit(player_weapon_copy, (width/2 +5 - int(player_weapon_copy.get_width()/2), height/2 + 15 - int(player_weapon_copy.get_height()/2)))
    def Shooting(self):
        if self.shooting:
            #calculates the angles the bullet should travel :/
            if self.i % self.fireRate == 0:
                if (self.energy == 0):
                    pass
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()   
                    distance_x = mouse_x - width/2
                    distance_y = mouse_y - height/2   
                    angle = math.atan2(distance_y, distance_x)    
                    bulletSpeed_x = self.bulletSpeed * math.cos(angle)
                    bulletSpeed_y = self.bulletSpeed * math.sin(angle)
                    all_bullets.append(Bullet(player.x, player.y, bulletSpeed_x, bulletSpeed_y, True))
                    self.energy -= 1
            self.i += 1

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.leftPr = False
        self.rightPr = False
        self.downPr = False
        self.upPr = False
        self.speed = 4
        self.health = 7
        self.maxHp = 7
        self.animationsCount = 0
        
    def healthBar(self):
        pygame.draw.rect(screen, (255, 0, 0), (20, 25, self.maxHp*30, 10))
        pygame.draw.rect(screen, (0, 255, 0), (20, 25, self.health*30 , 10))
    def energyBar(self):
        pygame.draw.rect(screen, (255, 0, 0), (20, 55, 150, 10))
        pygame.draw.rect(screen, (48, 117, 255), (20, 55, weapon.energy, 10))
    def collidesWithAnything(self):
        for wall in walls:
            if wall.collidesWith(self):
                return True
        return False
    def update(self):
        
        if self.leftPr and not self.rightPr:
            self.x -= self.speed
            if self.collidesWithAnything():
                self.x += self.speed
            
        if self.rightPr and not self.leftPr:
            self.x += self.speed
            if self.collidesWithAnything():
                self.x -= self.speed
            
        if self.upPr and not self.downPr:  
            self.y -= self.speed
            if self.collidesWithAnything():
                self.y += self.speed
            # revert if collision
            
        if self.downPr and not self.upPr:
            self.y += self.speed
            if self.collidesWithAnything():
                self.y -= self.speed
        
            
            # check for enemy colisions
    def getRandBuff(self):
        buff = random.randint(1, 5)
        if (buff == 1):
            self.speed += 1
        if (buff == 2):
            self.maxHp += 1
            self.health += 1
        if (buff == 3):
            weapon.bulletDmg += 1
        if (buff == 4):
            weapon.fireRate += 3
        if (buff == 5):
            weapon.bulletSpeed += 1
    def animations(self):
        if self.animationsCount + 1 >= 36:
            self.animationsCount = 0 
        if self.rightPr:
            screen.blit(pygame.transform.scale(playerWalkAnimR[self.animationsCount//12],(64, 64)), (width/2 - 40, height/2 - 30))
        elif self.leftPr:
            screen.blit(pygame.transform.scale(playerWalkAnimL[self.animationsCount//12],(64, 64)), (width/2 - 40, height/2 - 30))
        else: 
            screen.blit(pygame.transform.scale(playerWalkAnimR[0],(64, 64)), (width/2 - 40, height/2 - 30))
        self.animationsCount += 1

weapon = Weapon(10, 20, 2)
player = Player(1, 0)
#Loads map from file
def loadMapFromFile(path):
    walls.clear()
    backgrounds.clear()
    enemies.clear()
    with open(path, "r") as f:
        y = 0
        enemyLocations = []

        for line in f.readlines():
            x = 0
            for char in line:
                if char != ' ' and char != "\n":
                    backgrounds.append(Background(x * tileSize, y * tileSize))
                if char == '#':
                    walls.append(Wall(x * tileSize, y * tileSize))
                elif char == 'p' or char == 'P':
                    player.x = x * tileSize
                    player.y = y * tileSize
                elif char == 'e' or char == 'E':
                    if random.randint(1, 100) <= 40:
                        enemyLocations.append((x * tileSize, y * tileSize))
                x += 1
            y += 1
        for enemyL in enemyLocations:
            enemies.append(slimeEnemy(*enemyL))

def Text(type):
    pygame.font.init()
    fonts = pygame.font.Font('freesansbold.ttf', 32)
    if type == 1:
        text = fonts.render('GAME OVER', True, (255, 0, 0))
    if type == 2:
        text = fonts.render('You Win', True, (255, 0, 0))
    textRect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, textRect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

loadMapFromFile('Project/maps/Map0.txt')
hitCooldown = 40
cooldown = 300
lastLevel = 9
#running loop
gameOver = False
running = True

while running:
    if gameOver:
        Text(1)
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.upPr = True
                if event.key == pygame.K_s:
                    player.downPr = True
                if event.key == pygame.K_d:
                    player.rightPr = True
                if event.key == pygame.K_a:
                    player.leftPr = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.upPr = False
                if event.key == pygame.K_s:
                    player.downPr = False
                if event.key == pygame.K_d:
                    player.rightPr = False
                if event.key == pygame.K_a:
                    player.leftPr = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                weapon.shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                weapon.shooting = False 

        # updating
        
        camx = player.x - width / 2
        camy = player.y - height / 2
        screen.fill((0, 0, 0))
        player.update()
        #check if slime got hit
        for bullet in all_bullets:
            bullet.update()
            
            for enemy in enemies:
                if enemy.collidesWith(player):
                    if hitCooldown < 0:
                        hitCooldown = 40
                        player.health -= enemy.slimeCollisionDmg
                    if player.health <= 0:
                        gameOver = True
                elif enemy.collidesWith(bullet) and bullet.isPlayer:
                    removed_bullets.append(bullet)       
                    for i in range(10):
                        hitParticles.append(Particle(enemy.x, enemy.y, random.randrange(-5, 5)/10, random.randrange(-5, 5)/10, 4, (108, 216, 32)))
                    enemy.SlimeHp -= weapon.bulletDmg
                    if enemy.SlimeHp <= 0:
                        enemy.isAlive = False
                        if player.health >= player.maxHp:
                            player.health = player.maxHp
                        else:
                            player.health += 1
                        if  weapon.energy >= 150:
                            weapon.energy = 150
                        else:
                             weapon.energy += 2
            if bullet.collidesWith(player) and not bullet.isPlayer:
                if hitCooldown < 0:
                    hitCooldown = 40
                    player.health -= enemy.dmg
                if player.health <= 0:
                    gameOver = True
                removed_bullets.append(bullet)
                
        for bg in backgrounds:
            bg.draw(camx, camy)
        for wall in walls:
            wall.draw(camx, camy)
        # update all other entities

        #draw bullet
        for bullet in all_bullets:
            bullet.draw(camx, camy)
        # slime animations and remove dead slimes 
        for enemy in enemies:
            enemy.update()
            if enemy.isAlive:
                enemy.drawAlive(camx, camy) 
            if not enemy.isAlive:
                enemies.remove(enemy)
        # draw particles
        for particle in hitParticles:
            if particle.lifetime > 0:
                particle.draw(screen, camx, camy)
            else:
                hitParticles.pop(hitParticles.index(particle))
        
        player.animations()
        weapon.handle_weapons(screen)
        weapon.Shooting()
        player.healthBar()
        player.energyBar()
        if len(enemies) == 0:
            if cooldown <= 0:
                cooldown = 600
                if level == lastLevel:
                    Text(2)
                    time.sleep(5)
                    break
                loadMapFromFile("Project/maps\Map{0}.txt".format(level+1))
                level+=1
                player.getRandBuff()
                
                if  weapon.energy >= 150:
                    weapon.energy = 150
                else:
                    weapon.energy += 20
            cooldown -= 1   
        hitCooldown -= 1
        # finally update screen
        
        pygame.display.update()
        clock.tick(60)


