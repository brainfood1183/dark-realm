from fileinput import filename
from tkinter import font, filedialog

import pygame
import sys
import json
import tkinter as tk
from PIL import Image as ig
import os
from ed_classes import Image, Map, Images, Editor

# Initialize pygame
pygame.init()

# Create the window
SCREEN = pygame.display.set_mode((1200, 800))
FAKE_SCREEN = SCREEN.copy()
pygame.display.set_caption("My Pygame Window")
editor = Editor("new")
with open('D:/imagine/git/games/dark_realm/Dark_Realm/editor/editor.json', 'r') as file:
    E_DATA = json.load(file)
with open('D:/imagine/git/games/dark_realm/Dark_Realm/maps.json', 'r') as file_m:
    M_DATA = json.load(file_m)
clock = pygame.time.Clock()   # create clock
FPS = 20 
last_dir ="image"


def loadfile():
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(
        title="Open Image File",
        initialdir="D:\imagine\git\games\dark_realm\Dark_Realm\maps",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.bmp;*.png")],
    )

    return filename if filename else None



def button_match(button_name, images, texts):
    global MAP


    match button_name:
        case "new":
            print("New button action")
            images["new_popup"].toggle = True
            images["new_create"].toggle = True
            images["new_cancel"].toggle = True
            texts["map_name"].toggle = True
            input_box = pygame.Rect(175, 240, 405, 60)
            color = (100, 200, 100)
            pygame.draw.rect(SCREEN, color, input_box, 2)
            return 0
        case "open":
            file = loadfile()
            name = os.path.splitext(os.path.basename(file))[0]
            texts["map_name_razzer"].text = f"Map Name: {name}"
            images["up"].toggle = True
            images["down"].toggle = True    
            images["left"].toggle = True
            images["right"].toggle = True
            images["button_select"].toggle = True
            images["button_move"].toggle = True
            images["button_rotate"].toggle = True
            images["button_delete"].toggle = True 
            images["open"].toggle = True
            image = pygame.image.load(file).convert()
            editor.map = Map(name)          
            editor.load_map(image)
            return 1
        case "save":
            editor.save_map()
            print("Save button action")
            return 2
        case "tiles":
            images["button_floor"].toggle = True
            images["button_empty"].toggle = True
            images["button_player"].toggle = True
            print("Tiles button action")
            return 3
        case "objects":
            print("Objects button action")
            return 4 
        case "entities":
            print("Entities button action")
            return 5
        case "new_create":
            if len(texts["map_name"].text) == 0:
                print("Map name cannot be empty!")
                images["new_create"].toggle = True
                return 0
            editor.map = Map(editor.texts.texts["map_name"].text)
            texts["map_name_razzer"].text = f"Map Name: {editor.texts.texts['map_name'].text}"
            texts["map_name"].toggle = False
            images["new"].toggle = True
            images["new_create"].toggle = False
            images["new_cancel"].toggle = False
            images["new_popup"].toggle = False
            images["up"].toggle = True
            images["down"].toggle = True    
            images["left"].toggle = True
            images["right"].toggle = True
            images["button_select"].toggle = True
            images["button_move"].toggle = True
            images["button_rotate"].toggle = True
            images["button_delete"].toggle = True           

            return 6 
        case "new_cancel":
            images["new_popup"].toggle = False
            images["new"].toggle = True
            images["new_create"].toggle = False
            images["new_cancel"].toggle = False
            texts["map_name"].text = ""
            texts["map_name"].toggle = False
        case "right":
            if editor.map is not None and editor.map_x < len(editor.map.grid[0]) - 10:
                editor.map_x += 1
            images["right"].toggle = True
        case "left":
            if editor.map is not None and editor.map_x > 0:
                editor.map_x -= 1
            images["left"].toggle = True         
        case "up":
            if editor.map is not None and editor.map_y > 0:
                editor.map_y -= 1
            images["up"].toggle = True
        case "down":
            if editor.map is not None and editor.map_y < len(editor.map.grid) - 9:
                editor.map_y += 1
            images["down"].toggle = True
        case "button_select":
            editor.action = "select"
            print("Select button action")
            images["button_move"].toggle = True
            images["button_rotate"].toggle = True
            images["button_delete"].toggle = True
        case "button_move":
            editor.action = "move"
            print("Move button action")
            images["button_select"].toggle = True
            images["button_rotate"].toggle = True
            images["button_delete"].toggle = True
        case "button_rotate":
            editor.action = "rotate"
            print("Rotate button action")
            images["button_select"].toggle = True
            images["button_move"].toggle = True
            images["button_delete"].toggle = True
        case "button_delete":
            editor.action = "delete"
            print("Delete button action")
            images["button_select"].toggle = True
            images["button_move"].toggle = True
            images["button_rotate"].toggle = True
        case "button_floor":
            if editor.selected_tile is not None:
                editor.selected_tile.type = "floor"
            images["button_empty"].toggle = False   
            images["button_player"].toggle = False
            images["tiles"].toggle = True
        case "button_empty":
            if editor.selected_tile is not None:
                editor.selected_tile.type = "empty"
            images["button_floor"].toggle = False
            images["button_player"].toggle = False
            images["tiles"].toggle = True
        case "button_player":
            if editor.selected_tile is not None:
                editor.selected_tile.type = "player"
            images["button_floor"].toggle = False
            images["button_empty"].toggle = False
            images["tiles"].toggle = True
        case _:
            print("No button action")
            return -1


def main():
    # Main loop
    running = True
    choice = None
    active = False
    text = ""
    while running:
        for event in pygame.event.get():
            # Detect clicking the X button
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for image in editor.images.images.values():
                    if image.func == "button" and image.x <= mouse_pos[0] <= image.x + image.image.get_width() and image.y <= mouse_pos[1] <= image.y + image.image.get_height() and image.toggle:
                        image.toggle = False
                        choice = button_match(image.name, editor.images.images, editor.texts.texts)
                editor.select_tile(mouse_pos)


            elif event.type == pygame.KEYDOWN and choice == 0:


                if event.key == pygame.K_RETURN:
                    editor.map = Map(editor.texts.texts["map_name"].text)
                    editor.texts.texts["map_name_razzer"].text = f"Map Name: {editor.texts.texts['map_name'].text}"
                    editor.texts.texts["map_name"].text = ""
                    editor.texts.texts["map_name"].toggle = False
                    editor.images.images["new"].toggle = True
                    editor.images.images["new_create"].toggle = False
                    editor.images.images["new_cancel"].toggle = False
                    editor.images.images["new_popup"].toggle = False
                    choice = None

                elif event.key == pygame.K_BACKSPACE:
                    editor.texts.texts["map_name"].text = editor.texts.texts["map_name"].text[:-1]

                else:
                    if len(editor.texts.texts["map_name"].text) < 10:
                        if event.unicode.isalnum() or event.unicode in [' ', '_']:
                            editor.texts.texts["map_name"].text += event.unicode


        # Blit the background image
        editor.images.draw_background(SCREEN)
        if editor.map is not None:
            editor.draw_map(SCREEN)
        editor.draw_images(SCREEN)
        editor.draw_texts(SCREEN)

        if choice == 0:
            editor.texts.texts["map_name"].draw_text(SCREEN)



        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()