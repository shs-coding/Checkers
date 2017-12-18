import pygame
import sys
import getpass
import time

pygame.init()
pygame.mixer.pre_init(frequency=64000, size=-16, channels=2)
pygame.mixer.init()

username = getpass.getuser()

white = (255, 255, 255)
black = (0, 0, 0)


# ---------- LOADS FILES FROM FOLDER ---------- #

# LOADS BACKGROUNDS #

background = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/background.jpg')
dark_background = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/dark_background.jpg')

# LOADS IMAGES FOR PIECES #

redpiece = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/redpiece.png')
redpiece = pygame.transform.scale(redpiece, (70, 70))

blackpiece = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/blackpiece.png')
blackpiece = pygame.transform.scale(blackpiece, (70, 70))

crown = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/crown.png')

# LOADS SOUNDS #

win_sound = ('C:/Users/' + username + '/Downloads/CheckersPython/YouWin.wav')
move_sound = ('C:/Users/' + username + '/Downloads/CheckersPython/move_sound.wav')

# LOADS IMAGES FOR SOUND ON AND SOUND OFF #

sound_on_img = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/SoundOn.png')
sound_on_img = pygame.transform.scale(sound_on_img, (75, 75))

sound_off_img = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/SoundOff.png')
sound_off_img = pygame.transform.scale(sound_off_img, (75, 75))

sound_rect = pygame.Rect(640, 0, 80, 80)

# CREATES DISPLAY #

screen = pygame.display.set_mode([720, 640])
caption = 'Checkers'
icon = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/icon.png')
pygame.display.set_caption(caption)
pygame.display.set_icon(icon)

# LOADS IMAGES FOR CANCEL BUTTONS #

red_cancel = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/RedCancel.png')
red_cancel_rect = pygame.Rect(640, 80, 80, 80)

black_cancel = pygame.image.load('C:/Users/' + username + '/Downloads/CheckersPython/BlackCancel.png')
black_cancel_rect = pygame.Rect(640, 480, 80, 80)

pygame.display.flip()


# ---------- PIECE CLASS ---------- #


class Piece:

    global screen
    global background
    global dark_background

    def __init__(self, color, grid_x, grid_y):

        self.color = color
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(self.grid_x * 80 + 5, self.grid_y * 80 + 5, 70, 70)
        self.is_king = False

    # BLITS CORRECT PIECE #

    def create(self):

        if self.color == 'red':
            screen.blit(redpiece, (self.grid_x * 80 + 5, self.grid_y * 80 + 5))
        elif self.color == 'black':
            screen.blit(blackpiece, (self.grid_x * 80 + 5, self.grid_y * 80 + 5))

        if self.is_king:
            screen.blit(crown, (self.grid_x * 80 + 15, self.grid_y * 80 + 15))

    # RESETS IMAGE SO ONLY ONE IMAGE PER PIECE IS VISIBLE #

    def reset(self):
        if self.grid_x % 2 == self.grid_y % 2:
            screen.blit(background, (self.grid_x * 80, self.grid_y * 80))
        else:
            screen.blit(dark_background, (self.grid_x * 80, self.grid_y * 80))

        pygame.draw.rect(screen, white, (self.grid_x * 80, self.grid_y * 80, 80, 80), 0)

    # CHANGES POSITION OF PIECE #

    def move(self):

        global red_1
        global red_2
        global red_3
        global red_4
        global red_5
        global red_6
        global red_7
        global red_8
        global red_9
        global red_10
        global red_11
        global red_12

        global black_1
        global black_2
        global black_3
        global black_4
        global black_5
        global black_6
        global black_7
        global black_8
        global black_9
        global black_10
        global black_11
        global black_12

        global graphics_complete

        global invalid_move
        global move_canceled

        global red_cancel_rect
        global black_cancel_rect

        invalid_move = False
        move_canceled = False

        done = False

        while not done:

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    (new_x, new_y) = pygame.mouse.get_pos()

                    if self.color == 'red' and red_cancel_rect.collidepoint(new_x, new_y):
                        done = True
                        move_canceled = True
                        reblit()

                    elif self.color == 'black' and black_cancel_rect.collidepoint(new_x, new_y):
                        done = True
                        move_canceled = True
                        reblit()

                    new_x = int(new_x / 80)
                    new_y = int(new_y / 80)

                    avg_x = int((self.grid_x + new_x) / 2)
                    avg_y = int((self.grid_y + new_y) / 2)

                    # ENSURES NEW POINT IS ON THE BOARD #

                    if new_x <= 7 and new_y <= 7:

                        # CASE FOR MOVES 1 BY 1 #

                        while self.color == 'red':

                            if abs(new_x - self.grid_x) == 1 and new_y - self.grid_y == 1 or self.is_king and abs(new_x - self.grid_x) == 1 and abs(new_y - self.grid_y) == 1:

                                if not screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (1, 1, 1, 255) and not screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (254, 0, 0, 255):

                                    pass

                                else:

                                    print("Invalid Move")
                                    invalid_move = True

                            # CASE FOR MOVES NOT 1 BY 1 #

                            else:

                                # MAKES SURE CAPTURE MOVE ACTUALLY CAPTURES SOMETHING #

                                captures = screen.get_at((int((self.grid_x + new_x) / 2) * 80 + 40, int((self.grid_y + new_y) / 2) * 80 + 40)) == (1, 1, 1, 255)

                                # MAKES SURE CAPTURE MOVE IS THE RIGHT SIZE AND DIRECTION #

                                if self.is_king:
                                    is_correct_size = abs(new_x - self.grid_x) == 2 and abs(new_y - self.grid_y) == 2

                                else:
                                    is_correct_size = abs(new_x - self.grid_x) == 2 and new_y - self.grid_y == 2

                                # MAKES SURE NEW SQUARE IS NOT OCCUPIED #

                                dest_occupied = screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (1, 1, 1, 255) or screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (254, 0, 0, 255)

                                if not captures or not is_correct_size or dest_occupied:

                                    print("Invalid Move")
                                    invalid_move = True

                                else:

                                    # DELETES PIECE THAT WAS CAPTURED #

                                    try:
                                        black_1
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_1.grid_x, black_1.grid_y):
                                            black_1.reset()
                                            del black_1

                                    try:
                                        black_2
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_2.grid_x, black_2.grid_y):
                                            black_2.reset()
                                            del black_2

                                    try:
                                        black_3
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_3.grid_x, black_3.grid_y):
                                            black_3.reset()
                                            del black_3

                                    try:
                                        black_4
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_4.grid_x, black_4.grid_y):
                                            black_4.reset()
                                            del black_4

                                    try:
                                        black_5
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_5.grid_x, black_5.grid_y):
                                            black_5.reset()
                                            del black_5

                                    try:
                                        black_6
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_6.grid_x, black_6.grid_y):
                                            black_6.reset()
                                            del black_6

                                    try:
                                        black_7
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_7.grid_x, black_7.grid_y):
                                            black_7.reset()
                                            del black_7

                                    try:
                                        black_8
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_8.grid_x, black_8.grid_y):
                                            black_8.reset()
                                            del black_8

                                    try:
                                        black_9
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_9.grid_x, black_9.grid_y):
                                            black_9.reset()
                                            del black_9

                                    try:
                                        black_10
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_10.grid_x, black_10.grid_y):
                                            black_10.reset()
                                            del black_10

                                    try:
                                        black_11
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_11.grid_x, black_11.grid_y):
                                            black_11.reset()
                                            del black_11

                                    try:
                                        black_12
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (black_12.grid_x, black_12.grid_y):
                                            black_12.reset()
                                            del black_12

                            break

                        while self.color == 'black':

                            # MAKES SURE MOVE IS NOT 1 BY 1 #

                            if abs(new_x - self.grid_x) == 1 and new_y - self.grid_y == -1 or self.is_king and abs(new_x - self.grid_x) == 1 and abs(new_y - self.grid_y) == 1:

                                if not screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (1, 1, 1, 255) and not screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (254, 0, 0, 255):

                                    pass

                                else:

                                    print("Invalid Move")
                                    invalid_move = True

                            # CASE FOR MOVES NOT 1 BY 1 #

                            else:
                                # MAKES SURE SOMETHING IS CAPTURED #

                                captures = screen.get_at((int((self.grid_x + new_x) / 2) * 80 + 40, int((self.grid_y + new_y) / 2) * 80 + 40)) == (254, 0, 0, 255)

                                # MAKES SURE CAPTURE MOVE IS THE RIGHT SIZE #

                                if self.is_king:
                                    is_correct_size = abs(new_x - self.grid_x) == 2 and abs(new_y - self.grid_y) == 2

                                else:
                                    is_correct_size = abs(new_x - self.grid_x) == 2 and new_y - self.grid_y == -2

                                # MAKES SURE NEW SQUARE IS NOT OCCUPIED #

                                dest_occupied = screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (1, 1, 1, 255) or screen.get_at((new_x * 80 + 40, new_y * 80 + 40)) == (254, 0, 0, 255)

                                if not captures or not is_correct_size or dest_occupied:

                                    print("Invalid Move")
                                    invalid_move = True

                                else:

                                    # DELETES PIECE THAT WAS CAPTURED #

                                    try:
                                        red_1
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_1.grid_x, red_1.grid_y):
                                            red_1.reset()
                                            del red_1

                                    try:
                                        red_2
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_2.grid_x, red_2.grid_y):
                                            red_2.reset()
                                            del red_2

                                    try:
                                        red_3
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_3.grid_x, red_3.grid_y):
                                            red_3.reset()
                                            del red_3

                                    try:
                                        red_4
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_4.grid_x, red_4.grid_y):
                                            red_4.reset()
                                            del red_4

                                    try:
                                        red_5
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_5.grid_x, red_5.grid_y):
                                            red_5.reset()
                                            del red_5

                                    try:
                                        red_6
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_6.grid_x, red_6.grid_y):
                                            red_6.reset()
                                            del red_6

                                    try:
                                        red_7
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_7.grid_x, red_7.grid_y):
                                            red_7.reset()
                                            del red_7

                                    try:
                                        red_8
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_8.grid_x, red_8.grid_y):
                                            red_8.reset()
                                            del red_8

                                    try:
                                        red_9
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_9.grid_x, red_9.grid_y):
                                            red_9.reset()
                                            del red_9

                                    try:
                                        red_10
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_10.grid_x, red_10.grid_y):
                                            red_10.reset()
                                            del red_10

                                    try:
                                        red_11
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_11.grid_x, red_11.grid_y):
                                            red_11.reset()
                                            del red_11

                                    try:
                                        red_12
                                    except NameError:
                                        pass
                                    else:
                                        if (avg_x, avg_y) == (red_12.grid_x, red_12.grid_y):
                                            red_12.reset()
                                            del red_12

                            pygame.display.flip()

                            break

                        # UPDATES THE ACTUAL POSITION #

                        if not invalid_move:

                            self.grid_x = new_x
                            self.grid_y = new_y

                            self.rect = pygame.Rect(self.grid_x * 80 + 5, self.grid_y * 80 + 5, 70, 70)

                            if self.color == 'red' and self.grid_y == 7 and not self.is_king:
                                self.is_king = True
                            elif self.color == 'black' and self.grid_y == 0 and not self.is_king:
                                self.is_king = True

                            if sound_on:
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load(move_sound)
                                pygame.mixer.music.play(1)

                        done = True
                        graphics_complete = False

                    break

# ---------- GRID ---------- #

grid = []
for x in range(8):
    column = []
    for y in range(8):
        column.append(white)
    grid.append(column)


# ---------- FUNCTION THAT CHECKS IF A PLAYER HAS WON ---------- #

def has_won():

    global red_1
    global red_2
    global red_3
    global red_4
    global red_5
    global red_6
    global red_7
    global red_8
    global red_9
    global red_10
    global red_11
    global red_12

    global black_1
    global black_2
    global black_3
    global black_4
    global black_5
    global black_6
    global black_7
    global black_8
    global black_9
    global black_10
    global black_11
    global black_12

    global game_over
    global sound_on

    # CHECKS IF BLACK HAS WON #
    try:
        red_1
    except NameError:
        try:
            red_2
        except NameError:
            try:
                red_3
            except NameError:
                try:
                    red_4
                except NameError:
                    try:
                        red_5
                    except NameError:
                        try:
                            red_6
                        except NameError:
                            try:
                                red_7
                            except NameError:
                                try:
                                    red_8
                                except NameError:
                                    try:
                                        red_9
                                    except NameError:
                                        try:
                                            red_10
                                        except NameError:
                                            try:
                                                red_11
                                            except NameError:
                                                try:
                                                    red_12
                                                except NameError:

                                                    game_over = True

                                                    reblit()

                                                    if sound_on:
                                                        pygame.mixer.music.stop()
                                                        pygame.mixer.music.load(win_sound)
                                                        pygame.mixer.music.play(1)

                                                    is_busy = pygame.mixer.music.get_busy()

                                                    while is_busy:
                                                        pygame.time.wait(30)
                                                        is_busy = pygame.mixer.music.get_busy()

                                                    sys.exit('Black has won!')

                                                else:
                                                    pass
                                            else:
                                                pass
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

    # CHECKS IF RED HAS WON #

    try:
        black_1
    except NameError:
        try:
            black_2
        except NameError:
            try:
                black_3
            except NameError:
                try:
                    black_4
                except NameError:
                    try:
                        black_5
                    except NameError:
                        try:
                            black_6
                        except NameError:
                            try:
                                black_7
                            except NameError:
                                try:
                                    black_8
                                except NameError:
                                    try:
                                        black_9
                                    except NameError:
                                        try:
                                            black_10
                                        except NameError:
                                            try:
                                                black_11
                                            except NameError:
                                                try:
                                                    black_12
                                                except NameError:

                                                    game_over = True

                                                    reblit()

                                                    if sound_on:
                                                        pygame.mixer.music.stop()
                                                        pygame.mixer.music.load(win_sound)
                                                        pygame.mixer.music.play(1)

                                                    is_busy = pygame.mixer.music.get_busy()

                                                    while is_busy:
                                                        pygame.time.wait(30)
                                                        is_busy = pygame.mixer.music.get_busy()

                                                    sys.exit('Black has won!')

                                                else:
                                                    pass
                                            else:
                                                pass
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

# ---------- RE-BLITS GRAPHICS --------- #


def reblit():

    global graphics_complete
    global red_turn
    global game_over

    global red_cancel_rect
    global black_cancel_rect

    global move_canceled
    global invalid_move

    global sound_on
    global sound_rect

    for a in range(8):
        for b in range(8):
            if a % 2 == b % 2:
                screen.blit(background, (a * 80 + 2.5, b * 80 + 2.5))
            else:
                screen.blit(dark_background, (a * 80 + 2.5, b * 80 + 2.5))

            rect = pygame.Rect(a * 80, b * 80, 80, 80)
            pygame.draw.rect(screen, black, rect, 5)

    try:
        red_1
    except NameError:
        pass
    else:
        red_1.create()

    try:
        red_2
    except NameError:
        pass
    else:
        red_2.create()

    try:
        red_3
    except NameError:
        pass
    else:
        red_3.create()

    try:
        red_4
    except NameError:
        pass
    else:
        red_4.create()

    try:
        red_5
    except NameError:
        pass
    else:
        red_5.create()

    try:
        red_6
    except NameError:
        pass
    else:
        red_6.create()

    try:
        red_7
    except NameError:
        pass
    else:
        red_7.create()

    try:
        red_8
    except NameError:
        pass
    else:
        red_8.create()

    try:
        red_9
    except NameError:
        pass
    else:
        red_9.create()

    try:
        red_10
    except NameError:
        pass
    else:
        red_10.create()

    try:
        red_11
    except NameError:
        pass
    else:
        red_11.create()

    try:
        red_12
    except NameError:
        pass
    else:
        red_12.create()

    try:
        black_1
    except NameError:
        pass
    else:
        black_1.create()

    try:
        black_2
    except NameError:
        pass
    else:
        black_2.create()

    try:
        black_3
    except NameError:
        pass
    else:
        black_3.create()

    try:
        black_4
    except NameError:
        pass
    else:
        black_4.create()

    try:
        black_5
    except NameError:
        pass
    else:
        black_5.create()

    try:
        black_6
    except NameError:
        pass
    else:
        black_6.create()

    try:
        black_7
    except NameError:
        pass
    else:
        black_7.create()

    try:
        black_8
    except NameError:
        pass
    else:
        black_8.create()

    try:
        black_9
    except NameError:
        pass
    else:
        black_9.create()

    try:
        black_10
    except NameError:
        pass
    else:
        black_10.create()

    try:
        black_11
    except NameError:
        pass
    else:
        black_11.create()

    try:
        black_12
    except NameError:
        pass
    else:
        black_12.create()

    try:
        invalid_move
    except NameError:
        pass
    else:
        try:
            move_canceled
        except NameError:
            pass
        else:
            if not invalid_move and not move_canceled and not game_over:
                red_turn = not red_turn
                has_won()

    # RECTS FOR OUTSIDE THE BOARD #
    pygame.draw.rect(screen, white, (640, 0, 160, 640), 0)
    pygame.draw.rect(screen, black, (640, 0, 80, 640), 5)
    pygame.draw.rect(screen, black, (640, 160, 80, 400), 5)
    pygame.draw.rect(screen, black, red_cancel_rect, 5)
    pygame.draw.rect(screen, black, black_cancel_rect, 5)
    pygame.draw.line(screen, black, (640, 320), (720, 320), 5)

    # TURN INDICATOR #

    if red_turn:
        pygame.draw.polygon(screen, (0, 0, 0), ((680, 184), (655, 290), (680, 272), (705, 290)))
        pygame.draw.polygon(screen, (254, 0, 0), ((680, 195), (660, 283), (680, 267), (700, 283)))

        pygame.draw.polygon(screen, (0, 0, 0), ((680, 456), (656, 350), (680, 368), (704, 350)), 2)

    else:
        pygame.draw.polygon(screen, (0, 0, 0), ((680, 456), (656, 350), (680, 368), (704, 350)))
        pygame.draw.polygon(screen, (105, 105, 105), ((680, 445), (660, 357), (680, 373), (700, 357)))

        pygame.draw.polygon(screen, (0, 0, 0), ((680, 184), (655, 290), (680, 272), (705, 290)), 2)

    # RED CANCEL MOVE #

    screen.blit(red_cancel, (645, 100))

    # BLACK CANCEL MOVE #

    screen.blit(black_cancel, (645, 500))

    pygame.display.flip()

    graphics_complete = True

# ---------- GAME ---------- #


on = True
sound_on = True
game_over = False

red_time = 9000
black_time = 9000

# CREATES PIECES #

red_1 = Piece('red', 1, 0)
red_2 = Piece('red', 3, 0)
red_3 = Piece('red', 5, 0)
red_4 = Piece('red', 7, 0)
red_5 = Piece('red', 0, 1)
red_6 = Piece('red', 2, 1)
red_7 = Piece('red', 4, 1)
red_8 = Piece('red', 6, 1)
red_9 = Piece('red', 1, 2)
red_10 = Piece('red', 3, 2)
red_11 = Piece('red', 5, 2)
red_12 = Piece('red', 7, 2)

black_1 = Piece('black', 0, 5)
black_2 = Piece('black', 2, 5)
black_3 = Piece('black', 4, 5)
black_4 = Piece('black', 6, 5)
black_5 = Piece('black', 1, 6)
black_6 = Piece('black', 3, 6)
black_7 = Piece('black', 5, 6)
black_8 = Piece('black', 7, 6)
black_9 = Piece('black', 0, 7)
black_10 = Piece('black', 2, 7)
black_11 = Piece('black', 4, 7)
black_12 = Piece('black', 6, 7)

graphics_complete = False

red_turn = True

# RUNS ACTUAL GAME #

while on:

    # BLITS GRAPHICS IF THEY HAVE CHANGED #

    if not graphics_complete:
        reblit()

    # SOUND CAN BE CHANGED INDEPENDENTLY OF BOARD, SO THE TWO ARE SEPARATED #

    if sound_on:
        screen.blit(sound_on_img, (643, 2.5))
    else:
        screen.blit(sound_off_img, (644, 2.5))

    pygame.draw.rect(screen, black, sound_rect, 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            (pos_x, pos_y) = pygame.mouse.get_pos()

            if pos_x in range(640, 720) and pos_y in range(0, 80):

                sound_on = not sound_on

                # REMOVES THE EXISTING SOUND ICON #

                pygame.draw.rect(screen, white, (642.5, 0, 80, 80), 0)

            if red_turn:

                try:
                    red_1
                except NameError:
                    pass
                else:
                    if red_1.rect.collidepoint(pos_x, pos_y):
                        red_1.reset()
                        red_1.move()

                try:
                    red_2
                except NameError:
                    pass
                else:
                    if red_2.rect.collidepoint(pos_x, pos_y):
                        red_2.reset()
                        red_2.move()

                try:
                    red_3
                except NameError:
                    pass
                else:
                    if red_3.rect.collidepoint(pos_x, pos_y):
                        red_3.reset()
                        red_3.move()

                try:
                    red_4
                except NameError:
                    pass
                else:
                    if red_4.rect.collidepoint(pos_x, pos_y):
                        red_4.reset()
                        red_4.move()

                try:
                    red_5
                except NameError:
                    pass
                else:
                    if red_5.rect.collidepoint(pos_x, pos_y):
                        red_5.reset()
                        red_5.move()

                try:
                    red_6
                except NameError:
                    pass
                else:
                    if red_6.rect.collidepoint(pos_x, pos_y):
                        red_6.reset()
                        red_6.move()

                try:
                    red_7
                except NameError:
                    pass
                else:
                    if red_7.rect.collidepoint(pos_x, pos_y):
                        red_7.reset()
                        red_7.move()

                try:
                    red_8
                except NameError:
                    pass
                else:
                    if red_8.rect.collidepoint(pos_x, pos_y):
                        red_8.reset()
                        red_8.move()

                try:
                    red_9
                except NameError:
                    pass
                else:
                    if red_9.rect.collidepoint(pos_x, pos_y):
                        red_9.reset()
                        red_9.move()

                try:
                    red_10
                except NameError:
                    pass
                else:
                    if red_10.rect.collidepoint(pos_x, pos_y):
                        red_10.reset()
                        red_10.move()

                try:
                    red_11
                except NameError:
                    pass
                else:
                    if red_11.rect.collidepoint(pos_x, pos_y):
                        red_11.reset()
                        red_11.move()

                try:
                    red_12
                except NameError:
                    pass
                else:
                    if red_12.rect.collidepoint(pos_x, pos_y):
                        red_12.reset()
                        red_12.move()

            else:

                try:
                    black_1
                except NameError:
                    pass
                else:
                    if black_1.rect.collidepoint(pos_x, pos_y):
                        black_1.reset()
                        black_1.move()

                try:
                    black_2
                except NameError:
                    pass
                else:
                    if black_2.rect.collidepoint(pos_x, pos_y):
                        black_2.reset()
                        black_2.move()

                try:
                    black_3
                except NameError:
                    pass
                else:
                    if black_3.rect.collidepoint(pos_x, pos_y):
                        black_3.reset()
                        black_3.move()

                try:
                    black_4
                except NameError:
                    pass
                else:
                    if black_4.rect.collidepoint(pos_x, pos_y):
                        black_4.reset()
                        black_4.move()

                try:
                    black_5
                except NameError:
                    pass
                else:
                    if black_5.rect.collidepoint(pos_x, pos_y):
                        black_5.reset()
                        black_5.move()

                try:
                    black_6
                except NameError:
                    pass
                else:
                    if black_6.rect.collidepoint(pos_x, pos_y):
                        black_6.reset()
                        black_6.move()

                try:
                    black_7
                except NameError:
                    pass
                else:
                    if black_7.rect.collidepoint(pos_x, pos_y):
                        black_7.reset()
                        black_7.move()

                try:
                    black_8
                except NameError:
                    pass
                else:
                    if black_8.rect.collidepoint(pos_x, pos_y):
                        black_8.reset()
                        black_8.move()

                try:
                    black_9
                except NameError:
                    pass
                else:
                    if black_9.rect.collidepoint(pos_x, pos_y):
                        black_9.reset()
                        black_9.move()

                try:
                    black_10
                except NameError:
                    pass
                else:
                    if black_10.rect.collidepoint(pos_x, pos_y):
                        black_10.reset()
                        black_10.move()

                try:
                    black_11
                except NameError:
                    pass
                else:
                    if black_11.rect.collidepoint(pos_x, pos_y):
                        black_11.reset()
                        black_11.move()

                try:
                    black_12
                except NameError:
                    pass
                else:
                    if black_12.rect.collidepoint(pos_x, pos_y):
                        black_12.reset()
                        black_12.move()

        pygame.display.flip()
