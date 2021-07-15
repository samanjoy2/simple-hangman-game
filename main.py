import pygame
import math
import random
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
# setup
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman GAME...")

# fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)
HINT_FONT = pygame.font.SysFont("comicsans", 30)

# image loader
bg = pygame.image.load("bg_images/"+"background.png")
bg1 = pygame.image.load("bg_images/"+"background2.png")
bg_win = pygame.image.load("bg_images/"+"background_win.png")
bg_lose = pygame.image.load("bg_images/"+"background_lose.png")
bg_backup = pygame.image.load("bg_images/"+"backgroundbackup.png")
imgs = []
for i in range(7):
    image = pygame.image.load("status_imgs/"+"hangman"+str(i)+".png")
    imgs.append(image)

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH-(RADIUS*2+GAP)*13)/2) 
starty = 400
A = 65 # ascii value of A
for i in range(26):
    x = startx + GAP *2 + (RADIUS*2+GAP) * (i%13)
    y = starty + ((i//13) * (GAP+RADIUS*2))
    letters.append([x, y, chr(A+i), True])

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game variables
hangman_status = 0
words = ["HELLO", "SAMAN", "PUTIMAS", "DORIME","PYTHON","CALCULATOR",
        "VALORANT","LAPTOP","NOTEBOOK"] # add words here
hints = ["adele's famous song", "this game's creators name", 
        "a banglish word; small fish", "a mythical god",
        "snake and programming language","used to do maths",
        "a famous fps game","portable pc","a movie name and a study material"] # add hints here
word = random.choice(words)
hint = "Hint: "+hints[words.index(word)]
guessed = []

# setting game variables to default
def set_default():
    global hangman_status
    global word
    global hint
    global guessed
    global letters
    global session

    hangman_status = 0
    word = random.choice(words)
    # print(word)
    hint = "Hint: "+hints[words.index(word)]
    # print(hint)
    guessed = []
    letters = []
    startx = round((WIDTH-(RADIUS*2+GAP)*13)/2) 
    starty = 400
    A = 65
    for i in range(26):
        x = startx + GAP *2 + (RADIUS*2+GAP) * (i%13)
        y = starty + ((i//13) * (GAP+RADIUS*2))
        letters.append([x, y, chr(A+i), True])
    

# pygame main loop

def draw():
    win.fill(WHITE)
    win.blit(bg, (0, 0))

    # draw title
    text = TITLE_FONT.render("Play Hangman plis", 1, BLACK)
    win.blit(text, (WIDTH/2-text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    text = HINT_FONT.render(hint, 1, BLACK)
    win.blit(text, (400, 280))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 2)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x-text.get_width()/2, y-text.get_height()/2))

    win.blit(imgs[hangman_status], (150, 100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    if message == "YOU WON EZ":
        win.blit(bg_win, (0, 0))
    elif message == "YOU LOST GG":
        win.blit(bg_lose, (0, 0))
    else:
        win.blit(bg_backup, (0, 0))
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2-text.get_width()/2, 
                    HEIGHT/2-text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def game():
    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        global hangman_status
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x-m_x)**2+(y-m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("YOU WON EZ")
            set_default()
            return

        if hangman_status == 6:
            display_message("YOU LOST GG")
            abc = "The word was "+word
            display_message(abc)
            set_default()
            return

run = True
while run:
    run = True
    win.fill(WHITE)
    win.blit(bg1, (0, 0))
    text = WORD_FONT.render("Would you like to play?", 1, BLACK)
    text1 = LETTER_FONT.render("Press SpaceKey to play", 1, BLACK)
    text2 = LETTER_FONT.render("Press Q to Quit", 1, BLACK)

    win.blit(text, (WIDTH/2-text.get_width()/2, 
    HEIGHT/2-text.get_height()/2-50))
    win.blit(text1, (WIDTH/2-text.get_width()/2+60, 
    HEIGHT/2-text.get_height()/2+50))
    win.blit(text2, (WIDTH/2-text.get_width()/2+60, 
    HEIGHT/2-text.get_height()/2+90))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game()
            if event.key == pygame.K_q:
                run = False

pygame.quit()