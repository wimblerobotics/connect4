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
    def __init__(self, surface, col, row):
        global SQUARE_SIZE, CELL_EMPTY, PLAYER1
        self._RED = (220, 0, 0)
        self._BLACK = (0, 0, 0)
        self._BLUE = (50,70,220)
        self._WIN_LINE = (117, 251, 76)
        self._BACKGROUND = (54, 69, 212)
        self._YELLOW = (240, 240, 0)
        self._color = self._BLACK
        self._col = col
        self._row = row
        self._diameter = SQUARE_SIZE
        self._surface = surface
        self._occupied_by = CELL_EMPTY
        self._winner = False
    
    def setOccupancy(self, occupied_by):
        self._occupied_by = occupied_by

    def render(self):
        global HEADER_HEIGHT, CELL_RED, CELL_YELLOW, CELL_EMPTY
        radius = self._diameter / 2
        pygame.draw.rect(self._surface, self._BACKGROUND, [
                         self._col * self._diameter, (self._row * self._diameter) + HEADER_HEIGHT, self._diameter, self._diameter])
        pygame.draw.line(self._surface, self._BLACK, (self._col * self._diameter, (self._row * self._diameter) + HEADER_HEIGHT), 
                                                      ((self._col + 1) * self._diameter, (self._row * self._diameter) + HEADER_HEIGHT), 2)
        pygame.draw.line(self._surface, self._BLACK, ((self._col + 1) * self._diameter, (self._row * self._diameter) + HEADER_HEIGHT), 
                                                      ((self._col + 1) * self._diameter, ((self._row + 1) * self._diameter) + HEADER_HEIGHT), 2)
        pygame.draw.line(self._surface, self._BLACK, ((self._col + 1) * self._diameter, ((self._row + 1) * self._diameter) + HEADER_HEIGHT), 
                                                      (self._col * self._diameter, ((self._row + 1) * self._diameter) + HEADER_HEIGHT), 2)
        pygame.draw.line(self._surface, self._BLACK, (self._col * self._diameter, ((self._row + 1) * self._diameter) + HEADER_HEIGHT), 
                                                      (self._col * self._diameter, (self._row * self._diameter) + HEADER_HEIGHT), 2)
        color = self._BLACK
        if self._occupied_by == CELL_RED:
            color = self._RED
        elif self._occupied_by == CELL_YELLOW:
            color = self._YELLOW

        pygame.draw.circle(self._surface, color, 
            (self._col * self._diameter + radius, (self._row * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 12, 0)
        
        if (color != self._BLACK):
            pygame.draw.circle(self._surface, self._BLACK, 
                (self._col * self._diameter + radius, (self._row * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 15, 2)
            pygame.draw.circle(self._surface, self._BLACK, 
                (self._col * self._diameter + radius, (self._row * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 20, 1)
            if (self._winner):
                pygame.draw.circle(self._surface, self._WIN_LINE, 
                    (self._col * self._diameter + radius, (self._row * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 9, 5)
            else:
                pygame.draw.circle(self._surface, color,
                    (self._col * self._diameter + radius, (self._row * self._diameter + radius) + HEADER_HEIGHT), (self._diameter / 2) - 9, 5)

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

        self._squares = []
        for row in range(self._rows):
            row_of_squares = []
            for col in range(self._cols):
                row_of_squares.append(square(self._display_surf, col, row))
            self._squares.append(row_of_squares)

        self._running = True

    def dropColumn(self, occupancy, column):
        global CELL_EMPTY
        lastRow = -1
        row = 0
        while (row < self._rows) and (self._squares[row][column]._occupied_by == CELL_EMPTY):
            lastRow = row
            row = row + 1
        
        if (lastRow == -1):
            return False
        else:
            self._squares[lastRow][column]._occupied_by = occupancy
            self._squares[lastRow][column].render()
            return True

    def next_cell(self, col, row, direction):
        if direction == 'up':
            new_col = col + 0
            new_row = row - 1
        elif direction == 'up_right':
            new_col = col + 1
            new_row = row - 1
        elif direction == 'right':
            new_col = col + 1
            new_row = row + 0
        elif direction == 'down_right':
            new_col = col + 1
            new_row = row + 1
        elif direction == 'down':
            new_col = col + 0
            new_row = row + 1
        elif direction == 'down_left':
            new_col = col - 1
            new_row = row + 1
        elif direction == 'left':
            new_col = col - 1
            new_row = row - 0
        elif direction == 'up_left':
            new_col = col - 1
            new_row = row - 1
        else:
            new_col = -1
            new_row = -1
        
        if (new_col < 0) or (new_col >= self._cols) or (new_row < 0) or (new_row >= self._rows):
            return False
        else:
            return (new_col, new_row)

    def find_run_in_direction_starting_at(self, col, row, direction):
        global CELL_EMPTY
        if self._squares[row][col]._occupied_by == CELL_EMPTY:
            return 0
        else:
            current_occupant = self._squares[row][col]._occupied_by

        new_col = col
        new_y = row
        run_length = 0
        for i in range(self._cols):
            try:
                if self._squares[new_y][new_col]._occupied_by == current_occupant:
                    run_length += 1
                    (new_col, new_y) = self.next_cell(new_col, new_y, direction)
                else:
                    break
            except:
                break
        
        return run_length

    def game_won(self):
        global CELL_EMPTY
        for dir in ['up', 'up_right', 'right', 'down_right', 'down', 'down_left', 'left', 'up_left']:
            for row in range(self._rows):
                for col in range(self._cols):
                    if self.find_run_in_direction_starting_at(col, row, dir) >= 4:
                        return (row, col, dir, self._squares[row][col]._occupied_by)

        return (-1, -1, 'up', CELL_EMPTY)
    
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
        global CELL_EMPTY, CELL_RED, CELL_YELLOW, PLAYER1
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
            elif event.key == pygame.K_r:
                self._current_player = PLAYER1
            elif event.key == pygame.K_y:
                self._current_player = PLAYER2
            
            if success:
                self.swap_player()
                # print("Run length[0,5]: %d", self.find_run_in_direction_starting_at(0, 0, 'down_right'))

                # If winner found, mark winning squares.
                (row, col, dir, winner) = self.game_won()
                if winner != CELL_EMPTY:
                    print("Game won by %s" % "RED" if winner == CELL_RED else "YELLOW")
                    starting_square = self._squares[row][col]
                    radius = starting_square._diameter / 2
                    for counter in range(4):
                        self._squares[row][col]._winner = True
                        try:
                            (c, r) = self.next_cell(col, row, dir)
                            row = r
                            col = c
                        except:
                            print("whoops")

    def on_loop(self):
        pass

    def on_render(self):
        global BACKGROUND_COLOR, CELL_RED, COLUMN_FONT_SIZE, HEADER_HEIGHT, SQUARE_SIZE

        # Draw circle showing color of current player.
        player_color_radius = 10
        current_player_cell = CELL_RED if self._current_player == PLAYER1 else CELL_YELLOW
        color = 'red' if current_player_cell == CELL_RED else 'yellow'
        pygame.draw.circle(self._display_surf, color, 
            (0 + player_color_radius, 0 + player_color_radius), player_color_radius, 0)

        # Render squares.
        for row in range(self._rows):
            for col in range(self._cols):
                self._squares[row][col].render()

        # Show column headers.
        font = pygame.font.Font("arial.ttf", COLUMN_FONT_SIZE)

        (row, col, dir, winner) = self.game_won()
        for col_number in range(0, 7):
            if self.is_column_filled(col_number) or (winner != CELL_EMPTY):
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
        
        pygame.font.init()
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
