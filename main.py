'''
please read before reading our remarkable code 

known issues 
- timer and score keep disappearing and reappearing 
- in-game exit button needs to be violently pressed nine times before it actually exits 
- game over audio plays even after restarting 
- asset quality is questionable 
'''

import pygame
import random
import sys

# yolo init all the things
pygame.init()
pygame.mixer.init()

# spretend we're in the 90s with this retro arcade vibe-resolution 
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Bug Busters")

# load up the visuals (bugs, bombs, etc.)
background = pygame.image.load('assets/background.jpg').convert()
bug_images = {
    'roach': pygame.transform.scale(pygame.image.load('assets/roach.png').convert_alpha(), (50, 50)),
    'ant': pygame.transform.scale(pygame.image.load('assets/ant.png').convert_alpha(), (50, 50)),
    'ladybug': pygame.transform.scale(pygame.image.load('assets/bug.png').convert_alpha(), (50, 50)),
}
bomb_image = pygame.transform.scale(pygame.image.load('assets/bomb.png').convert_alpha(), (50, 50))
blood_image = pygame.transform.scale(pygame.image.load('assets/blood.png').convert_alpha(), (50, 50))

# sounds and vibes
bug_click_sound = pygame.mixer.Sound('assets/bug_click.mp3')
bomb_click_sound = pygame.mixer.Sound('assets/explode_bomb.mp3')
menu_music = 'assets/start_menu.mp3'
game_over_sound = pygame.mixer.Sound('assets/game_over.mp3')
level_up_sound = pygame.mixer.Sound('assets/level_up.mp3')

# default fonts are lame
font = pygame.font.Font('assets/SP.ttf', 48)
small_font = pygame.font.Font('assets/SP.ttf', 24)

# game vars, the real magic numbers
score = 0
timer = 10  
level = 1
bugs = []
bombs = []
bloods = []
game_over = False
in_menu = True
target_score = 0  
music_on = True  

# spawn a bug, because... game logic? 
def spawn_bug():
    bug_type = random.choice(list(bug_images.keys()))
    x = random.randint(0, WIDTH - 50)
    y = random.randint(0, HEIGHT - 50)
    speed = random.choice([-1, 1]) * random.randint(1, 3)
    bugs.append({'rect': pygame.Rect(x, y, 50, 50), 'type': bug_type, 'speed': speed})

# throw a bomb into the mix, why not?
def spawn_bomb():
    x = random.randint(0, WIDTH - 50)
    y = random.randint(0, HEIGHT - 50)
    bombs.append(pygame.Rect(x, y, 50, 50))

# draws text loololol
def draw_text(text, font, color, surface, x, y, center=True):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y)) if center else textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

# making the buttons round
def draw_rounded_button(rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=10)

# game reset, like starting fresh or whatever
def reset_game():
    global score, level, bugs, bombs, bloods, game_over, in_menu, target_score, start_ticks
    score = 0
    level = 1
    bugs.clear()
    bombs.clear()
    bloods.clear()
    game_over = False
    in_menu = False
    target_score = 0
    start_ticks = pygame.time.get_ticks()  # start ticking again, not gonna wait
    pygame.mixer.music.stop()  # shut that music up
    if music_on:
        pygame.mixer.music.load(menu_music)  # gotta reload the music for some reason idk
    start_ticks = pygame.time.get_ticks()  # reset the ticks again cuz why not

# oh hey, you made it to the next level, here we go again
def next_level():
    global level, score, target_score, game_over, start_ticks
    level += 1
    target_score = score  # next level goal is what you just did. do better!
    score = 0  # lol back to zero
    bugs.clear()
    bombs.clear()
    bloods.clear()
    game_over = False
    start_ticks = pygame.time.get_ticks()  # reset the timer for the new level
    level_up_sound.play()

# on/off music toggle, aka mom can't hear me play late night (or can she?)
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

# main game loop, where all the fun happens
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# menu music, cuz silence is awkward
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)

while True:
    screen.fill((0, 0, 0))

    if in_menu:
        # main menu stuff
        draw_text('Bug Busters', font, (255, 255, 255), screen, WIDTH // 2, 100)

        # play button, click it or don't. your call.
        play_button = pygame.Rect(WIDTH // 2 - 100, 200, 200, 65)
        draw_rounded_button(play_button, (0, 200, 0))
        draw_text('Play', font, (255, 255, 255), screen, play_button.centerx, play_button.centery)

        draw_text("Credits:", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text("Shivashis Adhikari - Scripter AND GUI", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Paribesh Khatiwada - Scripter", small_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 90)

        # music button, click if you hate fun (no offesne)
        music_button = pygame.Rect(20, HEIGHT - 80, 150, 50)
        draw_rounded_button(music_button, (100, 100, 100))
        draw_text("Music", small_font, (255, 255, 255), screen, music_button.centerx, music_button.centery)

        # exit button for those "I have other things to do" moments
        exit_button = pygame.Rect(WIDTH - 180, HEIGHT - 80, 150, 50)
        draw_rounded_button(exit_button, (200, 0, 0))
        draw_text("Exit", small_font, (255, 255, 255), screen, exit_button.centerx, exit_button.centery)

        # checking for menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    in_menu = False
                    pygame.mixer.music.stop()  # music stops, serious gamer time
                    start_ticks = pygame.time.get_ticks()
                elif music_button.collidepoint(event.pos):
                    toggle_music()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    else:
        # actual gameplay, bg and all
        screen.blit(background, (0, 0))

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # buttons for game over screen
                    reset_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 20, 260, 65)
                    next_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 90, 260, 65)
                    if reset_button.collidepoint(event.pos):
                        reset_game()
                    elif next_button.collidepoint(event.pos) and score >= target_score + 1:
                        next_level()
                else:
                    # click bugs, get points. simple.
                    for bug in bugs[:]:
                        if bug['rect'].collidepoint(event.pos):
                            bugs.remove(bug)
                            bug_click_sound.play()
                            bloods.append({'rect': bug['rect'], 'timer': 0})
                            score += 1

                    # click bombs, ruin everything. nice.
                    for bomb in bombs[:]:
                        if bomb.collidepoint(event.pos):
                            bomb_click_sound.play()
                            game_over = True
                            pygame.mixer.music.stop()
                            game_over_sound.play()

        # game logic
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > timer:
            game_over = True  # time's up. git gud next time.

        # game state: if not game over, keep spawning stuff
        if not game_over:
            if random.randint(0, 100) < 2 + level:
                spawn_bug()
            if random.randint(0, 200) < 1 + level:
                spawn_bomb()

            # move them bugs around, because bugs don't just stand still
            for bug in bugs:
                bug['rect'].y += bug['speed']
                if bug['rect'].top < 0 or bug['rect'].bottom > HEIGHT:
                    bug['speed'] *= -1

        # draw bugs
        for bug in bugs:
            screen.blit(bug_images[bug['type']], (bug['rect'].x, bug['rect'].y))

        # draw bombs
        for bomb in bombs:
            screen.blit(bomb_image, (bomb.x, bomb.y))

        # draw blood stains. cuz why not?
        for blood in bloods:
            screen.blit(blood_image, (blood['rect'].x, blood['rect'].y))
            blood['timer'] += 1
            if blood['timer'] > 30:
                bloods.remove(blood)

        # draw the score and time without that annoying flicker
        draw_text(f"Score: {score}", small_font, (255, 255, 255), screen, 10, 10, center=False)
        draw_text(f"Time: {max(0, int(timer - seconds))}", small_font, (255, 255, 255), screen, WIDTH - 150, 10, center=False)

        # game over screen stuff
        if game_over:
            draw_text("Game Over!", font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 50)
            reset_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 20, 260, 65)
            draw_rounded_button(reset_button, (200, 0, 0))
            draw_text("Restart", small_font, (255, 255, 255), screen, reset_button.centerx, reset_button.centery)

            # show next level button only if you earned it
            if score >= target_score + 1:
                next_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 90, 260, 65)
                draw_rounded_button(next_button, (0, 200, 0))
                draw_text("Next Level", small_font, (255, 255, 255), screen, next_button.centerx, next_button.centery)

        # exit button always available, even in game over
        exit_button = pygame.Rect(WIDTH - 180, HEIGHT - 80, 150, 50)
        draw_rounded_button(exit_button, (200, 0, 0))
        draw_text("Exit", small_font, (255, 255, 255), screen, exit_button.centerx, exit_button.centery)

        # check exit button during game
        for event in pygame.event.get():
            if exit_button.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

    # update the display, gotta see those changes
    pygame.display.flip()
    clock.tick(60)