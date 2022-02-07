import pprint
import pygame
from pygame.locals import *
import os
import numpy as np

BACKGROUND_COLOR = 'black'
CELL_EMPTY = 0
CELL_RED = 1
CELL_YELLOW = 2
COLUMN_FONT_SIZE = 50
HEADER_HEIGHT = 100
PLAYER1 = 1
PLAYER2 = 2
SQUARE_SIZE = 100

class square:
    def __init__(self, surface, x, y):
        global SQUARE_SIZE, CELL_EMPTY, PLAYER1
        self._RED = (220, 0, 0)
        self._BLACK = (0, 0, 0)
        self._BLUE = (50,70,220)
        self._WIN_LINE = (117, 251, 76)
        self._BACKGROUND = (54, 69, 212)
        self._YELLOW = (240, 240, 0)
        self._color = self._BLACK
        self._x = x
        self._y = y
        self._diameter = SQUARE_SIZE
        self._surface = surface
        self._occupied_by = CELL_EMPTY
    
    def setOccupancy(self, occupied_by):
        self._occupied_by = occupied_by

    def render(self):
        global HEADER_HEIGHT, CELL_RED, CELL_YELLOW, CELL_EMPTY
        radius = self._diameter / 2
        pygame.draw.rect(self._surface, self._BACKGROUND, [
                         self._x * self._diameter, (self._y * self._diameter) + HEADER_HEIGHT, self._diameter, self._diameter])
        pygame.draw.line(self._surface, self._BLACK, (self._x * self._diameter, (self._y * self._diameter) + HEADER_HEIGHT), 
                                                      ((self._x + 1) * self._diameter, (self._y * self._diameter) + HEADER_HEIGHT), 2)
        pygame.draw.line(self._surface, self._BLACK, ((self._x + 1) * self._diameter, (self._y * self._diameter) + HEADER_HEIGHT), 
                                                      ((self._x + 1) * self._diameter, ((self._y + 1) * self._diameter) + HEADER_HEIGHT), 2)
        pygame.draw.line(self._surface, self._BLACK, ((self._x + 1) * self._diameter, ((self._y + 1) * self._diameter) + HEADER_HEIGHT), 
                                                      (self._x * self._diameter, ((self._y + 1) * self._diameter) + HEADER_HEIGHT), 2)
        pygame.draw.line(self._surface, self._BLACK, (self._x * self._diameter, ((self._y + 1) * self._diameter) + HEADER_HEIGHT), 
                                                      (self._x * self._diameter, (self._y * self._diameter) + HEADER_HEIGHT), 2)
        color = self._BLACK
        if self._occupied_by == CELL_RED:
            color = self._RED
        elif self._occupied_by == CELL_YELLOW:
            color = self._YELLOW

        pygame.draw.circle(self._surface, color, 
            (self._x * self._diameter + radius, (self._y * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 12, 0)
        
        if (color != self._BLACK):
            pygame.draw.circle(self._surface, self._BLACK, 
                (self._x * self._diameter + radius, (self._y * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 15, 2)
            pygame.draw.circle(self._surface, self._BLACK, 
                (self._x * self._diameter + radius, (self._y * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 20, 1)
            if ((self._x % 4) == 0):
                pygame.draw.circle(self._surface, self._WIN_LINE, 
                    (self._x * self._diameter + radius, (self._y * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 9, 5)

        # pygame.display.flip()
        foo = 1


class Connect4Game:
    def __init__(self):
        global PLAYER1
        self._running = True
        self._display_surf = None
        self._current_player = PLAYER1

    def on_init(self):
        global CELL_RED, CELL_YELLOW, SQUARE_SIZE, HEADER_HEIGHT
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            [SQUARE_SIZE * 7 + 1, SQUARE_SIZE * 6 + HEADER_HEIGHT], pygame.RESIZABLE)
        pygame.display.set_caption("Connect 4")
        self._rows = 6
        self._cols = 7

        # _squares = [[square()] * self._cols for _ in range(self._rows)]
        self._squares = []
        for y in range(self._rows):
            row = []
            for x in range(self._cols):
                row.append(square(self._display_surf, x, y))
            self._squares.append(row)

        self._running = True

    def dropColumn(self, occupancy, column):
        global CELL_EMPTY
        lastRow = -1
        y = 0
        while (y < self._rows) and (self._squares[y][column]._occupied_by == CELL_EMPTY):
            lastRow = y
            y = y + 1
        
        if (lastRow == -1):
            return False
        else:
            self._squares[lastRow][column]._occupied_by = occupancy
            return True

    def next_cell(self, x, y, direction):
        if direction == 'up':
            new_x = x + 0
            new_y = y - 1
        elif direction == 'up_right':
            new_x = x + 1
            new_y = y - 1
        elif direction == 'right':
            new_x = x + 1
            new_y = y + 0
        elif direction == 'down_right':
            new_x = x + 1
            new_y = y + 1
        elif direction == 'down':
            new_x = x + 0
            new_y = y + 1
        elif direction == 'down_left':
            new_x = x - 1
            new_y = y + 1
        elif direction == 'left':
            new_x = x - 1
            new_y = y - 0
        elif direction == 'up_left':
            new_x = x - 1
            new_y = y - 1
        else:
            new_x = -1
            new_y = -1
        
        if (new_x < 0) or (new_x >= self._cols) or (new_y < 0) or (new_y >= self._rows):
            return False
        else:
            return (new_x, new_y)

    # def is_4_in_a_row_starting_at(self, x, y):

    
    def is_column_filled(self, column):
        global CELL_EMPTY
        return self._squares[0][column]._occupied_by != CELL_EMPTY

    def swap_player(self):
        global PLAYER1, PLAYER2
        if self._current_player == PLAYER1:
            self._current_player = PLAYER2
        else:
            self._current_player = PLAYER1

    def on_event(self, event):
        global CELL_RED, CELL_YELLOW, PLAYER1
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            success = False
            current_player_cell = CELL_RED if self._current_player == PLAYER1 else CELL_YELLOW
            if event.key == pygame.K_1:
                success = self.dropColumn(current_player_cell, 0)
            elif event.key == pygame.K_2:
                success = self.dropColumn(current_player_cell, 1)
            elif event.key == pygame.K_3:
                success = self.dropColumn(current_player_cell, 2)
            elif event.key == pygame.K_4:
                success = self.dropColumn(current_player_cell, 3)
            elif event.key == pygame.K_5:
                success = self.dropColumn(current_player_cell, 4)
            elif event.key == pygame.K_6:
                success = self.dropColumn(current_player_cell, 5)
            elif event.key == pygame.K_7:
                success = self.dropColumn(current_player_cell, 6)
            
            if success:
                self.swap_player()

    def on_loop(self):
        pass

    def on_render(self):
        global BACKGROUND_COLOR, COLUMN_FONT_SIZE, HEADER_HEIGHT, SQUARE_SIZE
        for y in range(self._rows):
            for x in range(self._cols):
                self._squares[y][x].render()

        pygame.font.init()
        font = pygame.font.Font("arial.ttf", COLUMN_FONT_SIZE)
        # col_numbers = font.render("1 2 3 4 5 6 7", True, (0,255,255))
        # self._display_surf.blit(col_numbers, (40,90))

        for col_number in range(0, 7):
            # col_text = font.render("hello there", True, (0, 255, 255))
            # col_text = font.render("1 2 3 4 5 6 7", True, (0,255,255))
            # self._display_surf.blit(col_text, (col_number * 50, 50))
            if self.is_column_filled(col_number):
                column_number_color = BACKGROUND_COLOR
            else:
                column_number_color = 'white'

            col_numbers = font.render(str(col_number + 1), True, column_number_color, BACKGROUND_COLOR)
            self._display_surf.blit(col_numbers, ((col_number * SQUARE_SIZE) + (SQUARE_SIZE / 3), HEADER_HEIGHT - (COLUMN_FONT_SIZE + 4)))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):

        if self.on_init() == False:
            self._running = False
        
        # elem = "[{x:1d},{y:1d}] "
        # for dir in ['up', 'up_right', 'right', 'down_right', 'down', 'down_left', 'left', 'up_left']:
        #     print("\n--- %s ---" % dir)
        #     for y in range(6):
        #         line = ""
        #         for x in range(7):
        #             next_cell = self.next_cell(x, y, dir)
        #             if (next_cell):
        #                 line += elem.format(x = next_cell[0], y = next_cell[1])
        #             else:
        #                 line += " -,-  "
        #         print(line)

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    global pp
    pp = pprint.PrettyPrinter(width=41, compact=True)
    game = Connect4Game()
    game.on_execute()
