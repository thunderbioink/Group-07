import enum
from typing import Text
import pygame
from csv import reader
from power_up import Power_Up
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
from text_box import Text_Box
from questions import Quesion_Event

class Level:
    def __init__(self,level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.power_ups = pygame.sprite.Group()
        self.text_box = pygame.sprite.GroupSingle()
        self.question = []
        # self.boss = pygame.sprite.GroupSingle()
        # self.fire_balls = pygame.sprite.GroupSingle()
        # file_path_books = "assets/maps/maps/prototype map_books.csv"
        # file_path_desk = "assets/maps/maps/prototype map_desk.csv"

        # book_map = []
        # with open(file_path_books) as map:
        #     level = reader(map, delimiter = ',')
        #     for row in level:
        #         book_map.append(list(row))

        # for row_index, row in enumerate(book_map):
        #     for col_index, val in enumerate(row):
        #         if val == '0':
        #             x = col_index * tile_size
        #             y = row_index * tile_size
        #             tile = Tile((x,y), tile_size, "assets/graphics/bookpiles.png")
        #             self.tiles.add(tile)

        
        # desk_map = []
        # with open(file_path_desk) as map:
        #     level = reader(map, delimiter = ',')
        #     for row in level:
        #         book_map.append(list(row))

        # for row_index, row in enumerate(desk_map):
        #     for col_index, val in enumerate(row):
        #         if val == '0':
        #             x = col_index * tile_size
        #             y = row_index * tile_size
        #             tile = Tile((0,0), tile_size, "assets/graphics/desk.png")
        #             self.tiles.add(tile)

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x,y), tile_size, "assets/graphics/books.png")
                    self.tiles.add(tile)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                if cell == 'O':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    power_up = Power_Up((x,y), tile_size)
                    self.power_ups.add(power_up)
            
    def scrol_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizonal_movment_collision(self):
        
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        for sprite in self.power_ups.sprites():
            if sprite.rect.colliderect(player.rect):
                question = Quesion_Event(self, player, sprite.right, sprite.wrong)
                pygame.sprite.Sprite.kill(sprite)
                self.question.append(question)
                text_box = question.create_text_box()
                self.text_box.add(text_box)

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def virtical_movment_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

        for sprite in self.power_ups.sprites():
            if sprite.rect.colliderect(player.rect):
                question = Quesion_Event(self, player, sprite.right, sprite.wrong)
                pygame.sprite.Sprite.kill(sprite)
                self.question.append(question)
                text_box = question.create_text_box()
                self.text_box.add(text_box)


    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.horizonal_movment_collision()
        self.virtical_movment_collision()
        self.player.draw(self.display_surface)
        self.scrol_x()

        self.power_ups.update(self.world_shift)
        self.power_ups.draw(self.display_surface)
        
        self.text_box.draw(self.display_surface)

        for i in self.question:
            i.update(self, self.player.sprite)

        
