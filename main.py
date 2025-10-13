from colored import Back, Fore, Style
import pygame 
from pygame.locals import *
from classes import Character, Map, Npc, Party, Button, Img, Images, Buttons, Text_Log
import sys
import time

MULTI = 1.2
WIDTH, HEIGHT = 1000 * MULTI, 800 * MULTI
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)
FAKE_SCREEN = SCREEN.copy()
pygame.display.set_caption("Dark Realm")
pygame.font.init()
MY_FONT = pygame.font.SysFont('Comic Sans MS', int(18 * MULTI))
STAT_FONT = pygame.font.SysFont('arialblack', int(13 * MULTI))
SPELL_FONT = pygame.font.SysFont('arialblack', int(16 * MULTI))
DESC_FONT = pygame.font.SysFont('arialblack', int(12 * MULTI))
LOG_FONT = pygame.font.SysFont('calibribold', int(18 * MULTI))
TEXT_LOG = Text_Log(FAKE_SCREEN, MULTI, LOG_FONT)


up_arrow_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/move_up.png").convert_alpha()
down_arrow_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/move_down.png").convert_alpha()
left_arrow_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/move_left.png").convert_alpha()
right_arrow_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/move_right.png").convert_alpha()
turn_left_arrow_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/move_rl.png").convert_alpha()
turn_right_arrow_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/move_rr.png").convert_alpha()
skip_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/skip.png").convert_alpha()
action_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action.png").convert_alpha()
attack_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action_attack.png").convert_alpha()
block_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action_block.png").convert_alpha()
pull_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action_pull.png").convert_alpha()
push_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action_push.png").convert_alpha()
use_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action_use.png").convert_alpha()
game_over_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/game_over.png").convert_alpha()
spell_image = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/action_spell.png").convert_alpha()


def main() -> None:
    map_to_load = "01"
    party = Party(SCREEN, MULTI,TEXT_LOG)
    map = Map(map_to_load, party)
    clock = pygame.time.Clock()
    game_loop(map, party, clock)


def game_loop(map, party, clock):
    run = True
    buttons = Buttons()
    images = Images()
    inventory = Images()

    load_images(buttons, images, inventory, map)

    images = check_tiles(map, party, images)
    draw(map, images)
    
    action_taken = False
    movement = False

    show_screen(map)

    while run:
        game_over = True
        clock.tick(60)
        for button in buttons.button.values():
            button.visible = button.default
        
        for character in party.p_members:
            if character.alive:
                game_over = False
            if character.alive == False:
                if character.p_name == "Skeleton" and "undead" in character.abilities or "golem" in character.abilities:
                    party.p_members.remove(character)

        if game_over:
            buttons.button["game_over"].toggle()
            draw_all(map,party,images,buttons, inventory)
            start_time = time.process_time()
            while time.process_time() - start_time < 1.5:
                ...
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons.button['arrow_up'].rect.collidepoint(pos):
                    direction = 'w' 
                    buttons.button['arrow_up'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif buttons.button['arrow_down'].rect.collidepoint(pos):
                    direction = 's'   
                    buttons.button['arrow_down'].toggle()  
                    action_taken, movement = party.move_direction(party, direction, map)  
                elif buttons.button['arrow_left'].rect.collidepoint(pos):
                    direction = 'a'  
                    buttons.button['arrow_left'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif buttons.button['arrow_right'].rect.collidepoint(pos):
                    direction = 'd'  
                    buttons.button['arrow_right'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif buttons.button['arrow_turn_left'].rect.collidepoint(pos):
                    direction = 'q'
                    party.rotate_party(direction)
                    map.rotate_map_clockwise()
                    map.find_party(party)
                    buttons.button['arrow_turn_left'].toggle()
                    movement = True
                elif buttons.button['arrow_turn_right'].rect.collidepoint(pos):
                    direction = 'e'
                    party.rotate_party(direction)
                    map.rotate_map_anti_clockwise()
                    map.find_party(party)
                    buttons.button['arrow_turn_right'].toggle()
                    movement = True
                elif buttons.button['action_button'].rect.collidepoint(pos):
                    buttons.button['skip_button'].toggle()
                    buttons.button['action_button'].toggle()
                    buttons.button['pull_button'].toggle()
                    buttons.button['push_button'].toggle()
                    buttons.button['use_button'].toggle()
                    buttons.button['block_button'].toggle()
                    buttons.button['arrow_up'].toggle()
                    buttons.button['arrow_down'].toggle()
                    buttons.button['arrow_left'].toggle()
                    buttons.button['arrow_right'].toggle()
                    buttons.button['arrow_turn_left'].toggle()
                    buttons.button['arrow_turn_right'].toggle()
                    buttons.button['attack_button'].toggle()
                    buttons.button['spell_button'].toggle()
                    TEXT_LOG.add_to_log(f"{party.inventories[0].owner.p_name}'s turn to take an action!", color=(0,0,100))
                    for character in party.p_members:
                        character.active = True
                        draw_all(map,party,images,buttons, inventory)
                        SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        if character.alive:
                            run = action_selected(map,character,run, buttons, party, images, inventory)
                        party.shift_order()
                    action_taken = True
                    movement = True
                elif images.image["main_floor_0"].rect.collidepoint(pos) and images.image["main_floor_0"].visible:
                    images.image["main_floor_0"].toggle()
                    draw(map, images)
                    party.choose_inventory(map.map_grid[party.p_position[0] - 1][party.p_position[1]].floor[0])
                    map.map_grid[party.p_position[0] - 1][party.p_position[1]].floor.pop(0)
                    SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                    pygame.display.update()
                elif images.image["main_floor_1"].rect.collidepoint(pos) and images.image["main_floor_1"].visible:
                    images.image["main_floor_1"].toggle()
                    draw(map, images)
                    party.choose_inventory(map.map_grid[party.p_position[0] - 1][party.p_position[1]].floor[1])
                    map.map_grid[party.p_position[0] - 1][party.p_position[1]].floor.pop(1)
                    SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                    pygame.display.update()
                elif images.image["main_floor_2"].rect.collidepoint(pos) and images.image["main_floor_2"].visible:
                    images.image["main_floor_2"].toggle()
                    draw(map, images)
                    party.choose_inventory(map.map_grid[party.p_position[0] - 1][party.p_position[1]].floor[2])
                    map.map_grid[party.p_position[0] - 1][party.p_position[1]].floor.pop(2)
                    SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction = 'w' 
                    buttons.button['arrow_up'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif event.key == pygame.K_s:
                    direction = 's' 
                    buttons.button['arrow_down'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif event.key == pygame.K_a:
                    direction = 'a' 
                    buttons.button['arrow_left'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif event.key == pygame.K_d:
                    direction = 'd' 
                    buttons.button['arrow_right'].toggle()
                    action_taken, movement = party.move_direction(party, direction, map)
                elif event.key == pygame.K_q:                  
                    direction = 'q'
                    party.rotate_party(direction)
                    map.rotate_map_clockwise()
                    map.find_party(party)
                    buttons.button['arrow_turn_left'].toggle()
                    movement = True
                elif event.key == pygame.K_e:                  
                    direction = 'e'
                    party.rotate_party(direction)
                    map.rotate_map_clockwise()
                    map.find_party(party)
                    buttons.button['arrow_turn_right'].toggle()
                    movement = True

        if action_taken:
            mob_ai(map,party, images, buttons, inventory)
            action_taken = False
        if movement:
            current_grid = map.map_grid[party.p_position[0]][party.p_position[1]]
            if current_grid.interaction != None and current_grid.interaction.type == "floor":
                if current_grid.interaction.name == 'pit':
                    x = 0
                    y = 0
                    wall = Img(image="pit", x=0, y=HEIGHT // 2, height=HEIGHT // 2, width=WIDTH // 2, name="pit", tileset=map.tileset)
                    wall.toggle()
                    while wall.y_coord > 0:
                        if wall.y_coord < 0:
                            wall.y_coord = 0
                        draw_shift_screen(images, x, y)
                        wall.change_coords(x,y)
                        wall.draw(FAKE_SCREEN)
                        draw_background(party)
                        SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        y += -3 * MULTI
                    current_grid.interaction.pit_fall(party)
            images = check_tiles(map, party, images)
            check_entities(map, party, images)
            movement = False
        draw_all(map,party,images,buttons, inventory)


def load_images(buttons, images, inventory, map):
    buttons.add_button('arrow_up', button=Button(image=up_arrow_image, x=369 * MULTI, y=420 * MULTI, visible=True))
    buttons.add_button('arrow_down', button=Button(image=down_arrow_image, x=369 * MULTI, y=486 * MULTI, visible=True))
    buttons.add_button('arrow_left', button=Button(image=left_arrow_image, x=302 * MULTI, y=486 * MULTI, visible=True))
    buttons.add_button('arrow_right', button=Button(image=right_arrow_image, x=436 * MULTI, y=486 * MULTI, visible=True)) 
    buttons.add_button('arrow_turn_left', button=Button(image=turn_left_arrow_image, x=302 * MULTI, y=420 * MULTI, visible=True))
    buttons.add_button('arrow_turn_right', button=Button(image=turn_right_arrow_image, x=436 * MULTI, y=420 * MULTI, visible=True))
    buttons.add_button('skip_button', button=Button(image=skip_image, x=502 * MULTI, y=420 * MULTI, visible=False))
    buttons.add_button('action_button', button=Button(image=action_image, x=502 * MULTI, y=487 * MULTI, visible=True))
    buttons.add_button('attack_button', button=Button(image=attack_image, x=524 * MULTI, y=368 * MULTI, visible=False))
    buttons.add_button('block_button', button=Button(image=block_image, x=524 * MULTI, y=316 * MULTI, visible=False))
    buttons.add_button('pull_button', button=Button(image=pull_image, x=524 * MULTI, y=109 * MULTI, visible=False)) 
    buttons.add_button('use_button', button=Button(image=use_image, x=524 * MULTI, y=161 * MULTI, visible=False)) 
    buttons.add_button('push_button', button=Button(image=push_image, x=524 * MULTI, y=5 * MULTI, visible=False)) 
    buttons.add_button('spell_button', button=Button(image=spell_image, x=524 * MULTI, y=264 * MULTI, visible=False)) 
    buttons.add_button('game_over', button=Button(image=game_over_image, x=150 * MULTI, y=180 * MULTI, visible=False)) 

    images.add_image("main", Img(name="main", image="00", x=0,y=0,height=HEIGHT // 2, width=WIDTH // 2, tileset=map.tileset))
    images.add_image("main_ent", Img(name="main_ent", image="07", x=0,y=0,height=HEIGHT // 2, width=WIDTH // 2, tileset=""))
    images.add_image("main_centre", Img(name="main_centre", image="centre", x=110 * MULTI,y=88 * MULTI,height=224 * MULTI,width=280 * MULTI, tileset=map.tileset))
    images.add_image("main_left", Img(name="main_left", image="side_01", x=0 * MULTI, y=0 * MULTI, height=HEIGHT / 2, width=WIDTH // 2 // 4 - 15, tileset=map.tileset))
    images.add_image("main_right", Img(name="main_right", image="side_02", x=390 * MULTI, y=0 * MULTI, height=HEIGHT / 2, width=WIDTH // 2 // 4 - 15, tileset=map.tileset))
    images.add_image("main_floor_0", Img(name="main_floor_0", image="07", x=200 * MULTI, y=305 * MULTI, height=100 * MULTI, width=200 * MULTI, tileset=""))
    images.add_image("main_floor_1", Img(name="main_floor_1", image="07", x=300 * MULTI, y=300 * MULTI, height=100 * MULTI, width=200 * MULTI, tileset=""))
    images.add_image("main_floor_2", Img(name="main_floor_2", image="07", x=300 * MULTI, y=300 * MULTI, height=100 * MULTI, width=200 * MULTI, tileset=""))
    images.add_image("middle_centre", Img(name="middle_centre", image="centre", x=172 * MULTI,y=138 * MULTI,height=129 * MULTI,width=157 * MULTI, tileset=map.tileset))
    images.add_image("middle_left", Img(name="middle_left", image="side_01", x=110 * MULTI, y=89 * MULTI, height=224 * MULTI, width=WIDTH // 2 // 4 // 2 + 1, tileset=map.tileset))
    images.add_image("middle_right", Img(name="middle_right", image="side_02", x=327 * MULTI, y=89 * MULTI, height=224 * MULTI, width=WIDTH // 2 // 4 // 2 + 1, tileset=map.tileset))
    images.add_image("middle_floor_0", Img(name="middle_floor_0", image="07", x=220 * MULTI, y=250 * MULTI, height=70 * MULTI, width=140 * MULTI, tileset=""))
    images.add_image("middle_floor_1", Img(name="middle_floor_1", image="07", x=280 * MULTI, y=250 * MULTI, height=70 * MULTI, width=140 * MULTI, tileset=""))
    images.add_image("middle_floor_2", Img(name="middle_floor_2", image="07", x=300 * MULTI, y=250 * MULTI, height=70 * MULTI, width=140 * MULTI, tileset=""))
    images.add_image("end_centre", Img(name="end_centre", image="centre", x=206 * MULTI,y=165 * MULTI,height=72 * MULTI,width=89 * MULTI, tileset=map.tileset))
    images.add_image("end_left", Img(name="end_left", image="side_01", x=173 * MULTI, y=137 * MULTI, height=130 * MULTI, width=WIDTH // 2 // 8 // 2 + (3 * MULTI), tileset=map.tileset))
    images.add_image("end_right", Img(name="end_right", image="side_02", x=295 * MULTI, y=137 * MULTI, height=130 * MULTI, width=WIDTH // 2 // 8 // 2 + (3 * MULTI), tileset=map.tileset))
    images.add_image("dist_centre_entity_far", Img(name="dist_centre_entity", image="07", x=190 * MULTI,y=150 * MULTI,height=79 * MULTI,width=107 * MULTI, tileset=""))
    images.add_image("end_centre_entity_far", Img(name="end_centre_entity", image="07", x=172 * MULTI,y=138 * MULTI,height=129 * MULTI,width=157 * MULTI, tileset=""))
    images.add_image("end_left_entity_far", Img(name="end_left_entity", image="07", x=55 * MULTI,y=138 * MULTI,height=130 * MULTI, width=120 * MULTI, tileset=""))
    images.add_image("end_right_entity_far", Img(name="end_right_entity", image="07", x=325 * MULTI, y=138 * MULTI, height=130 * MULTI, width=120 * MULTI, tileset=""))
    images.add_image("end_fog", Img(name="end_fog", image="fog", x=172 * MULTI,y=138 * MULTI,height=223 // 2 + 15 * MULTI, width=(280 // 2 + 17) * MULTI, tileset=""))
    images.add_image("end_centre_mob", Img(name="end_centre_mob", image="07", x=205 * MULTI, y=170 * MULTI, height=HEIGHT // 8, width=WIDTH // 9, tileset=""))
    images.add_image("end_left_mob", Img(name="end_left_mob", image="07", x=20 * MULTI, y=170 * MULTI, height=HEIGHT // 8, width=WIDTH // 9, tileset=""))
    images.add_image("end_right_mob", Img(name="end_right_mob", image="07", x=370 * MULTI, y=170 * MULTI, height=HEIGHT // 8, width=WIDTH // 9, tileset=""))
    images.add_image("dist_centre_entity_close", Img(name="dist_centre_entity", image="07", x=200 * MULTI,y=160 * MULTI,height=79 * MULTI,width=107 * MULTI, tileset=""))
    images.add_image("dist_left_entity_close", Img(name="dist_left_entity", image="07", x=113 * MULTI,y=160 * MULTI,height=79 * MULTI,width=94 * MULTI, tileset=""))
    images.add_image("dist_right_entity_close", Img(name="dist_right_entity", image="07", x=295 * MULTI, y=160 * MULTI,height=79 * MULTI,width=95 * MULTI, tileset=""))
    images.add_image("end_centre_entity_close", Img(name="end_centre_entity", image="07", x=172 * MULTI,y=138 * MULTI,height=129 * MULTI,width=157 * MULTI, tileset=""))
    images.add_image("end_left_entity_close", Img(name="end_left_entity", image="07", x=62 * MULTI,y=138 * MULTI,height=130 * MULTI, width=110 * MULTI, tileset=""))
    images.add_image("end_right_entity_close", Img(name="end_right_entity", image="07", x=328 * MULTI, y=138 * MULTI, height=130 * MULTI, width=110 * MULTI, tileset=""))
    images.add_image("middle_centre_entity_far", Img(name="middle_centre_entity", image="07", x=110 * MULTI,y=89 * MULTI,height=223 * MULTI,width=280 * MULTI, tileset=""))
    images.add_image("middle_left_entity_far", Img(name="middle_left_entity", image="07", x=0 * MULTI, y=110 * MULTI, height=200 * MULTI, width=110 * MULTI, tileset=""))
    images.add_image("middle_right_entity_far", Img(name="middle_right_entity", image="07", x=390 * MULTI, y=89 * MULTI, height=223 * MULTI, width=110 * MULTI, tileset=""))
    images.add_image("middle_fog", Img(name="main_fog", image="fog", x=110 * MULTI,y=89 * MULTI,height=223 * MULTI, width=280 * MULTI, tileset=""))
    images.add_image("middle_centre_mob", Img(name="middle_centre_mob", image="07", x=180 * MULTI, y=170 * MULTI, height=HEIGHT // 6, width=WIDTH // 7, tileset=""))
    images.add_image("middle_left_mob", Img(name="middle_left_mob", image="07", x=-10 * MULTI, y=170 * MULTI, height=HEIGHT // 6, width=WIDTH // 7, tileset=""))
    images.add_image("middle_right_mob", Img(name="middle_right_mob", image="07", x=370 * MULTI, y=170 * MULTI, height=HEIGHT // 6, width=WIDTH // 7, tileset=""))
    images.add_image("middle_centre_entity_close", Img(name="middle_centre_entity", image="07", x=110 * MULTI,y=89 * MULTI,height=223 * MULTI,width=280 * MULTI, tileset=""))
    images.add_image("middle_left_entity_close", Img(name="middle_left_entity", image="07", x=0, y=89 * MULTI, height=223 * MULTI, width=120 * MULTI, tileset=""))
    images.add_image("middle_right_entity_close", Img(name="middle_right_entity", image="07", x=390 * MULTI, y=89 * MULTI, height=223 * MULTI, width=120 * MULTI, tileset=""))
    images.add_image("main_centre_entity_far", Img(name="main_centre_entity", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("main_fog", Img(name="main_fog", image="fog", x=0,y=0,height=HEIGHT // 2, width=WIDTH // 2, tileset=""))
    images.add_image("main_centre_mob", Img(name="main_centre_mob", image="07", x=120 * MULTI, y=120 * MULTI, height=264 * MULTI, width=264 * MULTI, tileset=""))
    images.add_image("main_left_mob", Img(name="main_left_mob", image="07", x=-70 * MULTI, y=120 * MULTI, height=264 * MULTI, width=264 * MULTI, tileset=""))
    images.add_image("main_right_mob", Img(name="main_right_mob", image="07", x=370 * MULTI, y=120 * MULTI, height=HEIGHT // 4, width=WIDTH // 5, tileset=""))
    images.add_image("main_centre_entity_close", Img(name="main_centre_entity", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))

    inventory.add_image("0",Img(name="0", image="07", x=669 * MULTI,y=64 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset=""))
    inventory.add_image("1",Img(name="1", image="07", x=(669 + 61) * MULTI,y=64 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset=""))   
    inventory.add_image("2",Img(name="2", image="07", x=(669 + 122) * MULTI,y=64 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset="")) 
    inventory.add_image("3",Img(name="3", image="07", x=(669 + 183) * MULTI,y=64 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset="")) 
    inventory.add_image("4",Img(name="4", image="07", x=(669 + 244) * MULTI,y=64 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset=""))
    inventory.add_image("5",Img(name="5", image="07", x=669 * MULTI,y=125 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset=""))
    inventory.add_image("6",Img(name="6", image="07", x=(669 + 61) * MULTI,y=125 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset=""))   
    inventory.add_image("7",Img(name="7", image="07", x=(669 + 122) * MULTI,y=125 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset="")) 
    inventory.add_image("8",Img(name="8", image="07", x=(669 + 183) * MULTI,y=125 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset="")) 
    inventory.add_image("9",Img(name="9", image="07", x=(669 + 244) * MULTI,y=125 * MULTI,height=59 * MULTI, width=59 * MULTI, tileset="")) 


def draw_shift_screen(images, x, y):
    for image in images.image.values():
        image.change_coords(x,y)
        image.draw(FAKE_SCREEN)


def action_selected(map, character, run, buttons, party, images, inventory):
    action_taken = False
    while action_taken != True:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and character.active:
                pos = pygame.mouse.get_pos()
                if  buttons.button['attack_button'].rect.collidepoint(pos):
                    buttons.button['attack_button'].toggle()
                    draw_all(map,party,images,buttons, inventory)
                    pygame.display.update()                    
                    frame = 0
                    while frame <= 5:
                        animation_screen = FAKE_SCREEN.copy()
                        character.play_animation(SCREEN=animation_screen, width=500, height=500, frame=round(frame), animation=character.attack_animation)
                        SCREEN.blit(pygame.transform.scale(animation_screen, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        frame += 0.07
                    attack_action(map,character, party)
                    action_taken = True
                    character.active = False
                elif buttons.button['block_button'].rect.collidepoint(pos):
                    buttons.button['block_button'].toggle()
                    frame = 0
                    while frame <= 5:
                        animation_screen = FAKE_SCREEN.copy()
                        character.play_animation(SCREEN=animation_screen, width=500, height=500, frame=round(frame), animation=character.block_animation)
                        SCREEN.blit(pygame.transform.scale(animation_screen, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        frame += 0.07
                    TEXT_LOG.add_to_log(f"{character.p_name} blocks!", (0,120,0))
                    action_taken = True
                    character.active = False
                    character.status.append("block")
                elif buttons.button['pull_button'].rect.collidepoint(pos):
                    buttons.button['pull_button'].toggle()
                    target = map.map_grid[party.p_position[0]][party.p_position[1]].interaction
                    if target != None and target.action == 'pull' and map.check_directions(party.p_direction, map.map_grid[party.p_position[0]][party.p_position[1]].interaction.direction) == 1:
                        target.interact()
                        pygame.display.update()
                        TEXT_LOG.add_to_log(f"{character.p_name} pulls the {target.name}!", (0,120,0))                        
                    action_taken = True
                    character.active = False
                elif buttons.button['push_button'].rect.collidepoint(pos):
                    buttons.button['push_button'].toggle()
                    target = map.map_grid[party.p_position[0]][party.p_position[1]].interaction
                    if target != None and target.action == 'push' and map.check_directions(party.p_direction, map.map_grid[party.p_position[0]][party.p_position[1]].interaction.direction) == 1:
                        target.interact()
                        pygame.display.update()
                        TEXT_LOG.add_to_log(f"{character.p_name} pushes the {target.name}!", (0,120,0))                        
                    action_taken = True
                    character.active = False
                elif buttons.button['use_button'].rect.collidepoint(pos):
                    buttons.button['use_button'].toggle()
                    use_select(map, party, character, images, buttons, inventory, action_taken)                      
                    action_taken = True
                    character.active = False
                elif buttons.button['skip_button'].rect.collidepoint(pos):
                    buttons.button['skip_button'].toggle()
                    action_taken = True 
                    character.active = False
                elif buttons.button['spell_button'].rect.collidepoint(pos):
                    buttons.button['spell_button'].toggle()
                    spell_images = Images()
                    number = 0
                    for spell in character.spells:
                        spell_images.add_image(str(number),Img(name=spell.name, image=spell.icon, x=314, y=328,height=66, width=66, tileset=""))
                        spell_images.image[str(number)].update_advanced(spell_images.image[str(number)].image, spell_images.image[str(number)].height * MULTI, spell_images.image[str(number)].width * MULTI)
                        spell_images.image[str(number)].toggle()   
                        number += 1
                    action_taken = spell_select(map, party, character, spell_images, images, buttons, inventory, action_taken)
                    draw_all(map, party, images, buttons, inventory)                                                        
    return run   

def use_select(map, party, character, images, buttons, inventory, action_taken):
    close, equip, drop = party.draw_uses(character, FAKE_SCREEN)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and character.active:
                pos = pygame.mouse.get_pos()
                if close.collidepoint(pos):
                    return action_taken



def spell_select(map, party, character, spell_images, images, buttons, inventory, action_taken):
    if len(spell_images.image) < 1:
        return action_taken
    select_spell = False
    draw_all(map, party, images, buttons, inventory)
    spell_start = 0
    spell_end = 1
    target = character
    forward, back, close = draw_spells(spell_images, spell_start, spell_end, character)
    while select_spell != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and character.active:
                pos = pygame.mouse.get_pos()
                for j in range(len(spell_images.image.values())):
                    if spell_images.image[str(j)].rect.collidepoint(pos):
                        for spell in character.spells:
                            print(f"spell name: {spell.name}\nimages name: {spell_images.image[str(j)].name}")
                            if spell.name == spell_images.image[str(j)].name and spell_images.image[str(j)].visible:
                                spell_to_cast = spell
                                if spell_to_cast.target_type == "party_m":
                                    target = spell_to_cast.select_target(party, character, spell, SCREEN)
                                elif spell_to_cast.target_type == "mob":
                                    target = map.map_grid[party.p_position[0] - 1][party.p_position[1]].npc
                                spell.set_cast(character.style)
                                draw_all(map, party, images, buttons, inventory)
                                spell.play_spell_animation(character, SCREEN, FAKE_SCREEN)                
                                spell_to_cast.cast_spell(target, character, party, map)
                                select_spell = True
                                action_taken = True
                                character.active = False
                                return action_taken
                if close.collidepoint(pos):
                    return action_taken
                if forward != None and forward.collidepoint(pos) and spell_end < len(character.spells) - 1:
                    spell_images.image[str(spell_start)].toggle()
                    spell_images.image[str(spell_end)].toggle()
                    spell_end += 2
                    spell_start += 2
                    draw_all(map, party, images, buttons, inventory)                        
                    forward, back, close = draw_spells(spell_images, spell_start, spell_end, character)
                if back != None and back.collidepoint(pos) and spell_start > 0:
                    spell_images.image[str(spell_start)].toggle()
                    if spell_end <= len(spell_images.image) - 1:
                        spell_images.image[str(spell_end)].toggle()
                    spell_end -= 2
                    spell_start -= 2
                    draw_all(map, party, images, buttons, inventory)                        
                    forward, back, close = draw_spells(spell_images, spell_start, spell_end, character)
                        
        SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
        pygame.display.update()




def draw_spells(spell_images, spell_start, spell_end, character):
    spellbook= pygame.transform.scale(pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/spellbook.png"), (600 * MULTI, 400 * MULTI))
    FAKE_SCREEN.blit(spellbook, (250 * MULTI,250 * MULTI))
    spellbook_bk = pygame.transform.scale(pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/spellbook_bk.png"), (45 * MULTI, 45 * MULTI))
    if spell_start > 0:
        back = FAKE_SCREEN.blit(spellbook_bk, (304 * MULTI,268 * MULTI))
    else:
        back = None        
    spellbook_fw = pygame.transform.scale(pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/spellbook_fw.png"), (45 * MULTI, 45 * MULTI))
    if spell_end < len(character.spells) - 1:
        forward = FAKE_SCREEN.blit(spellbook_fw, (762 * MULTI,268 * MULTI))
    else:
        forward = None
    spellbook_x = pygame.transform.scale(pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/close.png"), (30 * MULTI, 30 * MULTI))
    close = FAKE_SCREEN.blit(spellbook_x, (825 * MULTI, 620 * MULTI))  
    spell_images.image[str(spell_start)].toggle()
    spell_images.image[str(spell_start)].move(x=314 * MULTI, y=328 * MULTI)
    spell_images.image[str(spell_start)].draw(FAKE_SCREEN)
    if spell_end <= len(spell_images.image) - 1:
        spell_images.image[str(spell_end)].toggle()
        spell_images.image[str(spell_end)].move(x=593 * MULTI, y=328 * MULTI)
        spell_images.image[str(spell_end)].draw(FAKE_SCREEN)

    for spell in character.spells:
        if spell.name == spell_images.image[str(spell_start)].name:
            text_spell_name = SPELL_FONT.render(f'{spell.name}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_name, (spell_images.image[str(spell_start)].x_coord + (10 * MULTI), spell_images.image[str(spell_start)].y_coord - (30 * MULTI)))
            if spell.caster_mana_modifier < 0:
                text_spell_mana = STAT_FONT.render(f'Mana Cost:  {spell.caster_mana_modifier}', False, (0, 0, 0))
                FAKE_SCREEN.blit(text_spell_mana, (spell_images.image[str(spell_start)].x_coord + (75  * MULTI), spell_images.image[str(spell_start)].y_coord + (20 * MULTI)))
            if spell.caster_health_modifier < 0:
                text_spell_health = STAT_FONT.render(f'Health Cost:  {spell.caster_health_modifier}', False, (0, 0, 0))
                FAKE_SCREEN.blit(text_spell_health, (spell_images.image[str(spell_start)].x_coord + (75  * MULTI), spell_images.image[str(spell_start)].y_coord + (40 * MULTI)))
            text_spell_desc_1 = DESC_FONT.render(f'{spell.description_1}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_desc_1, (spell_images.image[str(spell_start)].x_coord, spell_images.image[str(spell_start)].y_coord + (100 * MULTI)))
            text_spell_desc_2 = DESC_FONT.render(f'{spell.description_2}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_desc_2, (spell_images.image[str(spell_start)].x_coord, spell_images.image[str(spell_start)].y_coord + (120 * MULTI)))
            text_spell_desc_3 = DESC_FONT.render(f'{spell.description_3}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_desc_3, (spell_images.image[str(spell_start)].x_coord, spell_images.image[str(spell_start)].y_coord + (140 * MULTI)))
        if spell_end <= len(spell_images.image) - 1 and spell.name == spell_images.image[str(spell_end)].name:
            text_spell_name = SPELL_FONT.render(f'{spell.name}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_name, (spell_images.image[str(spell_end)].x_coord + (10 * MULTI), spell_images.image[str(spell_end)].y_coord - (30 * MULTI)))
            if spell.caster_mana_modifier < 0:
                text_spell_mana = STAT_FONT.render(f'Mana Cost:  {spell.caster_mana_modifier}', False, (0, 0, 0))
                FAKE_SCREEN.blit(text_spell_mana, (spell_images.image[str(spell_end)].x_coord + (75 * MULTI), spell_images.image[str(spell_end)].y_coord + (20 * MULTI)))
            if spell.caster_health_modifier < 0:
                text_spell_health = STAT_FONT.render(f'Health Cost:  {spell.caster_health_modifier}', False, (0, 0, 0))
                FAKE_SCREEN.blit(text_spell_health, (spell_images.image[str(spell_end)].x_coord + (75 * MULTI), spell_images.image[str(spell_end)].y_coord + (40 * MULTI)))
            text_spell_desc_1 = DESC_FONT.render(f'{spell.description_1}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_desc_1, (spell_images.image[str(spell_end)].x_coord - (10 * MULTI), spell_images.image[str(spell_end)].y_coord + (100 * MULTI)))
            text_spell_desc_2 = DESC_FONT.render(f'{spell.description_2}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_desc_2, (spell_images.image[str(spell_end)].x_coord - (10 * MULTI), spell_images.image[str(spell_end)].y_coord + (120 * MULTI)))
            text_spell_desc_3 = DESC_FONT.render(f'{spell.description_3}', False, (0, 0, 0))
            FAKE_SCREEN.blit(text_spell_desc_3, (spell_images.image[str(spell_end)].x_coord - (10 * MULTI), spell_images.image[str(spell_end)].y_coord + (140 * MULTI)))

    return forward, back, close


def attack_action(map,character, party):
    if map.map_grid[party.p_position[0] - 1][party.p_position[1]].npc == None:
        return
    mob = map.map_grid[party.p_position[0] - 1][party.p_position[1]].npc
    weapon = character.weapon
    character.attack(mob)
    mob.check_status()
    weapon.check_durability(character)


def show_screen(map) -> None:
    for i in range(len(map.map_grid)):
        for tile in map.map_grid[i]:
            print(f"{tile.colour}{tile.icon}{' '}", end="")
        print(f"{Fore.white}")


def draw_buttons(buttons):
    for button in buttons.button.values():
        if button.visible:
            button.draw(FAKE_SCREEN, MULTI)
        


def check_tiles(map, party, images):
    x = party.p_position[0]
    y = party.p_position[1]

    for image in images.image.values():
        if image.visible:
            image.toggle()  

    if party.p_direction == 'N' or party.p_direction == 'S':
        images.image['main'].update(image='00')
    else:
        images.image['main'].update(image='01')
    if map.map_grid[party.p_position[0]][party.p_position[1]].interaction != None and map.map_grid[party.p_position[0] - 1][party.p_position[1]].icon == 'R':
        if map.map_grid[party.p_position[0]][party.p_position[1]].interaction.direction == None and map.map_grid[party.p_position[0]][party.p_position[1]].interaction.name != "wall":
            images.image['main_ent'].update(image=f"{map.map_grid[party.p_position[0]][party.p_position[1]].interaction.name}_{map.map_grid[party.p_position[0]][party.p_position[1]].interaction.status}") 
        elif map.map_grid[party.p_position[0]][party.p_position[1]].interaction.name != "wall" and map.check_directions(party.p_direction, map.map_grid[party.p_position[0]][party.p_position[1]].interaction.direction) == 1:
            images.image['main_ent'].update(image=f"{map.map_grid[party.p_position[0]][party.p_position[1]].interaction.name}_{map.map_grid[party.p_position[0]][party.p_position[1]].interaction.status}") 



    if map.map_grid[x - 1][y].icon == 'R':
        return images
    else:
        for i in range(len(map.map_grid[x - 1][y].floor)):
            images.image[f"main_floor_{i}"].update(image=map.map_grid[x - 1][y].floor[i].floor_sprite)
        if party.p_position[0] % 2 == 0 and party.p_position[1] % 2 != 0 or party.p_position[0] % 2 != 0 and party.p_position[1] % 2 == 0:
            main_image = "ceil_01"
        else:
            main_image = "ceil_02"

        images.image['main'].update(image=main_image)
        if map.map_grid[x - 1][y - 1].icon == "R":
            images.image['main_left'].update(image='side_08')
        if map.map_grid[x - 1][y + 1].icon == "R":
            images.image['main_right'].update(image='side_07')
        images.image['main_fog'].update(image='fog')

    if  map.map_grid[x - 2][y].icon == 'R':
        images.image['main_centre'].update(image='centre') 
    else:
        for i in range(len(map.map_grid[x - 2][y].floor)):
            images.image[f"middle_floor_{i}"].update(image=map.map_grid[x - 2][y].floor[i].floor_sprite)


    if map.map_grid[x - 1][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 3][y - 1].icon == 'O' and map.map_grid[x - 2][y - 2].icon == 'R' and map.map_grid[x - 3][y - 2].icon == 'R' and map.map_grid[x - 2][y].icon == 'O':
        images.image['main_left'].update(image='side_11')
    elif map.map_grid[x - 1][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 3][y - 1].icon == 'O' and map.map_grid[x - 3][y - 2].icon == 'R' and map.map_grid[x - 2][y].icon == 'O' and map.map_grid[x - 3][y].icon == 'R':
        images.image['main_left'].update(image='side_09')
    elif map.map_grid[x - 1][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 3][y - 1].icon == 'O' and map.map_grid[x - 3][y - 2].icon != 'O' and map.map_grid[x - 3][y].icon == 'R' and map.map_grid[x - 2][y].icon == 'O' and map.map_grid[x - 1][y - 2].icon == 'R':
        images.image['main_left'].update(image='side_08')

    elif map.map_grid[x - 1][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 3][y - 1].icon == 'O' and map.map_grid[x - 4][y - 2].icon == 'R':
        images.image['main_left'].update(image='side_05')    
    elif map.map_grid[x - 1][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 3][y - 1].icon == 'R':
        images.image['main_left'].update(image='side_03')
    elif map.map_grid[x - 1][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'R':
        images.image['main_left'].update(image='side_02')

    if map.map_grid[x - 1][y + 1].icon == 'O' and map.map_grid[x - 2][y + 1].icon == 'O' and map.map_grid[x - 3][y + 1].icon == 'O' and map.map_grid[x - 2][y + 2].icon == 'R' and map.map_grid[x - 3][y + 2].icon == 'R' and map.map_grid[x - 2][y].icon == 'O':
        images.image['main_right'].update(image='side_12')
    elif map.map_grid[x - 1][y + 1].icon == 'O' and map.map_grid[x - 2][y + 1].icon == 'O' and map.map_grid[x - 3][y + 1].icon == 'O' and map.map_grid[x - 3][y + 2].icon == 'R' and map.map_grid[x - 2][y].icon == 'O' and map.map_grid[x - 3][y].icon == 'R':
        images.image['main_right'].update(image='side_10') 
    elif map.map_grid[x - 1][y + 1].icon == 'O' and map.map_grid[x - 2][y + 1].icon == 'O' and map.map_grid[x - 3][y + 1].icon == 'O' and map.map_grid[x - 4][y + 2].icon == 'R':
        images.image['main_right'].update(image='side_06')  
    elif map.map_grid[x - 1][y + 1].icon == 'O' and map.map_grid[x - 2][y + 1].icon == 'O' and map.map_grid[x - 3][y + 1].icon == 'R':
        images.image['main_right'].update(image='side_04') 
    elif map.map_grid[x - 1][y + 1].icon == 'O' and map.map_grid[x - 2][y + 1].icon == 'R':
        images.image['main_right'].update(image='side_01')  
 
    if map.map_grid[x - 2][y].icon == 'R':
        return images
    
    if map.map_grid[x - 2][y - 1].icon == 'R':
        images.image['middle_left'].update(image='side_08')
    if map.map_grid[x - 2][y + 1].icon == 'R':
        images.image['middle_right'].update(image='side_07')   
        images.image['middle_fog'].update(image='fog')  
    
    if map.map_grid[x - 3][y].icon == 'R':
        images.image['middle_centre'].update(image='centre') 
 
    if map.map_grid[x - 3][y - 1].icon == 'O' and map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 4][y - 1].icon == 'R':
        images.image['middle_left'].update(image='side_04') 
    elif map.map_grid[x - 2][y - 1].icon == 'O' and map.map_grid[x - 3][y - 1].icon == 'R': 
        images.image['middle_left'].update(image='side_02')  
    
    if map.map_grid[x - 3][y + 1].icon == 'O' and map.map_grid[x - 2][y + 1].icon == 'O' and map.map_grid[x - 4][y + 1].icon == 'R':
        images.image['middle_right'].update(image='side_03') 
    elif map.map_grid[x - 2][y + 1].icon == 'O' and map.map_grid[x - 3][y + 1].icon == 'R':
        images.image['middle_right'].update(image='side_01') 

    if map.map_grid[x - 3][y].icon == 'R':
        return images


    images.image['end_fog'].update(image='fog')
    if map.map_grid[x - 4][y].icon == 'R':
        images.image['end_centre'].update(image='centre')
    
    if map.map_grid[x - 3][y - 1].icon == 'R':
        images.image['end_left'].update(image='side_08')
    if map.map_grid[x - 3][y + 1].icon == 'R':
        images.image['end_right'].update(image='side_07')


    if map.map_grid[x - 3][y - 1].icon == 'R' and map.map_grid[x - 3][y + 1].icon == 'R':  
        return images

    
    if map.map_grid[x - 3][y - 1].icon == 'O' and map.map_grid[x - 4][y - 1].icon == 'R':
        images.image['end_left'].update(image='side_02')   


    if map.map_grid[x - 3][y + 1].icon == 'O' and map.map_grid[x - 4][y + 1].icon == 'R':
        images.image['end_right'].update(image='side_01')   

    
    return images
 

def check_entities(map, party, images) -> None:
    x = party.p_position[0]
    y = party.p_position[1]

    for i in range(x - 4, x): 
        for j in range(y - 3, y + 3):
            if map.map_grid[i][j].npc != None:
                draw_mob(i, x, j, y, party, map, images)
            if map.map_grid[i][j].interaction != None:
                draw_entity(i,x,j,y,party,map,images)


def draw_entity(entity_x_pos,player_x_pos, entity_y_pos, player_y_pos, party,map, images) -> None:

    entity = map.map_grid[entity_x_pos][entity_y_pos]

    directions = [
        'N',
        'E',
        'S',
        'W',
    ]

    if entity.interaction.type == "wall_c":
        return

    if map.map_grid[player_x_pos - 1][player_y_pos].icon != "O":
        return

    if entity_y_pos == player_y_pos:
        position = 'centre'
    elif entity_y_pos - player_y_pos == -1:
        position = 'left'
    else:
        position = 'right'
    

    if player_x_pos - entity_x_pos > 2 and position != 'centre':
        distance = 2
    else:
        distance = 1

    sprite_to_draw = f"{entity.interaction.name}_{entity.interaction.status}_{position}_{map.map_grid[entity_x_pos + 1][entity_y_pos].icon.lower()}{distance}{entity.interaction.tileset}"

    if entity.interaction.direction != None and position == 'centre':
        if entity.interaction.direction in "NS" and party.p_direction not in "NS" or entity.interaction.direction in "EW" and party.p_direction not in "EW":
            if directions.index(party.p_direction) - directions.index(entity.interaction.direction) == 1:
                sprite_to_draw = f"{entity.interaction.name}_{entity.interaction.status}_{"left"}_{map.map_grid[entity_x_pos + 1][entity_y_pos].icon.lower()}{distance}r{entity.interaction.tileset}"
            else:
                sprite_to_draw = f"{entity.interaction.name}_{entity.interaction.status}_{"right"}_{map.map_grid[entity_x_pos + 1][entity_y_pos].icon.lower()}{distance}r{entity.interaction.tileset}"
 
    if player_x_pos - entity_x_pos > 3:
        sprite_to_draw = f"{entity.interaction.name}_{entity.interaction.status}_centre_{map.map_grid[entity_x_pos + 1][entity_y_pos].icon.lower()}1{entity.interaction.tileset}"

    if abs(entity_x_pos - player_x_pos) == 1 and entity_y_pos == player_y_pos:
        images.image[f'main_centre_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)
    elif abs(entity_x_pos - player_x_pos) == 2 and entity_y_pos == player_y_pos:
        if map.map_grid[player_x_pos - 1][player_y_pos].icon != 'R':
            images.image[f'middle_centre_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)
    elif abs(entity_x_pos - player_x_pos) == 3 and entity_y_pos == player_y_pos:
        if map.map_grid[player_x_pos - 2][player_y_pos].icon != 'R':
            images.image[f'end_centre_entity_{entity.interaction.distance}'].update(image=sprite_to_draw) 
    elif abs(entity_x_pos - player_x_pos) == 4 and entity_y_pos == player_y_pos:
        if map.map_grid[player_x_pos - 3][player_y_pos].icon != 'R':
            images.image[f'dist_centre_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)
       

    if abs(entity_x_pos - player_x_pos) == 2 and entity_y_pos - player_y_pos == -1:
        if map.map_grid[player_x_pos - 1][player_y_pos - 1].icon != 'R':
            images.image[f'middle_left_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)
    elif abs(entity_x_pos - player_x_pos) == 3 and entity_y_pos - player_y_pos == -1:
        if map.map_grid[player_x_pos - 2][player_y_pos - 1].icon != 'R' and map.map_grid[player_x_pos - 2][player_y_pos].icon != 'R':
            images.image[f'end_left_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)     
    elif abs(entity_x_pos - player_x_pos) == 4 and entity_y_pos - player_y_pos == -1:
        if map.map_grid[player_x_pos - 2][player_y_pos - 1].icon != 'R' and map.map_grid[player_x_pos - 2][player_y_pos].icon != 'R' and map.map_grid[player_x_pos - 3][player_y_pos].icon != 'R':
            images.image[f'dist_left_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)  

    if abs(entity_x_pos - player_x_pos) == 2 and entity_y_pos - player_y_pos == 1:
        if map.map_grid[player_x_pos - 1][player_y_pos + 1].icon != 'R':
            images.image[f'middle_right_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)
    elif abs(entity_x_pos - player_x_pos) == 3 and entity_y_pos - player_y_pos == 1:
        if map.map_grid[player_x_pos - 2][player_y_pos + 1].icon != 'R' and map.map_grid[player_x_pos - 2][player_y_pos].icon != 'R':
            images.image[f'end_right_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)
    elif abs(entity_x_pos - player_x_pos) == 4 and entity_y_pos - player_y_pos == 1:
        if map.map_grid[player_x_pos - 2][player_y_pos + 1].icon != 'R' and map.map_grid[player_x_pos - 2][player_y_pos].icon != 'R'and map.map_grid[player_x_pos - 3][player_y_pos].icon != 'R':
            images.image[f'dist_right_entity_{entity.interaction.distance}'].update(image=sprite_to_draw)

def draw_mob(mob_x_pos, player_x_pos, mob_y_pos, player_y_pos, party, map, images) -> None:
    mob = map.map_grid[mob_x_pos][mob_y_pos].npc
    if map.map_grid[player_x_pos - 1][player_y_pos].icon != 'O':
        return
    
    d_result = map.check_directions(party.p_direction, mob.direction)
    if d_result == 1:
        sprite_to_draw = f"{mob.sprite}_u"
    elif d_result == 0:
        sprite_to_draw = f"{mob.sprite}_d"
    elif d_result == 2:
        sprite_to_draw = f"{mob.sprite}_r"
    else:
        sprite_to_draw = f"{mob.sprite}_l"

    if mob.alive == False:
        sprite_to_draw = mob.s_death           
 
    if abs(mob_x_pos - player_x_pos) == 1 and mob_y_pos == player_y_pos:
        images.image["main_centre_mob"].update_advanced(image=sprite_to_draw, height=mob.height, width=mob.width)
    elif abs(mob_x_pos - player_x_pos) == 2 and mob_y_pos == player_y_pos:
        if map.map_grid[player_x_pos - 1][player_y_pos].icon != 'R':
            images.image["middle_centre_mob"].update_advanced(image=sprite_to_draw, height=mob.height // 2, width=mob.width // 2)
    elif abs(mob_x_pos - player_x_pos) == 3 and mob_y_pos == player_y_pos:
        if map.map_grid[player_x_pos - 2][player_y_pos].icon != 'R':
            images.image["end_centre_mob"].update_advanced(image=sprite_to_draw, height=mob.height // 3, width=mob.width // 3)

    elif abs(mob_x_pos - player_x_pos) == 1 and mob_y_pos - player_y_pos == -1:
        images.image["main_left_mob"].update_advanced(image=sprite_to_draw, height=mob.height, width=mob.width)
    elif abs(mob_x_pos - player_x_pos) == 2 and mob_y_pos - player_y_pos == -1:
        if map.map_grid[player_x_pos - 1][player_y_pos - 1].icon != 'R':
            images.image["middle_left_mob"].update_advanced(image=sprite_to_draw, height=mob.height // 2, width=mob.width // 2)
    elif abs(mob_x_pos - player_x_pos) == 3 and mob_y_pos - player_y_pos == -1:
        if map.map_grid[player_x_pos - 2][player_y_pos - 1].icon != 'R' and map.map_grid[player_x_pos - 1][player_y_pos - 1].icon != 'R':
            images.image["end_left_mob"].update_advanced(image=sprite_to_draw, height=mob.height // 3, width=mob.width // 3)

    elif abs(mob_x_pos - player_x_pos) == 1 and mob_y_pos - player_y_pos == 1:
        images.image["main_right_mob"].update_advanced(image=sprite_to_draw, height=mob.height, width=mob.width)
    elif abs(mob_x_pos - player_x_pos) == 2 and mob_y_pos - player_y_pos == 1:
        if map.map_grid[player_x_pos - 1][player_y_pos + 1].icon != 'R':
            images.image["middle_right_mob"].update_advanced(image=sprite_to_draw, height=mob.height // 2, width=mob.width // 2)
    elif abs(mob_x_pos - player_x_pos) == 3 and mob_y_pos - player_y_pos == 1:
        if map.map_grid[player_x_pos - 2][player_y_pos + 1].icon != 'R' and map.map_grid[player_x_pos - 1][player_y_pos + 1].icon != 'R':
            images.image["end_right_mob"].update_advanced(image=sprite_to_draw, height=mob.height // 3, width=mob.width // 3)


def mob_ai(map, party, images, buttons, inventory):
    x = party.p_position[0]
    y = party.p_position[1]
    i_modifier = 0
    j_modifier = 0
    moved_to = []
    directions = [
        'N',
        'E',
        'S',
        'W'
    ]


    for i in reversed(range(x - 4, x)): 
        for j in range(y - 3, y + 3):
            mob = map.map_grid[i][j].npc
            distance = 0
            if mob == None or mob.alive == False:
                continue

            if y - j > 0:
                j_modifier = 1
                distance = 1
                if distance + directions.index(party.p_direction) > 3:
                    mob.direction = 'N'
                else:
                    mob.direction = directions[directions.index(party.p_direction) + distance]
            elif y - j < 0:
                j_modifier = -1
                distance =  -1
                if distance + directions.index(party.p_direction) < 0:
                    mob.direction = 'W'
                else:
                    mob.direction = directions[directions.index(party.p_direction) + distance]
            elif (i, j) not in moved_to:
                i_modifier = 1
                if party.p_direction == 'S':
                    mob.direction = 'N'
                elif party.p_direction == 'N':
                    mob.direction = 'S'
                elif party.p_direction == 'E':
                    mob.direction = 'W' 
                else:
                    mob.direction = 'E'
            if map.map_grid[i + 1][j].icon == 'P' or map.map_grid[i][j + 1].icon == 'P' or map.map_grid[i][j - 1].icon == 'P' or map.map_grid[i - 1][j].icon == 'P':
                if (i, j) not in moved_to:
                    mob_attack(mob, images, party, map, buttons, inventory)    
            elif map.map_grid[i + i_modifier][j + j_modifier].interaction == None or map.map_grid[i + i_modifier][j + j_modifier].interaction.ai_blocker != True: 
                if map.map_grid[i + i_modifier][j + j_modifier].npc == None or map.map_grid[i + i_modifier][j + j_modifier].npc.alive == False:
                    if map.map_grid[i + i_modifier][j + j_modifier].icon == 'O' and (i + i_modifier, j + j_modifier) not in moved_to:
                        moved_to.append((i + i_modifier, j + j_modifier))                                                                     
                        map.map_grid[i + i_modifier][j + j_modifier].npc = map.map_grid[i][j].npc
                        map.map_grid[i + i_modifier][j + j_modifier].colour = Fore.blue
                        map.map_grid[i][j].npc = None
                        map.map_grid[i][j].colour = Fore.black

              
def draw_all(map, party, images, buttons, inventory):
    check_tiles(map, party, images)
    check_entities(map, party, images)
    draw(map, images)
    draw_background(party)
    party.draw_inventories(FAKE_SCREEN, MY_FONT)
    TEXT_LOG.draw_log_small()
    draw_buttons(buttons)
    SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
    pygame.display.update()


def mob_attack(mob, images, party, map, buttons, inventory):
    frame = 0
    mob.turn_mob(party)
    draw_all(map, party, images, buttons, inventory)
    images.image["main_centre_mob"].toggle()
    draw(map, images)
    draw_background(party)
    draw_buttons(buttons)
    party.draw_inventories(FAKE_SCREEN, MY_FONT)
    TEXT_LOG.draw_log_small()
    while frame <= mob.a_frames:
        animation_screen = FAKE_SCREEN.copy()
        mob.play_animation(SCREEN=animation_screen, width=abs(mob.width // MULTI), height=abs(mob.height // MULTI), frame=round(frame), animation=mob.s_attack, multi=MULTI)
        SCREEN.blit(pygame.transform.scale(animation_screen, SCREEN.get_rect().size), (00, 00))
        pygame.display.update()
        frame += mob.a_speed
    images.image["main_centre_mob"].toggle()
    SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
    pygame.display.update()
    mob.attack(party, TEXT_LOG)  
    draw_all(map, party, images, buttons, inventory)
def draw_background(party):
    background = pygame.transform.scale(pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/background_01.png"), (WIDTH, HEIGHT))
    FAKE_SCREEN.blit(background, (0,0))   
    text_dir = STAT_FONT.render(f'direction: {party.p_direction}', False, (0, 0, 0))
    FAKE_SCREEN.blit(text_dir, (700 * MULTI,10 * MULTI))


def draw(map, images):
    for image in images.image.values():
        image.draw(FAKE_SCREEN)

        
if __name__ == "__main__":
    main()