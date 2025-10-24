import pgzero
import math
from pygame import Rect 

class Player:
    def __init__(self, pos=(0, -50)):
        self.actor = Actor('player_sprite', pos=pos)
        self.vy = 0
        self.on_ground = False
        self.facing_right = True
        self.is_jumping = False
        self.animation_time = 0
        self.current_frame = 0
    
    def update_animation(self, state, ANIMATION_SPEED):
        self.animation_time += ANIMATION_SPEED
        
        if state == 'idle':
            frames = ['player_idle_right', 'player_idle_right2'] if self.facing_right else ['player_idle_left', 'player_idle_left2']
        elif state == 'walk':
            frames = ['player_walk_right1', 'player_walk_right2'] if self.facing_right else ['player_walk_left1', 'player_walk_left2']
        elif state == 'jump':
            frames = ['player_jump_right'] if self.facing_right else ['player_jump_left']

        if self.current_frame >= len(frames):
            self.current_frame = 0

        if self.animation_time >= 1:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
        
        self.actor.image = frames[self.current_frame]

class Enemy:
    def __init__(self, pos):
        self.actor = Actor('enemy', pos=pos)
        self.direction = -1
        self.start_x = pos[0]
        self.patrol_distance = 50
        self.animation_time = 0
        self.current_frame = 0
    
    def update_animation(self, ENEMY_ANIMATION_SPEED):
        self.animation_time += ENEMY_ANIMATION_SPEED
        
        if self.direction == 1:
            frames = ['enemy_walk_right1', 'enemy_walk_right2']
        else:
            frames = ['enemy_walk_left1', 'enemy_walk_left2']

        if self.animation_time >= 1:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
        
        self.actor.image = frames[self.current_frame]

class Brother:
    def __init__(self, pos):
        self.actor = Actor('brother_idle', pos=pos)
        self.animation_time = 0
        self.current_frame = 0
    
    def update_animation(self, BROTHER_ANIMATION_SPEED):
        self.animation_time += BROTHER_ANIMATION_SPEED
        frames = ['brother_idle', 'brother_idle2']

        if self.animation_time >= 1:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
        
        self.actor.image = frames[self.current_frame]

GAME_ACTIVE = False
GAME_WON = False
WIDTH = 900
HEIGHT = 500
GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5
ANIMATION_SPEED = 0.1
ENEMY_ANIMATION_SPEED = 0.03
BROTHER_ANIMATION_SPEED = 0.03
PLATFORM_IMAGE = 'platform'
ENEMY_SPEED = 1
FLOOR_COLOR = (100, 50, 0)  
BROTHER_POS = (450, HEIGHT - 80)
RESTART_BUTTON_POS = Rect((WIDTH/2 - 100, HEIGHT/2 + 100), (200, 50))


BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
START_COLOR = (50, 168, 82)    
START_HOVER = (60, 198, 97)    
EXIT_COLOR = (168, 50, 50)     
EXIT_HOVER = (198, 60, 60)     
MUSIC_COLOR = (238, 132, 0)    
MUSIC_HOVER = (255, 165, 0)  
INITIAL_ENEMIES = [
    {'pos': (370, HEIGHT-190)},
    {'pos': (670, HEIGHT-290)}
]

player = Player((0, HEIGHT-50))
brother = Brother(BROTHER_POS)

last_start_hover = False
last_exit_hover = False
last_music_hover = False
start_hover = False
exit_hover = False
restart_hover = False
last_restart_hover = False

MUSIC_BUTTON_RADIUS = 25
music_playing = True
music_hover = False
music_button_pos = (WIDTH - 40, 40)

start_button_pos = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - 60), (BUTTON_WIDTH, BUTTON_HEIGHT))
exit_button_pos = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 + 20), (BUTTON_WIDTH, BUTTON_HEIGHT))

platforms = [
    Rect((150, HEIGHT-100), (120, 20)),  
    Rect((300, HEIGHT-150), (120, 20)), 
    Rect((450, HEIGHT-200), (120, 20)),  
    Rect((600, HEIGHT-250), (120, 20)), 
    Rect((750, HEIGHT-115), (120, 20)), 
]


def reset_enemies():
    global enemies
    enemies = []
    for enemy_data in INITIAL_ENEMIES:
        enemy = Enemy(enemy_data['pos']) 
        enemies.append(enemy)
    
enemies = []
reset_enemies()

background = 'sample'

def update():
    global GAME_WON
    
    if not music.is_playing('theme'):
        music.play('theme')
        music.set_volume(0.5)

    if GAME_ACTIVE and not GAME_WON:
        
        brother.update_animation(BROTHER_ANIMATION_SPEED)

        if player.actor.colliderect(brother.actor) and not GAME_WON:
            GAME_WON = True
            sounds.win.play()
            
        player.vy += GRAVITY  # Aplica gravidade
        player.actor.y += player.vy 
        
        # Reseta a variável on_ground antes de verificar colisões
        player.on_ground = False
        
        # Verifica colisão com o chão primeiro
        if player.actor.bottom > HEIGHT - 30:
            player.actor.bottom = HEIGHT - 30
            player.vy = 0
            player.on_ground = True
            player.is_jumping = False
            
        # Depois verifica colisão com plataformas
        for platform in platforms:
            if player.actor.colliderect(platform):
                # Verifica colisão vertical primeiro
                if player.vy > 0:  # Caindo
                    if player.actor.bottom > platform.top and player.actor.top < platform.top:
                        player.actor.bottom = platform.top
                        player.vy = 0
                        player.on_ground = True
                        player.is_jumping = False
                        continue  # Pula as verificações laterais se pousar na plataforma
                
                elif player.vy < 0:  # Subindo
                    if player.actor.top < platform.bottom and player.actor.bottom > platform.bottom:
                        player.actor.top = platform.bottom
                        player.vy = 0
                        continue  # Pula as verificações laterais se bater a cabeça
                
                # Só verifica colisões laterais se não houve colisão vertical
                if player.actor.right > platform.left and player.actor.centerx < platform.centerx:
                    player.actor.right = platform.left
                elif player.actor.left < platform.right and player.actor.centerx > platform.centerx:
                    player.actor.left = platform.right

        for enemy in enemies: 
            enemy.actor.x += ENEMY_SPEED * enemy.direction
            enemy.update_animation(ENEMY_ANIMATION_SPEED)           

            if enemy.actor.x > enemy.start_x + enemy.patrol_distance:
                enemy.direction = -1
            elif enemy.actor.x < enemy.start_x - enemy.patrol_distance:
                enemy.direction = 1

            if player.actor.colliderect(enemy.actor):
                if player.vy > 0 and player.actor.bottom < enemy.actor.top + 10:
                    enemies.remove(enemy)
                    player.vy = JUMP_SPEED * 0.7
                else:
                    sounds.lose.play()
                    player.actor.pos = (0, HEIGHT-50)
                    player.vy = 0
                    reset_enemies()


        if keyboard.a:
            player.actor.x -= MOVE_SPEED
            player.facing_right = False
            player.update_animation('walk', ANIMATION_SPEED)
          
        elif keyboard.d:
            player.actor.x += MOVE_SPEED
            player.facing_right = True
            player.update_animation('walk', ANIMATION_SPEED)
        
        elif player.is_jumping:
            player.update_animation('jump', ANIMATION_SPEED)   
         
        else:
            player.update_animation('idle', ANIMATION_SPEED)
     
        if player.actor.bottom > HEIGHT - 30:
            player.actor.bottom = HEIGHT - 30
        if player.actor.left < 0:
            player.actor.left = 0
        if player.actor.right > WIDTH:
            player.actor.right = WIDTH
        if player.actor.top < 0:
            player.top = 0
        if player.actor.bottom > HEIGHT:
            player.actor.bottom = HEIGHT  
   
def draw_menu():
    screen.clear()
    screen.blit(background, (0, 0))
    
    screen.draw.text("SAVE YOUR BROTHER!", 
                    center=(WIDTH/2, HEIGHT/2 - 150),
                    fontsize=70,
                    color="yellow",
                    shadow=(2, 2))   
    screen.draw.text("W = Jump", 
                    center=(WIDTH - 100, 430),
                    fontsize=25,
                    color="yellow",
                    shadow=(1, 1)) 
    screen.draw.text("A/D = Move Left/Right", 
                    center=(WIDTH - 100, 460),
                    fontsize=25,
                    color="yellow",
                    shadow=(1, 1)) 

    
    start_color = START_HOVER if start_hover else START_COLOR
    exit_color = EXIT_HOVER if exit_hover else EXIT_COLOR

    screen.draw.filled_rect(start_button_pos, start_color)
    screen.draw.filled_rect(exit_button_pos, exit_color)
    
    screen.draw.text("START", center=(WIDTH/2, HEIGHT/2 - 35), fontsize=40, color="white")
    screen.draw.text("EXIT", center=(WIDTH/2, HEIGHT/2 + 45), fontsize=40, color="white")

    music_color = MUSIC_HOVER if music_hover else MUSIC_COLOR
    screen.draw.filled_circle(music_button_pos, MUSIC_BUTTON_RADIUS, music_color)

    if music_playing:
        screen.draw.text("Mute", center=music_button_pos, fontsize=20, color="white")
    else:
        screen.draw.text("Unmute", center=music_button_pos, fontsize=20, color="white")

def draw_game():
    screen.clear()  
    screen.blit(background, (0, 0))

    floor_rect = Rect((0, HEIGHT - 30), (WIDTH, 60))
    screen.draw.filled_rect(floor_rect, FLOOR_COLOR)
    for platform in platforms:
        screen.blit(PLATFORM_IMAGE, platform)

    for enemy in enemies:
        enemy.actor.draw()
    brother.actor.draw()
    player.actor.draw()

    music_color = MUSIC_HOVER if music_hover else MUSIC_COLOR
    screen.draw.filled_circle(music_button_pos, MUSIC_BUTTON_RADIUS, music_color)

    if music_playing:
        screen.draw.text("Mute", center=music_button_pos, fontsize=20, color="white")
    else:
        screen.draw.text("Unmute", center=music_button_pos, fontsize=20, color="white")

    if GAME_WON:
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (0, 0, 0, 180))
        if not music_playing:
            sounds.win.set_volume(0)
        screen.draw.text("YOU SAVED YOUR BROTHER!", 
                        center=(WIDTH/2, HEIGHT/2), 
                        fontsize=60, 
                        color="yellow")
        
        restart_color = START_HOVER if restart_hover else START_COLOR
        screen.draw.filled_rect(RESTART_BUTTON_POS, restart_color)
        screen.draw.text("MENU", 
                        center=(WIDTH/2, HEIGHT/2 + 125), 
                        fontsize=40, 
                        color="white")

def draw():
    if GAME_ACTIVE:
        draw_game()
    else:
        draw_menu()

def on_mouse_move(pos):
    global start_hover, exit_hover, music_hover, restart_hover
    global last_start_hover, last_exit_hover, last_music_hover, last_restart_hover

    last_start_hover = start_hover
    last_exit_hover = exit_hover
    last_music_hover = music_hover

    start_hover = start_button_pos.collidepoint(pos)
    exit_hover = exit_button_pos.collidepoint(pos)

    dx = pos[0] - music_button_pos[0]
    dy = pos[1] - music_button_pos[1]
    music_hover = math.sqrt(dx*dx + dy*dy) <= MUSIC_BUTTON_RADIUS

    if not GAME_ACTIVE:
        if (start_hover and not last_start_hover) or \
           (exit_hover and not last_exit_hover) or \
           (music_hover and not last_music_hover):
           sounds.hover.play()

    if GAME_WON:
        last_restart_hover = restart_hover
        restart_hover = RESTART_BUTTON_POS.collidepoint(pos)
        if restart_hover and not last_restart_hover:
            sounds.hover.play()       

def on_mouse_down(pos):
    global music_playing, GAME_ACTIVE, GAME_WON 
    

    dx = pos[0] - music_button_pos[0]
    dy = pos[1] - music_button_pos[1]
    if math.sqrt(dx*dx + dy*dy) <= MUSIC_BUTTON_RADIUS:
        music_playing = not music_playing
        
        if music_playing:
            music.set_volume(1)
            sounds.hover.set_volume(1)
            sounds.jump.set_volume(1)
            sounds.lose.set_volume(1)
            sounds.win.set_volume(1)
       
        else:
            music.set_volume(0)
            sounds.hover.set_volume(0)
            sounds.jump.set_volume(0)
            sounds.lose.set_volume(0)
            sounds.win.set_volume(0)
           
    if not GAME_ACTIVE:
        if start_button_pos.collidepoint(pos):
            GAME_ACTIVE = True
            player.actor.pos = (0, HEIGHT)
        
        if exit_button_pos.collidepoint(pos):
            exit()

    if GAME_WON and RESTART_BUTTON_POS.collidepoint(pos):
        # Reseta o jogo
        GAME_WON = False
        GAME_ACTIVE = False
        player.actor.pos = (0, HEIGHT-50)
        player.vy = 0
        reset_enemies()          

def on_key_down(key):
    if GAME_ACTIVE and key == keys.W and player.on_ground:
        player.vy = JUMP_SPEED
        player.on_ground = False    
        player.is_jumping = True  
        sounds.jump.play()  
        player.actor.image = 'player_jump_right' if player.facing_right else 'player_jump_left'
                  
