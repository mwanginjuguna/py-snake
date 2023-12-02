from tkinter import *
import random

# Initialize screen width
SCREEN_WIDTH = 500
# Initialize screen height
SCREEN_HEIGHT = 500
# Game Speed
GAME_SPEED = 200
# Initialize screen space
SPACE_SIZE = 20
# Initial body length of the snake
BODY_SIZE = 2
# Snake color
SNAKE_COLOR = '#00FF00'
# Food color
FOOD_COLOR = '#FFFF00'
# screen background color
SCREEN_BG_COLOR = '#000000'


# snake template definition
class Snake:
    def __init__(self) -> None:
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0,0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y,
                                             x+SPACE_SIZE,
                                             y+SPACE_SIZE,
                                             fill=SNAKE_COLOR,
                                             tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int((SCREEN_WIDTH/SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((SCREEN_HEIGHT/SPACE_SIZE)-1)) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x,y,
                           x+SPACE_SIZE,
                           y+SPACE_SIZE,
                           fill=FOOD_COLOR,
                           tags="food")


def next_turn(snake, food):
    x,y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x,y,
                                    x+SPACE_SIZE,
                                    y+SPACE_SIZE,
                                    fill=SNAKE_COLOR,
                                    tags="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text=f"Score: {score}")

        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(GAME_SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    """Check snake's collision and position."""

    x,y = snake.coordinates[0]

    if x < 0 or x >= SCREEN_WIDTH:
        return True
    elif y < 0 or y >= SCREEN_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,
                       canvas.winfo_height()/2,
                       font=("consolas", 70),
                       text="GAME OVER!", fill="red",
                       tags="gameover"
                       )



# Game Title
window = Tk()
window.title("Eden Snake Game ")

score = 0
direction = 'right'

# Display points scored in the game
label = Label(window, text=f"Score: {score}", font=('consolas', 10))

label.pack()

canvas = Canvas(window,
                bg=SCREEN_BG_COLOR,
                height=SCREEN_HEIGHT,
                width=SCREEN_WIDTH
                )
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))

snake = Snake()

food = Food()

next_turn(snake,food)


window.mainloop()
