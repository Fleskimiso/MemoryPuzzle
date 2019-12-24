import random
import sys
import time

from pygame.locals import *

from Colors import Colors
from Puzzle import *


class Game:
    screen_width = 800
    screen_height = 500

    def __init__(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.fps = 30
        self.puzzle_list = []
        self.generate_puzzle_list()
        self.title = "Memory puzzle game"
        self.current_puzzle = [None, None]
        self.should_be_removed = False
        self.pop_time = time.time()
        self.font_object = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.game_won = False
        self.puzzles_left  = 0
        self.screen_messages_and_coordinates = {
            'puzzles_left' : ["Puzzles left: ",(0,0)],
            'win': ["Congratulations. You won",((self.screen_width - 60 * 6) / 2, self.screen_height / 2)]
        }
        pygame.display.set_caption(self.title)

    def generate_puzzle_list(self):
        self.puzzle_list.clear()
        for color_obj in Colors:
            for shape in Shapes:
                self.puzzle_list.append(Puzzle(shape, color_obj, 0, 0))
                self.puzzle_list.append(Puzzle(shape, color_obj, 0, 0))
        random.shuffle(self.puzzle_list)
        print(self.puzzle_list)
        positions = []
        translation_x = (self.screen_width - 60 * 6) / 2
        translation_y = (self.screen_height - 60 * 4) / 2
        for x in range(6):
            for y in range(4):
                positions.append({
                    'x': translation_x + x * 60,
                    'y': translation_y + y * 60
                })
        it = 0
        for puzzle in self.puzzle_list:
            puzzle.x_position = positions[it]['x']
            puzzle.y_position = positions[it]['y']
            print(str(it) + " Position: ", (puzzle.x_position, puzzle.y_position))
            it += 1
        self.puzzles_left = len(self.puzzle_list)/2

    def run(self):
        while 1:
            self.logic()
            self.draw()
            pygame.display.update()
            pygame.time.delay(self.fps)

    def draw(self):
        self.screen.fill((23, 56, 56))
        for puzzle in self.puzzle_list:
            self.screen.blit(puzzle.surface, (puzzle.x_position, puzzle.y_position))
        self.screen.blit(self.font_object.render(self.title, True, (0, 0, 0)), ((self.screen_width - 60 * 6) / 2, 50))
        self.screen.blit(self.font_object.render(self.screen_messages_and_coordinates['puzzles_left'][0] + str(int(len(self.puzzle_list) / 2)), True, (0, 0, 0)),
                         self.screen_messages_and_coordinates['puzzles_left'][1])
        if self.game_won:
            self.screen.blit(self.font_object.render(self.screen_messages_and_coordinates['win'][0], True, (0, 0, 0)),
                            self.screen_messages_and_coordinates['win'][1])

    def logic(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == QUIT:
                if event.key == K_ESCAPE:
                    sys.exit(1)
                elif event.key == K_r:
                    self.puzzle_list.clear()
                    self.game_won = True
            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pressed())
                mouse_position = pygame.mouse.get_pos()
                for puzzle in self.puzzle_list:
                    rectangle = pygame.Rect(puzzle.x_position, puzzle.y_position, puzzle.width, puzzle.height)
                    if rectangle.collidepoint(mouse_position[0], mouse_position[1]):
                        print("Collision detection. ")
                        if self.current_puzzle[0] is not None and self.current_puzzle[1] is not None:
                            self.pop_time -=1
                            continue
                        puzzle.draw_figure()
                        if self.current_puzzle[0] is None:
                            self.current_puzzle[0] = puzzle
                        elif self.current_puzzle[0] is not None:
                            if self.current_puzzle[0].color == puzzle.color and self.current_puzzle[0].shape == puzzle.shape and self.current_puzzle[0] is not puzzle:
                                self.current_puzzle[1] = puzzle
                                self.pop_time = time.time()
                                self.should_be_removed = True
                            else:
                                # print("Setting should be removed to false")
                                if self.current_puzzle[0] is not puzzle:
                                    self.current_puzzle[1] = puzzle
                                    self.should_be_removed = False
                                    self.pop_time = time.time()
                if self.game_won:
                    size_of_button_rect = self.font_object.size(self.screen_messages_and_coordinates['win'][0])
                    translation_of_button_rect =self.screen_messages_and_coordinates['win'][1]
                    rect = pygame.Rect(translation_of_button_rect,size_of_button_rect)
                    if rect.collidepoint(mouse_position):
                        print("Regenerating list: ")
                        self.game_won = False
                        self.generate_puzzle_list()

        # actuall logic goes here from this tabulation, input handling is up
        if (time.time() - self.pop_time > 1) and (
                self.current_puzzle[0] is not None and self.current_puzzle[1] is not None):
            # print("Acting on bool: it value: ", self.should_be_removed)
            if self.should_be_removed:
                for puzzle in self.current_puzzle:
                    self.puzzle_list.remove(puzzle)
                self.current_puzzle[0] = None
                self.current_puzzle[1] = None
            elif not self.should_be_removed:
                print("should be blank: ")
                self.current_puzzle[0].draw_blank()
                self.current_puzzle[0] = None
                print(self.current_puzzle[0])
                self.current_puzzle[1].draw_blank()
                self.current_puzzle[1] = None
        if len(self.puzzle_list) == 0:
            self.game_won = True


# game run
pygame.init()
game = Game()
game.run()
