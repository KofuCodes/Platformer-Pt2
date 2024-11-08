import pygame
import sys
import math
import asyncio
from level import Level
from settings import Settings
from game_data import levels

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

# Setup
sett = Settings()
screen = pygame.display.set_mode((sett.screen_width, sett.screen_height))
sett.screen = screen
clock = pygame.time.Clock()
current_level = sett.level_name
level = Level(levels[current_level], screen, sett)
in_game = False
dash_charge = pygame.Rect((20, sett.screen_height - 50), (200, 30))

async def run_game():
    global current_level, level, in_game

    # Load health bar images
    health_images = [
        pygame.image.load(f"./graphics/ui/health_bar/{i}.png").convert_alpha()
        for i in range(1, 6)
    ]
    health_images = [pygame.transform.scale_by(img, 4) for img in health_images]

    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            in_game = False  # Exit the game loop to return to the main menu

        screen.fill("black")
        if current_level != sett.level_name or sett.reload_level:
            sett.reload_level = False
            current_level = sett.level_name
            level = Level(levels[current_level], screen, sett)
        else:
            level.run()

            if sett.charge['dash'] < 120:
                sett.charge['dash'] += 2

            dash_charge.width = (sett.charge['dash'] / 120) * 200

            if 1 <= sett.health <= 5:
                screen.blit(health_images[sett.health - 1], (20, 60))

            dash_bar_index = min(5, math.floor(sett.charge['dash'] / 24))
            dash_bar = pygame.image.load(f"./graphics/ui/dash_bar/{dash_bar_index}.png")
            dash_bar = pygame.transform.scale_by(dash_bar, 4)
            screen.blit(dash_bar, (20, sett.screen_height - 600))

            if sett.invincible:
                current_time = pygame.time.get_ticks()
                if current_time - sett.invincibility_start_time > sett.invincibility_duration:
                    sett.invincible = False

            if sett.player_dead:
                if sett.health <= 0:
                    sett.score = 0
                    sett.health = 5
                    in_game = False
                else:
                    sett.player_dead = False

        pygame.display.flip()
        await asyncio.sleep(0)  # Required for pygbag
        clock.tick(60)

async def level_selection():
    global current_level, in_game
    levels_list = ["level0", "level1"]
    selected_index = 0
    scroll_offset = 0
    scroll_target = 0
    scroll_speed = 10

    while not in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(levels_list)
                    scroll_target = -screen.get_height() * selected_index
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(levels_list)
                    scroll_target = -screen.get_height() * selected_index
                elif event.key == pygame.K_RETURN:
                    sett.level_name = levels_list[selected_index]
                    in_game = True
                elif event.key == pygame.K_ESCAPE:
                    return

        scroll_offset += (scroll_target - scroll_offset) / scroll_speed

        screen.fill("black")
        font = pygame.font.Font("./graphics/ui/04B_30__.TTF", 50)
        for i, level_name in enumerate(levels_list):
            color = (255, 255, 255) if i == selected_index else (100, 100, 100)
            text = font.render(level_name, True, color)
            y_position = (screen.get_height() * i) + (screen.get_height() / 2) - (text.get_height() / 2) + scroll_offset
            screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, y_position))

        pygame.display.flip()
        await asyncio.sleep(0)  # Required for pygbag
        clock.tick(60)

async def show_controls():
    controls_font = pygame.font.Font("./graphics/ui/04B_30__.TTF", 35)
    controls_text = [
        "Controls:",
        "Arrow Keys - Move",
        "Z - Jump 2X",
        "X - Attack",
        "C - Dash",
        "ESC - Pause"
    ]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill("black")
        
        total_height = len(controls_text) * controls_font.get_linesize()
        start_y = (screen.get_height() - total_height) / 2

        for i, line in enumerate(controls_text):
            text_surface = controls_font.render(line, True, (255, 255, 255))
            x_position = (screen.get_width() - text_surface.get_width()) / 2
            y_position = start_y + i * controls_font.get_linesize()
            screen.blit(text_surface, (x_position, y_position))
        
        pygame.display.flip()
        await asyncio.sleep(0)  # Required for pygbag
        clock.tick(60)

async def main_menu():
    global in_game

    while not in_game:
        mouse = pygame.mouse.get_pos()
        height = screen.get_height()
        width = screen.get_width()
        color_light = (153, 196, 210)
        color_dark = (133, 176, 190)
        playfont = pygame.font.Font("./graphics/ui/04B_30__.TTF", 35)
        playtext = playfont.render('Start', True, (255, 255, 255))
        controls_text = playfont.render('Controls', True, (255, 255, 255))
        namefont = pygame.font.Font("./graphics/ui/04B_30__.TTF", 100)
        nametext = namefont.render("LOST KNIGHT", True, (255, 255, 255))
        
        # Load and scale background images
        bg_0 = pygame.transform.scale_by(pygame.image.load("./graphics/background/0.png"), 4)
        bg_1 = pygame.transform.scale_by(pygame.image.load("./graphics/background/1.png"), 4)
        bg_2 = pygame.transform.scale_by(pygame.image.load("./graphics/background/2.png"), 4)
        bg_top = pygame.transform.scale_by(pygame.image.load("./graphics/background/top.png"), 4)

        play_button_width = 150
        play_button_height = 50
        controls_button_width = controls_text.get_width() + 20
        controls_button_height = 50

        title_y_offset = -100
        button_y_offset = -50

        play_button_x = (width - play_button_width) / 2
        play_button_y = height / 2 + 100 + button_y_offset
        controls_button_x = (width - controls_button_width) / 2
        controls_button_y = height / 2 + 160 + button_y_offset

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_x <= mouse[0] <= play_button_x + play_button_width and play_button_y <= mouse[1] <= play_button_y + play_button_height:
                    await level_selection()
                elif controls_button_x <= mouse[0] <= controls_button_x + controls_button_width and controls_button_y <= mouse[1] <= controls_button_y + controls_button_height:
                    await show_controls()

        # Draw background layers
        screen.blit(bg_0, (0, height - 488))
        screen.blit(bg_1, (0, height - 488))
        screen.blit(bg_2, (0, height - 488))
        screen.blit(bg_top, (0, height - 720))

        # Draw buttons
        if play_button_x <= mouse[0] <= play_button_x + play_button_width and play_button_y <= mouse[1] <= play_button_y + play_button_height:
            pygame.draw.rect(screen, color_light, (play_button_x, play_button_y, play_button_width, play_button_height), border_radius=10)
        else:
            pygame.draw.rect(screen, color_dark, (play_button_x, play_button_y, play_button_width, play_button_height), border_radius=10)
        screen.blit(playtext, (play_button_x + (play_button_width - playtext.get_width()) / 2, play_button_y + (play_button_height - playtext.get_height()) / 2))

        if controls_button_x <= mouse[0] <= controls_button_x + controls_button_width and controls_button_y <= mouse[1] <= controls_button_y + controls_button_height:
            pygame.draw.rect(screen, color_light, (controls_button_x, controls_button_y, controls_button_width, controls_button_height), border_radius=10)
        else:
            pygame.draw.rect(screen, color_dark, (controls_button_x, controls_button_y, controls_button_width, controls_button_height), border_radius=10)
        screen.blit(controls_text, (controls_button_x + (controls_button_width - controls_text.get_width()) / 2, controls_button_y + (controls_button_height - controls_text.get_height()) / 2))

        # Draw title
        screen.blit(nametext, (width / 2 - (nametext.get_size()[0] / 2), height / 2 - (nametext.get_size()[1] / 2) + title_y_offset))

        pygame.display.flip()
        await asyncio.sleep(0)  # Required for pygbag
        clock.tick(60)

async def main():
    global in_game
    while True:
        if in_game:
            await run_game()
        else:
            await main_menu()
        await asyncio.sleep(0)

# Start the game
asyncio.run(main())