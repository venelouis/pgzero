import pgzrun
import random
import math
from pgzhelper import *

# Setup screen size
WIDTH = 1100
HEIGHT = 600


# Game Sprite
bullet_pickup_img = 'bullet' 
life_pickup_img = 'life' 
background = Actor('background', (WIDTH/2, HEIGHT/2))
music.play('bg')
music.set_volume(1)

player = Actor('p0', (WIDTH/2, HEIGHT/2))
player.fps = 10
player.angle = 0

# List for multiple units
zombies = []
bullets = []
bullet_pickups = []
love_list = []
life_pickups = []

# Starting Variables
score = 0
life = 5
bullet_holdoff = 0
zombie_timeout = 0
key_condition = 0
bullet_amount = 100
bullet_pickups_timeout = 1
bullet_pickups_timeout_duration = 0
life_pickups_timeout = 1
life_pickups_timeout_duration = 0
draw_love = True
no_key_pressed = True
game_over = True
player.x = WIDTH/2
player.y = HEIGHT/2

def draw():
    background.draw()
    if game_over:
        for love in love_list:
            love_list.remove(love)
        for zombie in zombies:
            zombies.remove(zombie)
        for bullet in bullets:
            bullets.remove(bullet)
        for pickup in bullet_pickups:
            bullet_pickups.remove(pickup)
        for life_pickup in life_pickups:
            life_pickups.remove(life_pickup)
        screen.draw.text('Matando Zumbis', centerx=WIDTH/2, centery=150, color="black", fontsize=80)
        screen.draw.text('Aperte "k" Para Começar o Jogo', centerx=WIDTH/2, centery=270, color="black", fontsize=30)
        screen.draw.text('Score: ' + str(score), centerx=WIDTH/2, centery=450, color="black", fontsize=60)
        screen.draw.text("Sound On/Off", centerx=WIDTH/2, centery=300, color="black", fontsize=30)
        screen.draw.text("Clique no 'x' para sair", centerx=WIDTH/2, centery=330, color="black", fontsize=30)

    else: 
        player.draw()

        for love in love_list:
            love.draw()
        for zombie in zombies:
            zombie.draw()
        for bullet in bullets:
            bullet.draw()
        for pickup in bullet_pickups:
            pickup.draw()
        for life_pickup in life_pickups:
            life_pickup.draw()
        screen.draw.text("Score: " + str(score), (10, 10), color="black")
        screen.draw.text("Life: " + str(life), (10, 30), color="black")
        screen.draw.text("Bullet Amount: " + str(bullet_amount), (10, 50), color="black")


def update():
    global game_over, score, life, key_condition, no_key_pressed, draw_love
    global zombie_timeout
    global bullet_holdoff, bullet_amount, bullet_pickups_timeout, bullet_pickups_timeout_duration
    global life_pickups_timeout, life_pickups_timeout_duration

    if game_over == False:
        if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
            if key_condition == 0:
                player.images = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
                player.fps = 10
            key_condition = 1 
            no_key_pressed = True
        else:
            if no_key_pressed:
                player.fps = 2
                player.images = ['p8', 'p9']
            no_key_pressed = False
            key_condition = 0
            

        if keyboard.left:
            player.x -= 5
            player.angle = 180
            player.flip_y = True
            
        elif keyboard.right:
            player.x += 5
            player.angle = 0
            player.flip_y = False

        elif keyboard.up:
            player.y -= 5
            if player.angle == 180:
                player.flip_y = True
            elif player.angle == 0:
                player.flip_y = False   

        elif keyboard.down:
            player.y += 5
            if player.angle == 180:
                player.flip_y = True
            elif player.angle == 0:
                player.flip_y = False   
        else:
            if player.angle == 180:
                player.flip_y = True
            elif player.angle == 0:
                player.flip_y = False        


        player.animate()
            

        # Update bullets
        if bullet_holdoff == 0 and bullet_amount > 0:
            if keyboard.space:
                sounds.bullet.set_volume(0.2)
                sounds.bullet.play()
                bullet = Actor('bullet')
                bullet.scale = 0.05
                if player.angle == 180:
                    bullet.angle = player.angle 
                    bullet.x = player.x - 30
                elif player.angle == 0:
                    bullet.angle = player.angle
                    bullet.x = player.x + 30           
                bullet.y = player.y + 10
                bullets.append(bullet)
                bullet_holdoff = 30
                bullet_amount -= 1

        elif bullet_holdoff > 0:
            bullet_holdoff -= 1

        for bullet in bullets:
            if bullet.angle == 0:
                bullet.x = bullet.x + 20
            elif bullet.angle == 180:
                bullet.x = bullet.x - 20
            
            # Check for collision with zombies
            for zombie in zombies:
                if bullet.colliderect(zombie):
                    zombie.life -= 1
                    bullets.remove(bullet)  # Remove the bullet
                    if zombie.life <= 0:
                        zombies.remove(zombie)  # Remove the zombie
                    score += 1
                    break  # Exit the loop after removing the zombie to avoid errors

        # Spawn zombies
        zombie_timeout += 1
        if zombie_timeout > 100:
            zombie = Actor('z0')
            zombie.images = ['z0','z1','z2','z3','z4','z5','z6','z7']
            zombie.y = random.randint(0, HEIGHT)
            zombie.x_random = random.randint(0, 1)
            if zombie.x_random == 0:
                zombie.x = 0
            elif zombie.x_random == 1:
                zombie.x = WIDTH
            zombie.type = random.randint(0, 1)
            if zombie.type == 0:
                zombie.life = 3
            elif zombie.type == 1:
                zombie.life = 1
            zombie.fps = 5
            zombies.append(zombie)
            zombie_timeout = 0
        
        # Update zombie positions
        for zombie in zombies:
            if zombie.type == 0:
                zombie.scale = 0.4
            elif zombie.type == 1:
                zombie.scale = 0.3
            zombie.animate()
            if zombie.x_random == 0:
                zombie.flip_x = False
            if zombie.x_random == 1:
                zombie.flip_x = True
            angle = math.atan2(player.y - zombie.y, player.x - zombie.x)
            speed = 1
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            zombie.x += dx
            zombie.y += dy

        # Check for collision with player
        for zombie in zombies:
            if player.colliderect(zombie):
                life -= 1
                draw_love = True
                zombies.remove(zombie)
                if life <= 0:
                    game_over = True

        # Update bullet pickups
        if bullet_pickups_timeout == 0:
            bullet_pickups_timeout_duration += 1
        elif bullet_pickups_timeout_duration == 0:
            bullet_pickups_timeout += 1
        
        for pickup in bullet_pickups:

            # Pick up and add bullets
            if player.colliderect(pickup):
                bullet_amount += 10
                bullet_pickups.remove(pickup)     

        # Remove the oldest bullet pickup if any exist
        if bullet_pickups_timeout_duration > 400:
            if bullet_pickups:
                bullet_pickups.pop(0)  
            
            bullet_pickups_timeout_duration = 0  
            bullet_pickups_timeout = 1   

        # Spawn bullet pickups
        if bullet_pickups_timeout > 300:
            bullet_pickup = Actor(bullet_pickup_img)
            bullet_pickup.scale = 0.1
            bullet_pickup.x = random.randint(0, WIDTH)
            bullet_pickup.y = random.randint(0, HEIGHT)
            bullet_pickups.append(bullet_pickup)
            bullet_pickups_timeout = 0


        if life_pickups_timeout == 0:
            life_pickups_timeout_duration += 1
        elif life_pickups_timeout_duration == 0:
            life_pickups_timeout += 1
        
        for life_pickup in life_pickups:

            # Pick up and add life
            if player.colliderect(life_pickup):
                if life < 5:
                    life += 1
                    draw_love = True
                life_pickups.remove(life_pickup)     

        # Remove the oldest life pickup if any exist
        if life_pickups_timeout_duration > 400:
            if life_pickups:
                life_pickups.pop(0)  
            life_pickups_timeout_duration = 0  
            life_pickups_timeout = 1 


        # Spawn life pickups
        if life_pickups_timeout > 300:
            life_pickup = Actor(life_pickup_img)
            life_pickup.scale = 0.1
            life_pickup.x = random.randint(0, WIDTH)
            life_pickup.y = random.randint(0, HEIGHT)
            life_pickups.append(life_pickup)
            life_pickups_timeout = 0

        # Draw life program
        if draw_love == True:
            for love in love_list:
                love_list.remove(love)
            if life > 1:
                for i in range(life):
                    love = Actor('life')
                    love.x = 1100 - 50*i
                    love.y = 50
                    love.scale = 0.1
                    love_list.append(love)
            draw_love = False
    else:
        if keyboard.k:
            # Starting Variables
            score = 0
            life = 5
            bullet_holdoff = 0
            zombie_timeout = 0
            key_condition = 0
            bullet_amount = 100
            bullet_pickups_timeout = 1
            bullet_pickups_timeout_duration = 0
            life_pickups_timeout = 1
            life_pickups_timeout_duration = 0
            draw_love = True
            no_key_pressed = True
            game_over = False
            player.x = WIDTH/2
            player.y = HEIGHT/2



pgzrun.go()
