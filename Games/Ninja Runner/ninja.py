import pgzrun
from pgzhelper import *

WIDTH=800
HEIGHT=600

runner = Actor('run__000')
run_images = ['run__000', 'run__001', 'run__002', 'run__003', 'run__004', 'run__005', 'run__006', 'run__007', 'run__008', 'run__009']
runner.images = run_images
runner.x = 100
runner.y = 400

velocity_y = 0
gravity = 1

obstacles = []
obstacles_timeout = 0

score = 0
game_over = False

def update():
  global velocity_y, obstacles_timeout, score, game_over
  runner.next_image()

  obstacles_timeout += 1
  if obstacles_timeout > 50:
    actor = Actor('cactus')
    actor.x = 850
    actor.y = 430
    obstacles.append(actor)
    obstacles_timeout = 0

  for actor in obstacles:
    actor.x -= 8
    if actor.x < -50:
      obstacles.remove(actor)
      score += 1

  if keyboard.up:
    velocity_y = -15

  runner.y += velocity_y
  velocity_y += gravity
  if runner.y > 400:
    velocity_y = 0
    runner.y = 400

  if runner.collidelist(obstacles) != -1:
    game_over = True

def draw():
  screen.draw.filled_rect(Rect(0,0,800,400), (163, 232, 254))
  screen.draw.filled_rect(Rect(0,400,800,200), (88, 242, 152))
  if game_over:
    screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    screen.draw.text('Score: ' + str(score), centerx=400, centery=330, color=(255,255,255), fontsize=60)
  else:
    runner.draw()
    for actor in obstacles:
      actor.draw()
    screen.draw.text('Score: ' + str(score), (15,10), color=(0,0,0), fontsize=30)

pgzrun.go() # Must be last line