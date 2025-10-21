from PIL import Image
from colored import Back, Fore, Style
import random
import json
import pygame
import sys


class Npc:
    def __init__(self, multi):
        with open('D:/imagine/git/games/dark_realm/Dark_Realm/npcs.json', 'r') as file:
            data = json.load(file)
        monster = random.choice(data)
        self.alive = True
        self.status = []
        self.name = monster["name"]
        self.sprite = monster["sprite"]
        self.s_attack = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{monster["s_attack"]}.png")
        self.s_death = monster["s_death"]
        self.health = monster["max_health"]
        self.tough = monster["toughness"]
        self.attack_type = monster["attack_type"]
        self.health_max = monster["max_health"]
        self.damage = monster["damage"]
        self.spells = monster["spells"]
        self.width = monster["width"] * multi
        self.height = monster["height"] * multi
        self.a_frames = monster["a_frames"] # number of frames of attack animation.
        self.a_speed = monster["a_speed"] # speed of attack animation.
        self.reward = monster["reward"]
        self.gold = monster["gold"]
        self.direction = "S"
        self.acted = False
    
    def __str__(self):
        return f"{self.name}"

    def check_status(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def attack(self, party, log):
        modifier = 0
        if 'splash' in self.attack_type:
            for character in party:
                d_value = str(self.damage - character.tough)[1::]
                character.loss_of_health(self.damage)
                log.add_to_log(f"{self.name} hits {character.p_name} for {d_value}!", (120,0,0))
            return
        select_victim = True
        while select_victim:
            character = random.choice(party.p_members)
            if character.alive:
                select_victim = False
                d_value = str(self.damage + character.tough)[1::]
        if "block" in character.status:
            modifier = self.damage // 2
            character.status.remove("block")
        character.modify_health(self.damage - modifier)
        log.add_to_log(f"{self.name} hits {character.p_name} for {d_value}!", (120,0,0))
        if 'poison' in self.attack_type:
            character.poison(abs(int(self.damage - modifier // 2)))
        if 'disease' in self.attack_type and "diseased" not in character.status:
            number = random.randint(0, 5)
            if number == 3:
                character.status.append("diseased")
                character.update_damage()
                log.add_to_log(f"{character.p_name} is diseased!", (150,0,0))

    def modify_health(self, h_modifier):
        self.health = self.health + h_modifier
        self.check_status()
    
    def play_animation(self, frame, width, height, SCREEN, animation, multi):
        h = animation.get_height()
        w = animation.get_width()
        animation = pygame.transform.scale(animation, (w * multi, h * multi))
        SCREEN.blit(animation, (140 * multi,120 * multi), (((width * round(frame)) * multi),0, width * multi,height * multi))
    
    def turn_mob(self,party):
        directions = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }
        self.direction = directions[party.p_direction]


class Interaction:
    def __init__(self, name, direction, target, tileset):
        with open('D:/imagine/git/games/dark_realm/Dark_Realm/inter.json', 'r') as file:
            data = json.load(file)
        obj = data[0][name]
        self.name = name
        self.action = obj["action"]
        self.toggle = obj["toggle"]
        self.type = obj["type"]
        self.ai_blocker = obj["ai_blocker"]
        self.party_blocker = obj["party_blocker"]
        self.status = self.toggle[0]
        self.tileset = ""
        self.direction = None
        self.distance = obj["distance"]
        if obj["has_tileset"]:
            self.tileset = tileset
        if direction != "Q": 
            self.direction = direction
        self.target = target

    def toggle_sprite(self):
        if self.status == self.toggle[0]:
            self.status = self.toggle[1]
        else:
            self.status = self.toggle[0]
        if self.target.interaction.type == "door":
            self.target.interaction.toggle_blockers()

    
    def toggle_blockers(self):
        if self.ai_blocker == True:
            self.ai_blocker = False
        else:
            self.ai_blocker = True
        if self.party_blocker == True:
            self.party_blocker = False
        else:
            self.party_blocker = True
        

    def interact(self):
        if self.action == None:
            return
        if self.target.interaction.status == self.target.interaction.toggle[0]:
            self.target.interaction.status = self.target.interaction.toggle[1]
            if self.target.interaction.name == "wall":
                self.target.icon = "O"
                self.target.npc = None
        else:
            self.target.interaction.status = self.target.interaction.toggle[0]
            if self.target.interaction.name == "wall":
                self.target.icon = "R"
        self.toggle_sprite()
    
    def pit_fall(self, party):
        for character in party.p_members:
            character.modify_health(-character.health)


class Tile:
    def __init__(self, icon, colour, npc, interaction):
        self.icon = icon
        self.colour = colour
        self.npc = npc
        self.interaction = interaction
        self.floor = []
        self.i = 0
        self.j = 0


class Item:
    def __init__(self, name):
        with open('D:/imagine/git/games/dark_realm/Dark_Realm/items.json', 'r') as file:
            data = json.load(file)
        item = data[name]
        self.name = item['name']
        self.type = item['type']
        self.animation = item['use_anim']
        self.icon = item['icon_sprite']
        self.floor_sprite = item['floor_sprite']
        self.weapon = False
        self.consumable = item['consume']
        if self.type == 'weapon':
            self.weapon = True
            self.damage = item['attack_damage']
        self.special = item['special']
        self.req = item['requirement']
        self.req_val = item['requirement_amount']
        self.durability = item['durability']
        self.value = item['value']
        if self.type == "clothing":
            self.ac = item['ac']
            self.location = item['location']
            self.worn_sprite = f"item_worn_{item['worn']}"

    
    def special_attack(self):
        if self.special == None:
            return
    
    def check_durability(self, character):
        if self.durability <= 0:
            self.durability = 0
            character.weapon = Item(character.default_attack)
            character.attack_animation = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.weapon.animation}{character.style}.png")


class Races:
    def __init__(self):
        self.all_races = {
            "human": Race(name="Human", strength=0, dexterity=0,charisma=1, intelligence=0, toughness=0, wisdom=0, default_attack="fists"),
            "dwarf": Race(name="Dwarf", strength=1, dexterity=-1,charisma=0, intelligence=0, toughness=1, wisdom=0, default_attack="fists"),
            "elf": Race(name="Elf", strength=0, dexterity=1,charisma=0, intelligence=1, toughness=-1, wisdom=2, default_attack="fists"),
            "anoran": Race(name="Anoran", strength=-1, dexterity=2,charisma=-1, intelligence=2, toughness=-1, wisdom=3, default_attack="fists"),
            "halforc": Race(name="Half Orc", strength=2, dexterity=0,charisma=-2, intelligence=-1, toughness=2, wisdom=-1, default_attack="fists"),
            "gnome": Race(name="Gnome", strength=-1, dexterity=2,charisma=1, intelligence=1, toughness=2, wisdom=1, default_attack="fists"),
            "tigris": Race(name="Tigris", strength=-1, dexterity=2,charisma=0, intelligence=0, toughness=3, wisdom=2, default_attack="claws"),
        }
    def select_race(self, race):
        return self.all_races[race]


class Race:
    def __init__(self, name, strength, dexterity, charisma, intelligence, toughness, wisdom, default_attack):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.charisma = charisma
        self.default_attack = default_attack
        self.intelligence = intelligence
        self.toughness = toughness
        self.description = ""
        self.wisdom = wisdom


class Spell:
    def __init__(self, name):
        with open('D:/imagine/git/games/dark_realm/Dark_Realm/spells.json', 'r') as file:
            data = json.load(file)
        spell = data[name]
        self.name = spell["name"]
        self.icon = spell["spell_icon"]
        self.target_type = spell["target_type"]
        self.description_1 = spell["description_1"]
        self.description_2 = spell["description_2"]
        self.description_3 = spell["description_3"]
        self.target_health_modifier = spell["target_health_modifier"]
        self.caster_health_modifier = spell["caster_health_modifier"]
        self.caster_mana_modifier = spell["caster_mana_modifier"]
        self.spell_type = spell["spell_type"]
        self.target_status = spell["target_status"]
        self.caster_status = spell["caster_status"]
        if self.target_type == "summon":
            self.summon = spell["summon"]
        self.animation = spell["cast_animation"]
        self.cast_animation = ""
    
    def set_cast(self, style):
        self.cast_animation = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{self.animation}_01.png")        
    

    def play_spell_animation(self, character, SCREEN, FAKE_SCREEN):
        frame = 0
        while frame <= 5:
            animation_screen = FAKE_SCREEN.copy()
            character.play_animation(SCREEN=animation_screen, width=500, height=500, frame=round(frame), animation=pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{self.animation}_01.png"))
            SCREEN.blit(pygame.transform.scale(animation_screen, SCREEN.get_rect().size), (0, 0))
            pygame.display.update()
            frame += 0.07  

    def select_target(self, party, caster, spell, r_screen):
        screen = party.screen
        target = None
        background = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/select_target.png")
        background_x = pygame.transform.scale(pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/close.png"), (30 * party.multi, 30 * party.multi))
        screen.blit(pygame.transform.scale(background, (background.get_width() * 1.5 * party.multi, background.get_height() * 1.5 * party.multi)), (100 * party.multi, 300 * party.multi))
        text_title = party.name_font.render(f'Select Target', False, (0, 0, 0))
        text_title_rect = text_title.get_rect()
        text_title_rect.center = (210 * party.multi, 325 * party.multi)
        screen.blit(text_title, text_title_rect)
        portraits = []
        no_target = True
        x_modifier = 0
        y_modifier = 0
        close = screen.blit(background_x, (310 * party.multi,570 * party.multi))
        for character in party.p_members:
            if x_modifier > (112 * party.multi):
                x_modifier = 0
                y_modifier = 120 * party.multi
            portrait = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.p_portrait}.png")
            text_health = party.name_font.render(f'{character.health}/{character.health_max}', False, (0, 0, 0))
            text_health_rect = text_health.get_rect()
            text_health_rect.center = (( 160 * party.multi) + x_modifier, (453 * party.multi) + y_modifier)
            portrait = screen.blit(pygame.transform.scale(portrait, ((portrait.get_width() * 1.45) * party.multi, (portrait.get_height() * 1.45) * party.multi)), ((116 * party.multi) + x_modifier, (350 * party.multi) + y_modifier))
            portraits.append(portrait)
            screen.blit(text_health, text_health_rect)
            x_modifier += 112 * party.multi             
        while no_target:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(portraits)):
                        if portraits[i].collidepoint(pos):
                            target = party.p_members[i]
                            no_target = False
                        if close.collidepoint(pos):
                            return target
                    

            r_screen.blit(pygame.transform.scale(screen, r_screen.get_rect().size), (0, 0))
            pygame.display.update()
        return target
            
                   

        

    def cast_spell(self, target, caster, party, map):
        if caster.mana + self.caster_mana_modifier < 0:
            party.log.add_to_log(f"{caster.p_name} fails to cast {self.name}, not enough mana!", (85,19,194))
            return
        if self.target_type == "mob" or self.target_type == "party_m":
            if target == None:
                party.log.add_to_log(f"{caster.p_name} fails to cast {self.name}, no  target!", (85,19,194))
                return
            target.modify_health(self.target_health_modifier)
            if self.target_type == "party_m":
                party.log.add_to_log(f"{caster.p_name} casts {self.name} on {target.p_name} for {abs(int(self.target_health_modifier))}!", (85,19,194))
            else:
                party.log.add_to_log(f"{caster.p_name} casts {self.name} on {target.name} for {abs(int(self.target_health_modifier))}!", (85,19,194))               
            if self.target_status != None:
                target.status_effect(self.caster_status[1], self.caster_status[0])
        elif self.target_type == "party":
            for character in party.p_members:
                if character != caster:
                    character.modify_health(self.caster_health_modifier)
                if self.caster_status != None:
                    character.status_effect(self.caster_status[1], self.caster_status[0])
            modified_health = ""
            if self.caster_health_modifier > 0:
                modified_health = f" for {abs(int(self.caster_health_modifier))}"
            party.log.add_to_log(f"{caster.p_name} casts {self.name} on party{modified_health}!", (85,19,194))
        if self.caster_status != None:
            character.status_effect(self.caster_status[1], self.caster_status[0])            
        caster.modify_mana(self.caster_mana_modifier)
        caster.modify_health(self.caster_health_modifier)
        if self.target_type == "summon" and caster.alive and len(party.p_members) < 4:
            with open('D:/imagine/git/games/dark_realm/Dark_Realm/summons.json', 'r') as file:
                data = json.load(file)   
            summon = data[self.name]
            party.log.add_to_log(f"{caster.p_name} summons a {self.summon}!", (85,19,194))
            party.add_new_member(summon)


class Classes:
    def __init__(self):
        self.all_classes = {
            "assassin": Char_Class(name="Assassin", weapon="katana", spells=[], abilities=[],helmet=None, chest=None, strength=4, dexterity=4, charisma=0, intelligence=1, toughness=2, wisdom=1),
            "barbarian": Char_Class(name="Barbarian", weapon="axe", spells=[], abilities=["berserk"],helmet="horned", chest=None, strength=5, dexterity=3, charisma=0, intelligence=0, toughness=2, wisdom=0),
            "cleric": Char_Class(name="Cleric", weapon="dagger", spells=["spurt", "heal", "magic_arrow"], abilities=[],helmet=None, chest=None, strength=2, dexterity=2, charisma=1, intelligence=3, toughness=1, wisdom=3),
            "druid": Char_Class(name="Druid", weapon="staff", spells=["spurt", "heal", "amber_spear"], abilities=[],helmet=None, chest=None, strength=1, dexterity=3, charisma=1, intelligence=3, toughness=1, wisdom=4),
            "enchanter": Char_Class(name="Enchanter", weapon=None, spells=["blind", "health_to_mana", "mind_blast"], abilities=[],helmet=None, chest="robe", strength=0, dexterity=1, charisma=2, intelligence=5, toughness=2, wisdom=2),
            "fighter": Char_Class(name="Fighter", weapon="sword", spells=[], abilities=[],helmet="bascinet", chest="leather_armor", strength=5, dexterity=3, charisma=1, intelligence=1, toughness=1, wisdom=1),
            "guardian": Char_Class(name="Guardian", weapon="sword", spells=[], abilities=["guard"],helmet="bascinet", chest="splint mail", strength=3, dexterity=2, charisma=1, intelligence=1, toughness=4, wisdom=1),
            "healer": Char_Class(name="Healer", weapon="cudgel", spells=["cure", "heal"], abilities=["meditate"],helmet=None, chest=None, strength=1, dexterity=2, charisma=2, intelligence=4, toughness=0, wisdom=3),
            "illusionist": Char_Class(name="Illusionist", weapon="staff", spells=["lesser_heal", "distract", "blind"], abilities=[],helmet=None, chest=None, strength=1, dexterity=2, charisma=2, intelligence=3, toughness=0, wisdom=4),
            "jester": Char_Class(name="Jester", weapon=None, spells=["laugh_of_damnation", "distract"], abilities=[],helmet="jester hat", chest=None, strength=2, dexterity=2, charisma=4, intelligence=2, toughness=0, wisdom=2),
            "knight": Char_Class(name="Knight", weapon="great sword", spells=[], abilities=[],helmet=None, chest="chainmail", strength=4, dexterity=2, charisma=2, intelligence=1, toughness=2, wisdom=1),
            "lancer": Char_Class(name="Lancer", weapon="spear", spells=[], abilities=[],helmet=None, chest="leather armor", strength=3, dexterity=3, charisma=0, intelligence=2, toughness=2, wisdom=2),
            "magician": Char_Class(name="Magician", weapon="staff", spells=["spurt", "fireball", "heal"], abilities=[],helmet=None, chest="robe", strength=0, dexterity=1, charisma=1, intelligence=6, toughness=0, wisdom=4),
            "necromancer": Char_Class(name="Necromancer", weapon="staff", spells=["curse", "life_leech", "summon skeleton"], abilities=[],helmet=None, chest="robe", strength=0, dexterity=1, charisma=1, intelligence=6, toughness=0, wisdom=4),
            "paladin": Char_Class(name="Paladin", weapon="mace", spells=["lesser_heal", "holy_light"], abilities=[],helmet="barbute", chest="splint mail", strength=3, dexterity=2, charisma=3, intelligence=3, toughness=2, wisdom=0),
            "quarrelist": Char_Class(name="Quarrelist", weapon="dagger", spells=["distract"], abilities=["barter"],helmet="leather helm", chest=None, strength=2, dexterity=2, charisma=4, intelligence=2, toughness=1, wisdom=1),
            "rogue": Char_Class(name="Rogue", weapon="bow", spells=["invisibility"], abilities=[],helmet=None, chest="boiled leather armor", strength=2, dexterity=4, charisma=1, intelligence=2, toughness=2, wisdom=1),
            "sorcerer": Char_Class(name="Sorcerer", weapon=None, spells=["spurt", "lesser heal", "energy bolt"], abilities=[],helmet=None, chest="robe", strength=1, dexterity=1, charisma=0, intelligence=5, toughness=0, wisdom=5),
            "thief": Char_Class(name="Thief", weapon="dagger", spells=[], abilities=["steal","stealth"],helmet=None, chest=None, strength=1, dexterity=3, charisma=1, intelligence=2, toughness=2, wisdom=3),
            "undying": Char_Class(name="Undying", weapon="staff", spells=["summon_skeleton", "heal", "energy_bolt", "summon_blood_golem", "healing_aura", "mass_cure"], abilities=["meditate","resurrection"],helmet="helm of undying", chest="robe", strength=2, dexterity=2, charisma=0, intelligence=20, toughness=4, wisdom=2),
            "vagabond": Char_Class(name="Vagabond", weapon="club", spells=[], abilities=["begging"],helmet=None, chest=None, strength=2, dexterity=2, charisma=2, intelligence=2, toughness=2, wisdom=2),
            "warlock": Char_Class(name="Warlock", weapon="staff", spells=["spurt", "lesser_heal", "eldritch blast"], abilities=[],helmet=None, chest="robe", strength=1, dexterity=0, charisma=2, intelligence=5, toughness=0, wisdom=4),
            "xar": Char_Class(name="Follower Of Xar", weapon="none", spells=["spurt", "lesser_heal", "summon demonblade"], abilities=[],helmet="bascinet", chest="robe", strength=2, dexterity=2, charisma=2, intelligence=2, toughness=2, wisdom=2),
            "yithian": Char_Class(name="Yithian", weapon="dagger", spells=["heal", "eldritch_blast"], abilities=[],helmet="bascinet", chest="robe", strength=2, dexterity=2, charisma=2, intelligence=2, toughness=2, wisdom=2),
            "zealot": Char_Class(name="Zealot", weapon="cudgel", spells=["spurt", "immolate"], abilities=["meditate"],helmet=None, chest="robe", strength=2, dexterity=2, charisma=0, intelligence=2, toughness=3, wisdom=3),
            "skeleton": Char_Class(name="Skeleton", weapon="sword", spells=[], abilities=["poison_immune", "undead"],helmet=None, chest=None, strength=2, dexterity=2, charisma=0, intelligence=0, toughness=0, wisdom=0),
            "bloodg": Char_Class(name="Blood Golem", weapon="fists", spells=[], abilities=[],helmet=None, chest=None, strength=10, dexterity=1, charisma=0, intelligence=0, toughness=3, wisdom=0),
        }

    def select_class(self, class_chosen):
        return self.all_classes[class_chosen]


class Char_Class:
    def __init__(self, name, weapon, spells, abilities, helmet, chest, strength, dexterity, charisma, intelligence, toughness, wisdom):
        self.name = name
        self.weapon = weapon
        self.spells = spells
        self.abilities = abilities
        self.helmet = helmet
        self.chest = chest
        self.strength = strength
        self.dexterity = dexterity
        self.charisma = charisma
        self.intelligence = intelligence
        self.toughness = toughness
        self.wisdom = wisdom
        self.description = ""


class Character:
    def __init__(self, name, portrait, style, race, class_chosen, races, classes, multi, log):
        self.log = log
        self.p_name = name
        self.multi = multi
        self.p_portrait = portrait
        self.char_race = races.all_races[race]
        self.char_class = classes.all_classes[class_chosen]
        self.p_class = self.char_class.name
        self.default_attack = self.char_race.default_attack
        self.str = self.char_class.strength + self.char_race.strength
        self.dex = self.char_class.dexterity + self.char_race.dexterity
        self.int = self.char_class.intelligence + self.char_race.intelligence
        self.wis = self.char_class.wisdom + self.char_race.wisdom
        self.tough = self.char_class.toughness + self.char_race.toughness
        self.char = self.char_class.charisma + self.char_race.charisma
        self.health_max = 30 + int((self.str // 2 + self.tough) * 10)
        self.mana_max = 5 + int(((self.int // 2 + self.wis) * 10))
        self.style = style
        self.p_portrait_dead = f"portrait_dead_{self.char_race.name}"
        self.health = self.health_max
        self.mana = self.mana_max
        self.status = []
        self.abilities = self.char_class.abilities
        self.spells = []
        self.inventory = []
        self.poison_tick = 0
        self.alive = True
        self.chest = None
        self.head = None
        self.boots = None
        for spell in self.char_class.spells:
            self.spells.append(Spell(spell))
        self.missing_health = (((self.health_max - self.health) / self.health_max) * 62)  * self.multi
        self.missing_mana = (((self.mana_max - self.mana) / self.mana_max) * 62)  * self.multi
        if self.char_class.weapon != None:
            self.weapon = Item(self.char_class.weapon)
        else:
            self.weapon = Item("fists")
        if self.char_class.chest != None:
            self.chest = Item(self.char_class.chest)       
        self.attack_animation = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{self.weapon.animation}{self.style}.png")
        self.block_animation = pygame.image.load("D:/imagine/git/games/dark_realm/Dark_Realm/images/block_01.png")
        self.active = False
        self.damage = self.weapon.damage + self.str
    
    def attack(self, mob):
        if self.weapon.durability == 0 or mob.alive == False:
            return 
        text_alive = ""   
        mob.health -= self.damage - mob.tough
        if mob.health <= 0:
            text_alive = f" killing it"
        self.log.add_to_log(f"{self.p_name} hits {mob.name} for {self.damage - mob.tough}{text_alive}!", (164,100,20))  
        self.weapon.durability -= mob.tough   

    def play_animation(self, frame, width, height, SCREEN, animation):
        h = animation.get_height()
        w = animation.get_width()
        animation = pygame.transform.scale(animation, (w * self.multi, h * self.multi))
        SCREEN.blit(animation, (0,0), (((width * round(frame)) * self.multi),0, width * self.multi,height * self.multi))
    
    def modify_health(self, value):
        self.health += value
        if self.health <= 0:
            self.alive = False
            self.health = 0
            if self.p_name != "Skeleton":
                self.log.add_to_log(f"{self.p_name} has died!", (150,0,0))
        if self.health > self.health_max:
            self.health = self.health_max
        self.missing_health = (((self.health_max - self.health) / self.health_max) * 62) * self.multi

    def modify_mana(self, value):
        self.mana += value
        if self.mana <= 0:
            self.mana = 0
        self.missing_mana = (((self.mana_max - self.mana) / self.mana_max) * 62) * self.multi
    
    def update_damage(self):
        modifier = 0
        if "diseased" in self.status:
            modifier += -2
        if "berserk" in self.status:
            modifier += self.str

        self.damage = self.weapon.damage + self.str + modifier

    def poison(self, damage):
        if damage <= 0 or "poison_immune" in self.abilities:
            return
        if "poisoned" in self.status:
            self.poison_tick += damage
        else:
            self.status.append("poisoned")
            self.poison_tick = damage
            self.log.add_to_log(f"{self.p_name} had been poisoned!", (200,0,0))
        if self.poison_tick + (self.health_max - self.health) > self.health_max:
            self.poison_tick = self.poison_tick - ((self.poison_tick + (self.health_max - self.health)) - self.health_max)
     
    def poison_tick_down(self):
        if "poisoned" not in self.status:
            return
        if self.alive != True:
            self.status = []
            self.poison_tick = 0
        if "poisoned" in self.status and self.poison_tick <= 0:
            self.status.remove("poisoned")
            self.poison_tick = 0
        else:
            if self.health == 1:
                self.poison_tick = 0
                self.status.remove("poisoned")
                return
            self.poison_tick -= 1.1
            self.modify_health(-1)

    def status_effect(self, status, action):
        if action == "r" and status in self.status:
            self.status.remove(status)
        elif action == "a" and status not in self.status:
            self.status.append(status)


class Button:
    def __init__(self, x, y, image, visible):
        self.x = x
        self.y = y
        self.visible = visible
        self.default = self.visible
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.height = self.rect.height
        self.rect.width = self.rect.width
        self.rect.topleft = (x,y)
    
    def draw(self, SCREEN, MULTI):
        if self.visible:
            SCREEN.blit(pygame.transform.scale(self.image, (self.rect.width * MULTI, self.rect.height * MULTI)), (self.rect.x, self.rect.y))
  
    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
    
    def reset(self):
        self.visible = self.default


class Buttons:
    def __init__(self):
        self.button = {}

    def add_button(self, button_name, button):
        self.button[button_name] = button


class Img:
    def __init__(self, image, x, y, height, width, name, tileset):
        self.image = image
        self.name = name
        self.tileset = tileset
        self.visible = False
        self.image_live = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{self.image}{self.tileset}.png").convert_alpha()
        self.x_coord = x
        self.y_coord = y
        self.height = height
        self.width = width
        self.rect = self.image_live.get_rect()
        self.rect.topleft = (x,y)
        self.rect.height = height
        self.rect.width = width
    
    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
    
    def move(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.rect.topleft = (x,y)      

    
    def update(self, image):
        self.image = image
        self.image_live = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{self.image}{self.tileset}.png").convert_alpha()
        self.visible = True
    
    def update_advanced(self, image, height, width):
        self.image = image
        self.height = height
        self.width = width
        self.image_live = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{self.image}{self.tileset}.png").convert_alpha()
        self.visible = True
        
    def change_coords(self, x, y):
        self.x_coord = self.x_coord + x
        self.y_coord = self.y_coord + y

    def draw(self, SCREEN):
        if self.visible:
            img = pygame.transform.scale(self.image_live, (self.width, self.height))
            SCREEN.blit(img, (self.x_coord, self.y_coord))


class Images:
    def __init__(self):
        self.image = {}
    
    def add_image(self, image_name, img):
        self.image[image_name] = img


class Party:
    def __init__(self, SCREEN, MULTI, log):
        self.races = Races()
        self.log = log
        self.multi = MULTI
        self.name_font = pygame.font.SysFont('Comic Sans MS', int(18 * self.multi))
        self.classes = Classes()
        self.screen = SCREEN
        self.p_position = [0,0]
        self.p_direction = 'N'
        self.p_members = [Character(name="Brainfood", portrait="portrait_1", style='00', race="human", class_chosen="undying", races=self.races, classes=self.classes, multi=self.multi, log=self.log),Character(name="Bob", portrait="portrait_2", style='01', race="human", class_chosen="fighter", races=self.races, classes=self.classes, multi=self.multi, log=self.log), Character(name="Brainfood", portrait="portrait_5", style='00', race="human", class_chosen="barbarian", races=self.races, classes=self.classes, multi=self.multi, log=self.log)]
        self.inventories = []
        for i in range(len(self.p_members)):
            self.inventories.append(Inventory(self.p_members[i], self.screen, str(i), self.multi))
        self.inventory = []


    def add_new_member(self, new_character):
        if len(self.p_members) >= 4:
            return
        values = ['0','1','2','3']
        for inventory in self.inventories:
            value = inventory.value
            if inventory.value in values:
                values.remove(inventory.value)
        value = random.choice(values)
        self.p_members.append(Character(name=new_character["name"], portrait=new_character["portrait"], style=new_character["style"], race=new_character["race"], class_chosen=new_character["class"], races=self.races, classes=self.classes, multi=self.multi, log=self.log))
        self.inventories.append(Inventory(self.p_members[len(self.p_members) - 1], self.screen, str(value), self.multi))
        self.log.add_to_log(text=f"{new_character["name"]} has joined your party!", color=(0,200,0))


    def move_direction(self, party, direction, map): 
        self.move_party(map, direction)
        action_taken = True
        movement = True
        party.check_poison()
        return action_taken, movement


    def shift_order(self):
        if len(self.inventories) == 1:
            return
        temp = None
        new_list = []
        for i in range(len(self.inventories)):
            if i == 0:
                temp = self.inventories[i]
            else:
                new_list.append(self.inventories[i])     
        new_list.append(temp)
        self.inventories = new_list
        if self.p_members[0] != self.inventories[0].owner:
            self.log.add_to_log(text=f"{self.inventories[0].owner.p_name}'s turn to take an action!", color=(0,0,100))


    def choose_inventory(self, item):
        for character in self.p_members:
            if len(character.inventory) < 4:
                character.inventory.append(item)
                self.log.add_to_log(text=f"{character.p_name} picks up {item.name}", color=(0,0,100))
                return
        self.log.add_to_log(text=f"Inventory is full!", color=(100,0,0)) 
        return      
            

    def rotate_party(self, direction):
        directions = ['N','E','S', 'W']
        if direction == 'q':
            distance = -1
        else:
            distance = 1
        index = directions.index(self.p_direction) + distance
        if index > len(directions) - 1:
            index = 0
        elif index < 0:
            index = len(directions) - 1
        self.p_direction = directions[index]
        direction_string = {
            'N': "North",
            'E': "East",
            'S': "South",
            'W': "West",
        }
        self.log.add_to_log(text=f"Party turned to face {direction_string[self.p_direction]}!", color=(0,0,100))


    def move_party(self, map, direction):
        i = self.p_position[0] 
        j = self.p_position[1]
        movement = ""
        if direction == 'w':
            i -= 1
            movement = "steps forward"
        elif direction == 's':
            i += 1
            movement = "steps backwards"
        elif direction == 'a':
            j -= 1
            movement = "sidesteps left"
        else:
            j += 1
            movement = "sidesteps right"
        if map.map_grid[i][j].icon != 'O' or map.map_grid[i][j].npc != None and map.map_grid[i][j].npc.alive == True or map.map_grid[i][j].interaction != None and map.map_grid[i][j].interaction.party_blocker == True:
            return
        map.map_grid[self.p_position[0]][self.p_position[1]].icon = 'O'
        map.map_grid[self.p_position[0]][self.p_position[1]].colour = Fore.black
        map.map_grid[i][j].icon = 'P'
        map.map_grid[i][j].colour = Fore.green
        self.p_position = [i,j]
        self.log.add_to_log(text=f"Party {movement}!", color=(0,0,100))
    

    def check_poison(self):
        for character in self.p_members:
            if "poisoned" in character.status:
                character.poison_tick_down()


    def draw_inventories(self, SCREEN, MY_FONT):
        y_modifier = 0
        compass = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/compass_{self.p_direction}.png")
        SCREEN.blit(pygame.transform.scale(compass, (compass.get_width() * self.multi, compass.get_height() * self.multi)), (20 * self.multi, 555 * self.multi))        

        for i in reversed(range(len(self.inventories))):
            character = self.inventories[i].owner
            SCREEN.blit(self.inventories[i].inventory_screen, (647 * self.multi, (235 * self.multi) + y_modifier))
            if character.alive:
                portrait = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.p_portrait}.png")
            else:
                portrait = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.p_portrait_dead}.png")               
            portrait = pygame.transform.scale(portrait, (60 * self.multi, 60 * self.multi))
            SCREEN.blit(portrait, (653 * self.multi, (482 * self.multi) + y_modifier))   
            self.draw_inventory(character, y_modifier, SCREEN)
            self.draw_bars(y_modifier, SCREEN, character)    
            if self.inventories[i] == self.inventories[0]:
                SCREEN.blit(self.inventories[i].paper_doll, (720 * self.multi, (280 * self.multi) + y_modifier))  
                if character.weapon.name != "Fists":
                    weapon = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.weapon.icon}.png")
                    SCREEN.blit(pygame.transform.scale(weapon,(weapon.get_width() * self.multi, weapon.get_height() * self.multi)), (662 * self.multi, (361 * self.multi) + y_modifier))
                if character.chest != None:
                    chest = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.chest.icon}.png")
                    SCREEN.blit(pygame.transform.scale(chest,(chest.get_width() * self.multi, chest.get_height() * self.multi)), (804 * self.multi, (359 * self.multi) + y_modifier))  
                    chest_worn = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{character.chest.worn_sprite}.png")
                    SCREEN.blit(pygame.transform.scale(chest_worn, (chest_worn.get_width() * self.multi, chest_worn.get_height() * self.multi)), (719 * self.multi, (315 * self.multi) + y_modifier))                 
                self.draw_texts(y_modifier,SCREEN, character)                 
            y_modifier += -73 * self.multi
    

    def draw_texts(self, y_modifier,SCREEN, character):
        stat_font = pygame.font.SysFont('arialblold', int(16 * self.multi))
        text_name = self.name_font.render(f'{character.p_name}', False, (0, 0, 0))
        text_name_rect = text_name.get_rect()
        text_name_rect.center = (755 * self.multi, (260 * self.multi) + y_modifier)
        SCREEN.blit(text_name, text_name_rect)  
        text_class = stat_font.render(f'{character.p_class}', False, (0, 0, 0)) 
        SCREEN.blit(text_class, (880 * self.multi, (285 * self.multi) + y_modifier))    
        text_str = stat_font.render(f'strength:  {character.str}', False, (0, 0, 0)) 
        SCREEN.blit(text_str, (880 * self.multi, (297 * self.multi) + y_modifier))    
        text_dex = stat_font.render(f'dexterity:  {character.dex}', False, (0, 0, 0)) 
        SCREEN.blit(text_dex, (880 * self.multi,(309 * self.multi) + y_modifier))           
        text_int = stat_font.render(f'intelligence:  {character.int}', False, (0, 0, 0)) 
        SCREEN.blit(text_int, (880 * self.multi, (321 * self.multi)  + y_modifier))  
        text_char = stat_font.render(f'charisma:  {character.char}', False, (0, 0, 0)) 
        SCREEN.blit(text_char, (880* self.multi, (333 * self.multi) + y_modifier))
        text_wis = stat_font.render(f'wisdom:  {character.wis}', False, (0, 0, 0)) 
        SCREEN.blit(text_wis, (880 * self.multi, (345 * self.multi) + y_modifier))
        text_tgh = stat_font.render(f'toughness:  {character.tough}', False, (0, 0, 0)) 
        SCREEN.blit(text_tgh, (880 * self.multi, (357 * self.multi) + y_modifier))
        text_health = stat_font.render(f'health:  {character.health}/{character.health_max}', False, (0, 0, 0)) 
        SCREEN.blit(text_health, (880 * self.multi, (369 * self.multi) + y_modifier))
        text_mana = stat_font.render(f'mana:  {character.mana}/{character.mana_max}', False, (0, 0, 0)) 
        SCREEN.blit(text_mana, (880 * self.multi, (381 * self.multi) + y_modifier))

    def draw_inventory(self, character, y_modifier, SCREEN):
        x_modifier = 0     
        for item in character.inventory:
            item_img = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/{item.icon}.png")
            SCREEN.blit(pygame.transform.scale(item_img,(item_img.get_width() * self.multi, item_img.get_height() * self.multi)), ((770 * self.multi) + x_modifier, (487 * self.multi) + y_modifier)) 
            x_modifier += 51 * self.multi
        x_modifier = 0 


    def draw_bars(self, y_modifier, SCREEN, character):
        bar_y = (481 * self.multi) + y_modifier
        width = 10 * self.multi
        poison = ((character.poison_tick / character.health_max) * 62) * self.multi

        pygame.draw.rect(SCREEN,(150,30,30),((723 * self.multi), bar_y, width, 62 * self.multi))
        if "poisoned" in character.status:
            pygame.draw.rect(SCREEN, (30,100,30), ((723 * self.multi), bar_y + character.missing_health - 2, width, poison + 2))
        pygame.draw.rect(SCREEN, (30,30,30), ((723 * self.multi), bar_y, width, character.missing_health))
        pygame.draw.rect(SCREEN,(30,30,150),((737 * self.multi), bar_y, width, 62 * self.multi))         
        pygame.draw.rect(SCREEN, (30,30,30), ((737 * self.multi), bar_y, width, character.missing_mana * self.multi))
    
    def draw_uses(self, character, screen):
        case_font = pygame.font.SysFont('Comic Sans MS', int(16 * self.multi))
        background = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/select_use.png")
        equip = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_equip.png")
        drop = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_drop.png")
        consume = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_consume.png")
        learn = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_learn.png")
        examine = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_inspect.png")
        repair = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_repair.png")
        cast = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_cast.png")
        enchant = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/use_enchant.png")
        self.screen.blit(pygame.transform.scale(background, (background.get_width() * 1.5 * self.multi, background.get_height() * 1.5 * self.multi)), (100 * self.multi, 300 * self.multi))
        close_x = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/close.png")
        blit_equip = self.screen.blit(pygame.transform.scale(equip, (equip.get_width() * 1.5 * self.multi, equip.get_height() * 1.5 * self.multi)), (115 * self.multi, 347 * self.multi))
        blit_consume = self.screen.blit(pygame.transform.scale(consume, (consume.get_width() * 1.5 * self.multi, consume.get_height() * 1.5 * self.multi)), (225 * self.multi, 347 * self.multi))
        blit_drop = self.screen.blit(pygame.transform.scale(drop, (equip.get_width() * 1.5 * self.multi, equip.get_height() * 1.5 * self.multi)), (115 * self.multi, 467 * self.multi))
        blit_learn = self.screen.blit(pygame.transform.scale(learn, (learn.get_width() * 1.5 * self.multi, learn.get_height() * 1.5 * self.multi)), (225 * self.multi, 467 * self.multi))
        blit_examine = self.screen.blit(pygame.transform.scale(examine, (examine.get_width() * 1.5 * self.multi, examine.get_height() * 1.5 * self.multi)), (330 * self.multi, 347 * self.multi))
        blit_cast = self.screen.blit(pygame.transform.scale(cast, (cast.get_width() * 1.5 * self.multi, cast.get_height() * 1.5 * self.multi)), (330 * self.multi, 467 * self.multi))
        blit_repair = self.screen.blit(pygame.transform.scale(repair, (repair.get_width() * 1.5 * self.multi, repair.get_height() * 1.5 * self.multi)), (443 * self.multi, 347 * self.multi))
        blit_enchant = self.screen.blit(pygame.transform.scale(enchant, (enchant.get_width() * 1.5 * self.multi, enchant.get_height() * 1.5 * self.multi)), (443 * self.multi, 467 * self.multi))
        close = self.screen.blit(pygame.transform.scale(close_x, (close_x.get_width() * self.multi, close_x.get_height() * self.multi)), (522 * self.multi, 300 * self.multi))
        text_title = self.name_font.render(f'Select Intention!', False, (0, 0, 0))
        text_equip = case_font.render(f'Equip/Unequip', False, (0, 0, 0))
        text_consume = case_font.render(f'Consume', False, (0, 0, 0))
        text_drop = case_font.render(f'Drop', False, (0, 0, 0))
        text_learn = case_font.render(f'Learn', False, (0, 0, 0))
        text_examine = case_font.render(f'Examine', False, (0, 0, 0))
        text_cast = case_font.render(f'Cast', False, (0, 0, 0))
        text_repair = case_font.render(f'Repair', False, (0, 0, 0))
        text_enchant = case_font.render(f'Enchant Item', False, (0, 0, 0))
        text_title_rect = text_title.get_rect()
        text_equip_rect = text_equip.get_rect()
        text_examine_rect = text_examine.get_rect()
        text_consume_rect = text_consume.get_rect()
        text_repair_rect = text_repair.get_rect()
        text_drop_rect = text_drop.get_rect()
        text_learn_rect = text_learn.get_rect()
        text_cast_rect = text_cast.get_rect()
        text_enchant_rect = text_enchant.get_rect()
        text_drop_rect.center = (165 * self.multi, 570 * self.multi)
        text_equip_rect.center = (165 * self.multi, 450 * self.multi)
        text_examine_rect.center = (375 * self.multi, 450 * self.multi)
        text_title_rect.center = (320 * self.multi, 325 * self.multi)
        text_consume_rect.center = (270 * self.multi, 450 * self.multi)
        text_learn_rect.center = (270 * self.multi, 570 * self.multi)
        text_cast_rect.center = (375 * self.multi, 570 * self.multi)
        text_repair_rect.center = (490 * self.multi, 450 * self.multi)
        text_enchant_rect.center = (490 * self.multi, 570 * self.multi)
        self.screen.blit(text_equip, text_equip_rect)
        self.screen.blit(text_title, text_title_rect)
        self.screen.blit(text_consume, text_consume_rect)
        self.screen.blit(text_drop, text_drop_rect)
        self.screen.blit(text_learn, text_learn_rect)
        self.screen.blit(text_examine, text_examine_rect)
        self.screen.blit(text_cast, text_cast_rect)
        self.screen.blit(text_repair, text_repair_rect)
        self.screen.blit(text_enchant, text_enchant_rect)
        screen.blit(pygame.transform.scale(screen, screen.get_rect().size), (0, 0))
        pygame.display.update()
        return close, blit_equip, blit_drop, blit_consume, blit_learn, blit_examine, blit_cast


class Inventory:
    def __init__(self, character, SCREEN, value, multi):
        self.owner = character
        self.screen = SCREEN
        self.value = value
        self.paper_doll = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/paperdoll_{self.owner.p_portrait}.png").convert_alpha()
        h = self.paper_doll.get_height()  
        w = self.paper_doll.get_width()
        self.paper_doll = pygame.transform.scale(self.paper_doll, (w * multi, h * multi))
        self.inventory_screen = pygame.image.load(f"D:/imagine/git/games/dark_realm/Dark_Realm/images/inventory_{self.value}.png").convert_alpha()
        h = self.inventory_screen.get_height()  
        w = self.inventory_screen.get_width()
        self.inventory_screen = pygame.transform.scale(self.inventory_screen, (w * multi, h * multi))


class Map:
    def __init__(self, map_to_load, party):
        self.map_to_load = map_to_load
        with open('D:/imagine/git/games/dark_realm/Dark_Realm/maps.json', 'r') as file:
            data = json.load(file)
        self.multi = party.multi
        map_data = data[0][map_to_load]
        self.map_name = map_data['name']
        self.tileset = map_data['tileset']
        self.floor = map_data['floor']
        img, pix = self.load_map_image()
        self.height = img.height
        self.width = img.width
        self.map_grid = []
        self.interaction = map_data['interactions']
        self.create_map(pix, party) 


    def load_map_image(self):
        img = Image.open(f"D:/imagine/git/games/dark_realm/Dark_Realm/maps/{self.map_to_load}.png")
        pix = img.load()
        return img, pix 
    
    def next_map(self, party):
        next_map = int(self.map_to_load)
        next_map += 1
        self.map_to_load = str(next_map)
        img, pix = self.load_map_image()
        self.height = img.height
        self.width = img.width
        self.map_grid = []
        self.create_map(pix, party)       
    
    def create_map(self, pix, party):
        temp_list = []
        for i in reversed(range(self.height)):
            for j in range(self.width):
                if pix[i,j] == (0,0,0,255):
                    temp_list.append(Tile(icon='R', colour=Fore.red, npc=None, interaction=None))
                elif pix[i,j] == (0,255,0,255):
                    temp_list.append(Tile(icon='P', colour=Fore.green, npc=None, interaction=None))
                elif pix[i,j] == (255,255,255,255):
                    temp_list.append(Tile(icon='O', colour=Fore.black, npc=None, interaction=None))
                elif pix[i,j] == (0,0,255,255):
                    temp_list.append(Tile(icon='O', colour=Fore.blue, npc=Npc(self.multi), interaction=None))
            self.map_grid.append(temp_list)
            temp_list = []
        self.find_party(party)
        for i in range(len(self.map_grid)):
            for j in range(len(self.map_grid[i])):
                tile = self.map_grid[i][j]
                tile.i = i
                tile.j = j
                location = str(tile.i) + str(tile.j)
                if location in self.floor:
                    for item in self.floor[location]:
                        tile.floor.append(Item(item))
                    tile.colour = Fore.magenta
                if location in self.interaction:
                    name, direction, target_grid = self.interaction[location].split(" ")
                    x = int(target_grid[:2])
                    y = int(target_grid[2:])
                    target = self.map_grid[x][y]
                    tile.interaction = Interaction(name, direction, target, self.tileset)
                    tile.colour = Fore.yellow

    def check_directions(self, direction_1, direction_2):
        directions = ["N", "E", "S", "W"]
        if directions.index(direction_1) == directions.index(direction_2):
            return 1
        elif abs(directions.index(direction_1) -  directions.index(direction_2)) == 2:
            return 0
        elif directions.index(direction_1) -  directions.index(direction_2) == -1 or directions.index(direction_1) -  directions.index(direction_2) == 3:
            return 2
        else:
            return 3
                

    def rotate_map_clockwise(self):
        temp_map = []
        temp_grid = []


        for i in range(len(self.map_grid)):
            for j in reversed(range(len(self.map_grid[i]))):
                temp_grid.append(self.map_grid[j][i])
            temp_map.append(temp_grid)
            temp_grid = []

        self.map_grid = temp_map
    
    def rotate_map_anti_clockwise(self):
        temp_map = []
        temp_grid = []

        for i in reversed(range(len(self.map_grid))):
            for j in range(len(self.map_grid)):
                temp_grid.append(self.map_grid[j][i])
            temp_map.append(temp_grid)
            temp_grid = []

        self.map_grid = temp_map

    def find_party(self, party):
        for i in range(len(self.map_grid)):
            for j in range((len(self.map_grid[i]))):
                tile = self.map_grid[i][j]
                if tile.icon == 'P':
                    party.p_position = [i,j]
                    return


class Text_Log:
    def __init__(self, screen, multi, font):
        self.screen = screen
        self.multi = multi
        self.font = font
        self.log = []
        self.add_to_log("welcome!!",(200,0,0))

    
    def add_to_log(self, text, color):
        self.log.insert(0, Text(text, color, self.font))
        if len(self.log) > 50:
            self.log.pop()
    
    def draw_log_small(self):
        count = 0
        y_modifier = 0
        for log in self.log:
            if count > 5:
                return
            self.screen.blit(log.text, (10 * self.multi, ((530 * self.multi) - y_modifier)))
            y_modifier += 20 * self.multi
            count += 1


class Text:
    def __init__(self, text, color, font):
        self.text = font.render(f'{text}', False, color) 
