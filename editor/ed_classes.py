import pygame
import json


class Image:
    def __init__(self, name, image, x_coord=0, y_coord=0,func=None, toggle=True):
        self.name = name
        self.toggle = toggle
        self.image = image
        self.x = x_coord
        self.y = y_coord
        self.func = func

    def draw(self, screen):
        if self.toggle:
            screen.blit(self.image, (self.x, self.y))


class Images:
    def __init__(self):
        self.images = {
            "background": Image(name="background", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/background.png"), x_coord=0, y_coord=0),
            "new": Image(name="new", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_new.png"), x_coord=9, y_coord=0, func="button"),
            "open": Image(name="open", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_open.png"), x_coord=177, y_coord=0, func="button"),
            "save": Image(name="save", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_save.png"), x_coord=346, y_coord=0, func="button"),
            "tiles": Image(name="tiles", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_tiles.png"), x_coord=514, y_coord=0, func="button"),
            "objects": Image(name="objects", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_objects.png"), x_coord=682, y_coord=0, func="button"),
            "entities": Image(name="entities", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_entities.png"), x_coord=849, y_coord=0, func="button"),
            "new_popup": Image(name="new_popup", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/popup_new.png"), x_coord=160, y_coord=155, toggle=False),
            "new_create": Image(name="new_create", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_create.png"), x_coord=172, y_coord=315, toggle=False, func="button"),
            "new_cancel": Image(name="new_cancel", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_cancel.png"), x_coord=463, y_coord=315, toggle=False, func="button"),
            "up": Image(name="up", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_up.png"), x_coord=7, y_coord=42, toggle=False, func="button"),
            "down": Image(name="down", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_down.png"), x_coord=7, y_coord=740, toggle=False, func="button"),
            "left": Image(name="left", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_left.png"), x_coord=7, y_coord=783, toggle=False, func="button"),
            "right": Image(name="right", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_right.png"), x_coord=803, y_coord=783, toggle=False, func="button"),
            "button_select": Image(name="button_select", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_select.png"), x_coord=850, y_coord=48, toggle=False, func="button"),
            "button_move": Image(name="button_move", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_move.png"), x_coord=850, y_coord=108, toggle=False, func="button"),
            "button_rotate": Image(name="button_rotate", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_rotate.png"), x_coord=850, y_coord=168, toggle=False, func="button"),
            "button_delete": Image(name="button_delete", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_delete.png"), x_coord=850, y_coord=228, toggle=False, func="button"),
            "button_floor": Image(name="button_floor", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_floor.png"), x_coord=514, y_coord=35, toggle=False, func="button"),
            "button_empty": Image(name="button_empty", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_empty.png"), x_coord=514, y_coord=70, toggle=False, func="button"),
            "button_player": Image(name="button_player", image=pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/gui/editor/button_player.png"), x_coord=514, y_coord=105, toggle=False, func="button"),
        }
    def draw_images(self, screen):
        for image in self.images.values():
            if image.name != "background":
                image.draw(screen)
    
    def draw_background(self, screen):
        self.images["background"].draw(screen)


class Map:
    def __init__(self, name):
        self.name = name
        self.grid = []
        self.create_map()
    
    def create_map(self):
        for y in range(30):
            row = []
            for x in range(30):
                if x == 0 or y == 0 or x == 29 or y == 29:
                    row.append(Tile("wall"))
                else:
                    row.append(Tile("empty"))
            self.grid.append(row)

    def rotate_map(self):
        temp_map = []
        temp_grid = []

        for i in reversed(range(len(self.grid))):
            for j in range(len(self.grid)):
                temp_grid.append(self.grid[j][i])
            temp_map.append(temp_grid)
            temp_grid = []

        self.grid = temp_map


class Tile:
    def __init__(self, type="empty"):
        self.interaction = "None"
        self.npc = "None"
        self.floor = ["None","None","None","None","None"]
        self.type = type
        self.image = None
        self.object = "None"


class Text:
    def __init__(self, name, text, x_coord=0, y_coord=0, toggle=True):
        self.name = name
        self.toggle = toggle
        self.text = text
        self.x = x_coord
        self.y = y_coord
        self.blit = None
    
    def draw_text(self, screen):
        if self.toggle:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, (0, 0, 0))
            self.blit = screen.blit(text_surface, (self.x, self.y))

class Texts:
    def __init__(self):
        self.texts = {
            "map_name": Text("map_name", "", 190, 250, False),
            "map_name_razzer": Text("map_name_razzer", f"Map Name: None", 190, 200),
            "tiles": Text("tiles", f"None", 990, 370),
            "inter": Text("interactions", f"None", 990, 445),
            "npc": Text("npc", f"None", 990, 520),
            "floor_1": Text("floor_1", f"None", 990, 597),
            "floor_2": Text("floor_2", f"None", 990, 635),
            "floor_3": Text("floor_3", f"None", 990, 675),
            "floor_4": Text("floor_4", f"None", 990, 710),
            "floor_5": Text("floor_5", f"None", 990, 750),
        }
    
    def draw_texts(self, screen):
        for text in self.texts.values():
            text.draw_text(screen)
    

class Editor:
    def __init__(self, name):
        self.font = pygame.font.Font(None, 36)
        self.name = name
        self.map = None
        self.images = Images()
        self.texts = Texts()
        self.map_x = 2
        self.map_y = 0
        self.action = None
        self.selected_action = None
        self.selected_tile = None
    
    def draw_images(self, screen):
        self.images.draw_images(screen)
    
    def draw_texts(self, screen):
        self.texts.draw_texts(screen)
    
    def draw_map(self, screen):
        if self.map is not None:
            for y, row in enumerate(self.map.grid):
                for x, tile in enumerate(row):
                    if x >= self.map_x and x <= self.map_x + 9 and y >= self.map_y and y <= self.map_y + 8:
                        if tile != None and tile == self.selected_tile:
                            color = (50, 50, 100)
                        elif tile.type == "player":
                            color = (100, 200, 100)
                        elif tile.type == "wall":
                            color = (60, 60, 60)
                        elif tile.type == "empty":
                            color = (100, 100, 100)
                        else:
                            color = (150, 150, 150)
                        tile.image = pygame.draw.rect(screen, color, (25 + (x*80) - 80 * self.map_x, 55 + (y*80) - 80 * self.map_y, 78, 78))
                        if tile.npc != "None":
                            font = pygame.font.Font(None, 36)
                            text_surface = font.render("M", True, (100, 0, 0))
                            screen.blit(text_surface, (35 + (x*80) - 80 * self.map_x, 65 + (y*80) - 80 * self.map_y, 78, 78))
                        if tile.object != "None":
                            font = pygame.font.Font(None, 36)
                            text_surface = font.render(tile.object[0].title() + tile.object[1], True, (50, 50, 0))
                            screen.blit(text_surface, (70 + (x*80) - 80 * self.map_x, 100 + (y*80) - 80 * self.map_y, 78, 78))
                        elif tile.type == "player":
                            font = pygame.font.Font(None, 36)
                            text_surface = font.render("P", True, (0, 100, 0))
                            screen.blit(text_surface, (35 + (x*80) - 80 * self.map_x, 65 + (y*80) - 80 * self.map_y, 78, 78))                            

    def select_tile(self, mouse_pos):
        if self.map is not None and self.action == "select":
            for y, row in enumerate(self.map.grid):
                for x, tile in enumerate(row):
                    if tile.image is not None and tile.image.collidepoint(mouse_pos):
                        self.selected_tile = tile
                        self.update_texts(tile)

    def load_map(self, image):
        width, height = 29,29
        with open('D:/imagine/git/games/dark_realm/Dark_Realm/maps.json', 'r') as file_m:
            M_DATA = json.load(file_m)
        for map_d in M_DATA:
            for key in map_d:
                if key == self.map.name:
                    map = map_d[key]
        for y in range(height):
            for x in range(width):
                color = image.get_at((x, y))
                if x == 0 or y == 0 or x == 29 or y == 29:
                    self.map.grid[y][x].type = "wall"
                elif color == (0, 0, 0):
                    self.map.grid[y][x].type = "empty"
                elif color == (255, 255, 255):
                    self.map.grid[y][x].type = "floor"
                elif color == (0, 255, 0):
                    self.map.grid[y][x].type = "player"
                elif color ==(0,0,255):
                    self.map.grid[y][x].type = "floor"
                    self.map.grid[y][x].npc = "Monster"
        self.map.rotate_map()
        for y in range(height):
            for x in range(width):
                for key, value in map["interactions"].items():
                    if f"{y}{x}" == key:
                        print(f"{y}{x}", key)
                        self.map.grid[y][x].object = value

    def update_texts(self, tile):
        texts = self.texts.texts
        texts["tiles"].text = tile.type
        texts["npc"].text = tile.npc
        texts["inter"].text = tile.object
        

    def save_map(self):
        grid = self.map.grid
        filename = f"{self.texts.texts["map_name"].text}.png"
        colors = {
            "empty": (0, 0, 0),
            "player": (0, 255, 0),
            "floor": (255, 255, 255),
            "wall": (0, 0, 0),
        }
        image = pygame.Surface((30, 30))
        for y in range(30):
            for x in range(30):
                tile_id = grid[x][y]
                color = colors[grid[x][y].type]
                image.set_at((x, y), color)

        pygame.image.save(image, f"D:\imagine\git\games\dark_realm\Dark_Realm\maps\{filename}")








