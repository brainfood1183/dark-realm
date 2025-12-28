from colored import Back, Fore, Style
import pygame 
from pygame.locals import *
from classes import Character, Map, Npc, Party, Button, Img, Images, Buttons, Text_Log
import sys
import time

MULTI = 1
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
    map_to_load = "03"
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

    draw_walls(map, party, images)
    draw(map, images)
    
    action_taken = False
    movement = False
    direction = 'o'

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
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                break
            character_first = party.p_members[0]
 
            if character_first.weapon.image_blit != None and character_first.weapon.image_blit.collidepoint(pos):
                wep_name_draw = False
                while character_first.weapon.image_blit.collidepoint(pos):
                    if wep_name_draw == False:
                        text_item = DESC_FONT.render(f'{character_first.weapon.name}!', False, (0, 0, 0))
                        text_item_rect = text_item.get_rect()
                        text_item_rect.center = (pos[0], pos[1])
                        FAKE_SCREEN.blit(text_item, text_item_rect)
                        SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        wep_name_draw = True
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
            if character_first.head.image_blit != None and character_first.head.image_blit.collidepoint(pos):
                head_name_draw = False
                while character_first.head.image_blit.collidepoint(pos):
                    if head_name_draw == False:
                        text_item = DESC_FONT.render(f'{character_first.head.name}!', False, (0, 0, 0))
                        text_item_rect = text_item.get_rect()
                        text_item_rect.center = (pos[0], pos[1])
                        FAKE_SCREEN.blit(text_item, text_item_rect)
                        SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        head_name_draw = True
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
            if character_first.chest.image_blit != None and character_first.chest.image_blit.collidepoint(pos):
                chest_name_draw = False
                while character_first.chest.image_blit.collidepoint(pos):
                    if chest_name_draw == False:
                        text_item = DESC_FONT.render(f'{character_first.chest.name}!', False, (0, 0, 0))
                        text_item_rect = text_item.get_rect()
                        text_item_rect.center = (pos[0], pos[1])
                        FAKE_SCREEN.blit(text_item, text_item_rect)
                        SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
                        pygame.display.update()
                        chest_name_draw = True
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                    map.rotate_map_anti_clockwise()
                    map.find_party(party)
                    buttons.button['arrow_turn_right'].toggle()
                    movement = True
        if action_taken:
            mob_ai(map,party, images, buttons, inventory)
            action_taken = False
        if movement:


            current_grid = map.map_grid[party.p_position[0]][party.p_position[1]]
            check_floor(party, current_grid, images, map)
            draw_walls(map, party, images)
            # images = check_tiles(map, party, images)
            check_entities(map, party, images)
            movement = False
        draw_all(map,party,images,buttons, inventory)


def check_floor(party, current_grid, images, map):
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
    
    images.add_image("bg", Img(name="bg", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))

    images.add_image("wall_-42", Img(name="wall_-42", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-4-2", Img(name="wall_-4-2", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-41", Img(name="wall_-41", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-4-1", Img(name="wall_-4-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-40", Img(name="wall_-40", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("main_floor_0", Img(name="main_floor_0", image="07", x=200 * MULTI, y=305 * MULTI, height=100 * MULTI, width=200 * MULTI, tileset=""))
    images.add_image("main_floor_1", Img(name="main_floor_1", image="07", x=300 * MULTI, y=300 * MULTI, height=100 * MULTI, width=200 * MULTI, tileset=""))
    images.add_image("main_floor_2", Img(name="main_floor_2", image="07", x=300 * MULTI, y=300 * MULTI, height=100 * MULTI, width=200 * MULTI, tileset=""))

    images.add_image("object_-43", Img(name="object_-43", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-4-3", Img(name="object_-4-3", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-42", Img(name="object_-42", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-4-2", Img(name="object_-4-2", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-41", Img(name="object_-41", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-4-1", Img(name="object_-4-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-40", Img(name="object_-40", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("middle_floor_0", Img(name="middle_floor_0", image="07", x=220 * MULTI, y=250 * MULTI, height=70 * MULTI, width=140 * MULTI, tileset=""))
    images.add_image("middle_floor_1", Img(name="middle_floor_1", image="07", x=280 * MULTI, y=250 * MULTI, height=70 * MULTI, width=140 * MULTI, tileset=""))
    images.add_image("middle_floor_2", Img(name="middle_floor_2", image="07", x=300 * MULTI, y=250 * MULTI, height=70 * MULTI, width=140 * MULTI, tileset=""))

    images.add_image("wall_-3-2", Img(name="wall_-3-2", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-32", Img(name="wall_-32", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("object_-3-2", Img(name="object_-3-2", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-32", Img(name="object_-32", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-3-1", Img(name="object_-3-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-31", Img(name="object_-31", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-30", Img(name="object_-30", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("npc_-3-2", Img(name="npc_-3-2", image="07", x=-140,y=80,height=HEIGHT // 2 // 2.1,width=WIDTH // 2 // 2.1, tileset=""))
    images.add_image("npc_-32", Img(name="npc_-32", image="07", x=400,y=80,height=HEIGHT // 2 // 2.1,width=WIDTH // 2 // 2.1, tileset=""))
    images.add_image("npc_-3-1", Img(name="npc_-3-1", image="07", x=-20,y=80,height=HEIGHT // 2 // 2.1,width=WIDTH // 2 // 2.1, tileset=""))
    images.add_image("npc_-31", Img(name="npc_-31", image="07", x=270,y=80,height=HEIGHT // 2 // 2.1,width=WIDTH // 2 // 2.1, tileset=""))
    images.add_image("wall_-3-1", Img(name="wall_-3-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-31", Img(name="wall_-31", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("npc_-30", Img(name="npc_-30", image="07", x=130,y=80,height=HEIGHT // 2 // 2.1,width=WIDTH // 2 // 2.1, tileset=""))
    images.add_image("wall_-30", Img(name="wall_-30", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.image["floor_-30"] = Images()
    images.image["floor_-3-1"] = Images()
    images.image["floor_-31"] = Images()
    images.image["floor_-3-2"] = Images()
    images.image["floor_-32"] = Images()

    images.add_image("wall_-2-2", Img(name="wall_-2-2", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-22", Img(name="wall_-22", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-2-1", Img(name="wall_-2-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-21", Img(name="wall_-21", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("wall_-20", Img(name="wall_-20", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))

    images.add_image("object_-2-2", Img(name="object_-2-2", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-22", Img(name="object_-22", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("object_-2-1", Img(name="object_-2-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-21", Img(name="object_-21", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("npc_-2-1", Img(name="npc_-2-1", image="07", x=-150,y=50,height=HEIGHT // 2 // 1.5,width=WIDTH // 2 // 1.5, tileset=""))
    images.add_image("npc_-21", Img(name="npc_-21", image="07", x=300,y=50,height=HEIGHT // 2 // 1.5,width=WIDTH // 2 // 1.5, tileset=""))
    images.add_image("object_-20", Img(name="object_-20", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("npc_-20", Img(name="npc_-20", image="07", x=90,y=50,height=HEIGHT // 2 // 1.5,width=WIDTH // 2 // 1.5, tileset=""))

    images.add_image("fog_-2-1", Img(name="fog_-2-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("wall_-1-1", Img(name="wall_-1-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("fog_-21", Img(name="fog_-21", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("wall_-11", Img(name="wall_-11", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("fog_-20", Img(name="fog_-20", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.image["floor_-20"] = Images()
    images.image["floor_-2-1"] = Images()
    images.image["floor_-21"] = Images()

    images.add_image("object_-1-1", Img(name="object_-1-1", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-11", Img(name="object_-11", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.add_image("object_-10", Img(name="object_-10", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("npc_-10", Img(name="npc_-10", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=""))
    images.add_image("wall_-10", Img(name="wall_-10", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset=map.tileset))
    images.add_image("object_00", Img(name="object_00", image="07", x=0,y=0,height=HEIGHT // 2,width=WIDTH // 2, tileset="")) 
    images.image["floor_-10"] = Images()

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
        if type(image) == Img and image.visible:
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
    drawn_uses = party.draw_uses(character, FAKE_SCREEN)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and character.active:
                pos = pygame.mouse.get_pos()
                if drawn_uses['close'].collidepoint(pos):
                    return action_taken
                elif drawn_uses['equip'].collidepoint(pos):
                    action = "equip"
                    party.select_item(character, action, FAKE_SCREEN, None, drawn_uses)
                    return action_taken
                elif drawn_uses['drop'].collidepoint(pos):
                    action = "drop"
                    party.select_item(character, action, FAKE_SCREEN, map, drawn_uses)
                    return action_taken
                elif drawn_uses['consume'].collidepoint(pos):
                    action = "consume"
                    party.select_item(character, action, FAKE_SCREEN, None, drawn_uses)                    
                    return action_taken
                elif drawn_uses['learn'].collidepoint(pos):
                    action = "learn"
                    party.select_item(character, action, FAKE_SCREEN, None, drawn_uses)                    
                    return action_taken
                elif drawn_uses['throw'].collidepoint(pos):
                    action = "throw"
                    party.select_item(character, action, FAKE_SCREEN, map, drawn_uses)                    
                    return action_taken
                elif drawn_uses['cast'].collidepoint(pos):
                    action = "cast"
                    item = party.select_item(character, action, FAKE_SCREEN, map, drawn_uses)
                    item.play_spell_animation(character, SCREEN, FAKE_SCREEN) 

                    return action_taken
                elif drawn_uses['repair'].collidepoint(pos):
                    print("repair")
                    return action_taken
                elif drawn_uses['enchant'].collidepoint(pos):
                    print("enchant")
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
                                    target = spell_to_cast.select_target(party, SCREEN)
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
        

def draw_object(i,x,j,y,party,map,images):
    object = map.map_grid[i][j].interaction
    direction = map.check_directions(party.p_direction, object.direction)
    try: 
        images.image[f'object_{i - x}{j - y}'].update(image=f'objects/{object.name}{object.status}_{i - x}{j - y}_{object.facing_direction(direction)}{object.tileset}')
    except KeyError:
        return

def draw_npc(i,x,j,y,party,map,images):
    entity = map.map_grid[i][j].npc
    direction = map.check_directions(party.p_direction, entity.direction)
    npc_x = i - x
    npc_y = j - y      
    try: 
        if entity.alive == False:
            images.image[f'npc_{npc_x}{npc_y}'].update(image=f'npcs/{entity.sprite}_dead')
            return
        images.image[f'npc_{npc_x}{npc_y}'].update(image=f'npcs/{entity.sprite}_{entity.facing_direction(direction)}')
    except KeyError:
        return


def draw_fog(map, party, images):
    x = party.p_position[0]
    y = party.p_position[1]


    if map.map_grid[x - 2][y].icon == 'O':
        images.image['fog_-20'].update(image=f'effects/fog_-20')
    if map.map_grid[x - 2][y - 1].icon == 'O':
        images.image['fog_-2-1'].update(image='effects/fog_-2-1')
    if map.map_grid[x - 2][y + 1].icon == 'O':
        images.image['fog_-21'].update(image='effects/fog_-21')
    


def draw_walls(map, party, images):
    for image in images.image.values():
        if type(image) is not Images:
            if image.visible:
                image.toggle()
    
    x = party.p_position[0]
    y = party.p_position[1]

    if party.p_position[0] % 2 == 0 and party.p_position[1] % 2 == 0:
        variation = '01'
    else:
        variation = '00'
    
    if map.map_grid[x][y].interaction != None and map.map_grid[x][y].interaction.name == 'pit':
        images.image['wall_-10'].update(image=f'objects/pit')
        return        

    if map.map_grid[x - 1][y].icon == 'R':
        images.image['wall_-10'].update(image=f'walls/-10_{variation}')
        return
    else:
        images.image["bg"].update(image=f'walls/bg_{variation}')

    if map.map_grid[x - 1][y - 1].icon == 'R':
        images.image['wall_-1-1'].update(image='walls/-1-1')
    if map.map_grid[x - 1][y + 1].icon == 'R':
        images.image['wall_-11'].update(image='walls/-11')

    if map.map_grid[x - 2][y].icon == 'R':
        images.image['wall_-20'].update(image='walls/-20')
    
    if images.image['wall_-20'].visible and images.image['wall_-1-1'].visible and images.image['wall_-11'].visible:
        draw_fog(map, party, images)
        return
    
    if map.map_grid[x - 2][y - 1].icon == 'R':
        images.image['wall_-2-1'].update(image='walls/-2-1')
    if map.map_grid[x - 2][y + 1].icon == 'R':
        images.image['wall_-21'].update(image='walls/-21')

    if images.image['wall_-20'].visible and images.image['wall_-21'].visible and images.image['wall_-2-1'].visible:
        draw_fog(map, party, images)
        return
    
    if map.map_grid[x - 2][y + 2].icon == 'R':
        images.image['wall_-22'].update(image='walls/-22')
    if map.map_grid[x - 2][y - 2].icon == 'R':
        images.image['wall_-2-2'].update(image='walls/-2-2')
    
    if map.map_grid[x - 3][y].icon == 'R':
        images.image['wall_-30'].update(image='walls/-30')
    if map.map_grid[x - 3][y - 1].icon == 'R':
        images.image['wall_-3-1'].update(image='walls/-3-1')
    if map.map_grid[x - 3][y + 1].icon == 'R':
        images.image['wall_-31'].update(image='walls/-31')
    if map.map_grid[x - 3][y - 2].icon == 'R':
        images.image['wall_-3-2'].update(image='walls/-3-2')
    if map.map_grid[x - 3][y + 2].icon == 'R':
        images.image['wall_-32'].update(image='walls/-32')
    
    if images.image['wall_-30'].visible and images.image['wall_-31'].visible and images.image['wall_-3-1'].visible:
        draw_fog(map, party, images)        
        return
    
    if map.map_grid[x - 4][y].icon == 'R':
        images.image['wall_-40'].update(image='walls/-40')
    
    if map.map_grid[x - 4][y - 1].icon == 'R':
        images.image['wall_-4-1'].update(image='walls/-4-1')
    if map.map_grid[x - 4][y + 1].icon == 'R':
        images.image['wall_-41'].update(image='walls/-41')
    if map.map_grid[x - 4][y + 2].icon == 'R':
        images.image['wall_-42'].update(image='walls/-42')
    if map.map_grid[x - 4][y - 2].icon == 'R':
        images.image['wall_-4-2'].update(image='walls/-4-2')

    draw_fog(map, party, images)
 
def draw_floor(i,x,j,y,party,map,images):
    loc_x = i - x
    loc_y = j - y
    if len(map.map_grid[i][j].floor) == 0:
        return

    count = 0
    for item in map.map_grid[i][j].floor:
        try: 
            height = images.image[f'npc_{loc_x}{loc_y}'].rect.height
            width = images.image[f'npc_{loc_x}{loc_y}'].rect.width
            x = images.image[f'npc_{loc_x}{loc_y}'].x_coord
            y = images.image[f'npc_{loc_x}{loc_y}'].y_coord
            print(f"{y}")
            images.image[f'floor_{loc_x}{loc_y}'].add_image(f"{count}", Img(name=f"{count}", image=f"/items/{item.floor_sprite}", x=x + item.floor_mod,y=y,height=height,width=width, tileset=""))
            count += 1
        except KeyError:
            return

def check_entities(map, party, images) -> None:
    x = party.p_position[0]
    y = party.p_position[1]

    for i in range(x - 4, x + 1): 
        for j in range(y - 2, y + 3):      
            if map.map_grid[i][j].npc != None:
                draw_npc(i, x, j, y, party, map, images)
            if map.map_grid[i][j].interaction != None:
                draw_object(i,x,j,y,party,map,images)
            if len(map.map_grid[i][j].floor) != 0:
                draw_floor(i,x,j,y,party,map,images)


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
    # check_tiles(map, party, images)
    draw_walls(map, party, images)
    check_entities(map, party, images)
    draw(map, images)
    draw_background(party)
    party.draw_inventories(FAKE_SCREEN, MY_FONT)
    TEXT_LOG.draw_log_small()
    draw_buttons(buttons)
    SCREEN.blit(pygame.transform.scale(FAKE_SCREEN, SCREEN.get_rect().size), (0, 0))
    pygame.display.update()

def draw_shift(map, party, images, buttons, inventory, screen):
    draw_walls(map, party, images)
    check_entities(map, party, images)
    draw(map, images)
    draw_background(party)
    party.draw_inventories(FAKE_SCREEN, MY_FONT)
    TEXT_LOG.draw_log_small()
    draw_buttons(buttons)
    return SCREEN.blit(pygame.transform.scale(screen, SCREEN.get_rect().size), (0, 0))



def mob_attack(mob, images, party, map, buttons, inventory):
    frame = 0
    mob.turn_mob(party)
    draw_all(map, party, images, buttons, inventory)
    images.image["npc_-10"].toggle()
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
    images.image["npc_-10"].toggle()
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
        if type(image) is Images:
            print(len(image.image))
            for imaged in image.image.values():
                imaged.visible = True
                imaged.draw(FAKE_SCREEN)
            image.image.clear()
        else:
            image.draw(FAKE_SCREEN)

        
if __name__ == "__main__":
    main()