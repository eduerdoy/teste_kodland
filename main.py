import pgzero
import math
from pygame import Rect 

GAME_ACTIVE = False

WIDTH = 900
HEIGHT = 500

GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5
ANIMATION_SPEED = 0

player = Actor('player_sprite')
player.pos = (-35, 0)
player.vy = 0
player.on_ground = False
player.facing_right = True
player.is_jumping = False
player.animation_time = 0
player.current_frame = 0

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

START_COLOR = (50, 168, 82)    
START_HOVER = (60, 198, 97)    
EXIT_COLOR = (168, 50, 50)     
EXIT_HOVER = (198, 60, 60)     
MUSIC_COLOR = (238, 132, 0)    
MUSIC_HOVER = (255, 165, 0)  

last_start_hover = False
last_exit_hover = False
last_music_hover = False
start_hover = False
exit_hover = False

MUSIC_BUTTON_RADIUS = 25
music_playing = True
music_hover = False

music_button_pos = (WIDTH - 40, 40)
start_button_pos = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - 60), (BUTTON_WIDTH, BUTTON_HEIGHT))
exit_button_pos = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 + 20), (BUTTON_WIDTH, BUTTON_HEIGHT))



background = 'sample'



def update():
    # Garante que a música sempre esteja tocando
    if not music.is_playing('theme'):
        music.play('theme')
        music.set_volume(0.5)

    if GAME_ACTIVE:

        if GAME_ACTIVE:
            player.is_jumping = not player.on_ground

        if keyboard.left:
            player.x -= MOVE_SPEED
            player.facing_right = False
            update_player_animation('walk')
        elif keyboard.right:
            player.x += MOVE_SPEED
            player.facing_right = True
            update_player_animation('walk')
        else:
            update_player_animation('idle')

        # Atualiza animação de pulo
        if player.is_jumping:
            update_player_animation('jump')
        
        player.vy += GRAVITY  # Aplica gravidade
        player.y += player.vy 

        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
            player.vy = 0
            player.on_ground = True
        else:
            player.on_ground = False

        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH


        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        if player.top < 0:
            player.top = 0
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT    

def draw_menu():
    screen.clear()
    screen.blit(background, (0, 0))
    

    # Usa cores diferentes baseado no estado do hover
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
    player.draw()
    music_color = MUSIC_HOVER if music_hover else MUSIC_COLOR
    screen.draw.filled_circle(music_button_pos, MUSIC_BUTTON_RADIUS, music_color)

    if music_playing:
        screen.draw.text("Mute", center=music_button_pos, fontsize=20, color="white")
    else:
        screen.draw.text("Unmute", center=music_button_pos, fontsize=20, color="white")

def draw():
    if GAME_ACTIVE:
        draw_game()
    else:
        draw_menu()

def on_mouse_move(pos):
    global start_hover, exit_hover, music_hover
    global last_start_hover, last_exit_hover, last_music_hover

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

def on_mouse_down(pos):
    global music_playing, GAME_ACTIVE
    

    dx = pos[0] - music_button_pos[0]
    dy = pos[1] - music_button_pos[1]
    if math.sqrt(dx*dx + dy*dy) <= MUSIC_BUTTON_RADIUS:
        music_playing = not music_playing
        
        if music_playing:
            music.set_volume(1)
            sounds.hover.set_volume(1)
        else:
            music.set_volume(0)
            sounds.hover.set_volume(0)

    if not GAME_ACTIVE:
        if start_button_pos.collidepoint(pos):
            GAME_ACTIVE = True
            player.pos = (WIDTH//2, HEIGHT//2)
        
        if exit_button_pos.collidepoint(pos):
            exit()

def on_key_down(key):
    if GAME_ACTIVE and key == keys.SPACE and player.on_ground:
        player.vy = JUMP_SPEED
        player.on_ground = False    
            
def update_player_animation(state):
     # Atualiza o tempo da animação
    player.animation_time += ANIMATION_SPEED
    
    # Define os frames baseado no estado
    if state == 'idle':
        frames = ['player_idle_right', 'player_sprite'] if player.facing_right else ['player_sprite', 'player_idle_left2']
    elif state == 'walk':
        frames = ['player_walk_right2', 'player_walk_right1'] if player.facing_right else ['player_walk_left1', 'player_walk_left2']
    elif state == 'jump':
        frames = ['player_jump_right'] if player.facing_right else ['player_jump_left']
    
    # Atualiza o frame atual
    if player.animation_time >= 1:
        player.animation_time = 0
        player.current_frame = (player.current_frame + 1) % len(frames)
    
    # Aplica o sprite atual
    player.image = frames[player.current_frame]