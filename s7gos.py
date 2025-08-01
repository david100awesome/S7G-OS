import os
import random
import time
import math
import ti_system as sys
import ti_graphics as g

# --- Constants ---
SCREEN_W = 320
SCREEN_H = 240
BG_COLOR = g.GRAY
WHITE = g.WHITE
YELLOW = g.YELLOW

# --- Menu Items ---
main_menu = ["Games", "About", "Shutdown"]
games_menu = [
    "Flappy Bird",
    "Number Guess",
    "Reaction Test",
    "Snake",
    "Pong",
    "Dice Roller",
    "Back"
]

# --- State ---
screen = "main"
cursor = 0

# --- Helpers ---
def draw_menu(title, items, selected):
    g.clear()
    g.set_color(WHITE)
    g.draw_text(10, 10, f"[ s7g OS ] {title}", size="small")
    for i, item in enumerate(items):
        y = 40 + i * 25
        color = YELLOW if i == selected else WHITE
        g.set_color(color)
        g.draw_text(20, y, item)
    g.show()

def wait_key():
    while True:
        key = sys.wait_for_key()
        if key in ("up", "down", "enter", "esc"):
            return key

def dice_roller():
    while True:
        g.clear()
        roll = random.randint(1, 6)
        g.set_color(WHITE)
        g.draw_text(100, 100, f"You rolled a {roll}")
        g.show()
        time.sleep(0.3)
        key = sys.wait_for_key()
        if key == "esc": break

def snake_game():
    block = 10
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "right"
    food = (random.randint(0, (SCREEN_W - block)//block) * block,
            random.randint(0, (SCREEN_H - block)//block) * block)
    alive = True

    while alive:
        g.clear()
        g.set_color(g.GREEN)
        for segment in snake:
            g.fill_rect(segment[0], segment[1], block, block)
        g.set_color(g.RED)
        g.fill_rect(food[0], food[1], block, block)
        g.show()
        time.sleep(0.1)

        # Input
        if sys.keydown("up") and direction != "down":
            direction = "up"
        elif sys.keydown("down") and direction != "up":
            direction = "down"
        elif sys.keydown("left") and direction != "right":
            direction = "left"
        elif sys.keydown("right") and direction != "left":
            direction = "right"

        # Move snake
        head_x, head_y = snake[0]
        if direction == "up": head_y -= block
        elif direction == "down": head_y += block
        elif direction == "left": head_x -= block
        elif direction == "right": head_x += block
        new_head = (head_x, head_y)

        # Collision
        if (new_head in snake or
            head_x < 0 or head_x >= SCREEN_W or
            head_y < 0 or head_y >= SCREEN_H):
            break

        snake.insert(0, new_head)
        if new_head == food:
            food = (random.randint(0, (SCREEN_W - block)//block) * block,
                    random.randint(0, (SCREEN_H - block)//block) * block)
        else:
            snake.pop()

    g.clear()
    g.draw_text(90, 100, f"Game Over! Score: {len(snake)-3}")
    g.show()
    sys.wait_for_key()

def pong_game():
    ball_x = SCREEN_W // 2
    ball_y = SCREEN_H // 2
    ball_dx = 4
    ball_dy = 3

    paddle_h = 40
    paddle_w = 8
    p1_y = SCREEN_H // 2 - paddle_h // 2
    ai_y = SCREEN_H // 2 - paddle_h // 2

    p1_score = 0
    ai_score = 0

    ai_speed = 2  # Adjust to make AI easier/harder

    while True:
        g.clear()
        g.set_color(WHITE)

        # Draw paddles
        g.fill_rect(10, p1_y, paddle_w, paddle_h)
        g.fill_rect(SCREEN_W - 20, ai_y, paddle_w, paddle_h)

        # Draw ball
        g.fill_rect(ball_x, ball_y, 8, 8)

        # Draw score
        g.draw_text(120, 10, f"{p1_score} - {ai_score}")
        g.show()
        time.sleep(0.03)

        # Player movement
        if sys.keydown("up"): p1_y -= 4
        if sys.keydown("down"): p1_y += 4
        p1_y = max(0, min(SCREEN_H - paddle_h, p1_y))

        # AI movement (simple tracking)
        if ball_y > ai_y + paddle_h // 2:
            ai_y += ai_speed
        elif ball_y < ai_y + paddle_h // 2:
            ai_y -= ai_speed
        ai_y = max(0, min(SCREEN_H - paddle_h, ai_y))

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Wall bounce
        if ball_y <= 0 or ball_y >= SCREEN_H - 8:
            ball_dy *= -1

        # Paddle collision
        if 10 < ball_x < 10 + paddle_w and p1_y <= ball_y <= p1_y + paddle_h:
            ball_dx *= -1
        if SCREEN_W - 20 - 8 < ball_x < SCREEN_W - 20 and ai_y <= ball_y <= ai_y + paddle_h:
            ball_dx *= -1

        # Scoring
        if ball_x < 0:
            ai_score += 1
            ball_x, ball_y = SCREEN_W//2, SCREEN_H//2
            time.sleep(0.5)
        elif ball_x > SCREEN_W:
            p1_score += 1
            ball_x, ball_y = SCREEN_W//2, SCREEN_H//2
            time.sleep(0.5)

        if p1_score >= 5 or ai_score >= 5:
            g.clear()
            winner = "You" if p1_score > ai_score else "AI"
            g.draw_text(100, 100, f"{winner} Win!")
            g.show()
            sys.wait_for_key()
            break


# --- Game 1: Flappy Bird ---
def flappy_bird():
    g.clear()
    bird_y = SCREEN_H // 2
    velocity = 0
    gravity = 1
    flap_strength = -8
    pipe_x = SCREEN_W
    pipe_gap = 70
    pipe_top = random.randint(30, SCREEN_H - pipe_gap - 30)
    score = 0
    clock = time.monotonic

    while True:
        g.clear()
        # Draw Bird
        g.set_color(g.YELLOW)
        g.fill_rect(50, bird_y, 10, 10)

        # Draw Pipes
        g.set_color(g.WHITE)
        g.fill_rect(pipe_x, 0, 20, pipe_top)
        g.fill_rect(pipe_x, pipe_top + pipe_gap, 20, SCREEN_H)

        # Score
        g.draw_text(10, 10, f"Score: {score}")

        g.show()
        time.sleep(0.05)

        # Physics
        velocity += gravity
        bird_y += velocity

        # Pipe Movement
        pipe_x -= 5
        if pipe_x < -20:
            pipe_x = SCREEN_W
            pipe_top = random.randint(30, SCREEN_H - pipe_gap - 30)
            score += 1

        # Input
        if sys.keydown("enter"):
            velocity = flap_strength

        # Collision
        if bird_y < 0 or bird_y > SCREEN_H:
            break
        if 50 + 10 > pipe_x and 50 < pipe_x + 20:
            if bird_y < pipe_top or bird_y > pipe_top + pipe_gap:
                break

    g.clear()
    g.draw_text(80, 100, f"Game Over! Score: {score}")
    g.show()
    sys.wait_for_key()

# --- Game 2: Number Guess ---
def number_guess():
    g.clear()
    secret = random.randint(1, 100)
    tries = 0
    while True:
        guess = int(input("Guess (1-100): "))
        tries += 1
        g.clear()
        if guess < secret:
            g.draw_text(20, 100, "Too low!")
        elif guess > secret:
            g.draw_text(20, 100, "Too high!")
        else:
            g.draw_text(20, 100, f"Correct! Tries: {tries}")
            g.show()
            break
        g.show()
        time.sleep(1)
    sys.wait_for_key()

# --- Game 3: Reaction Test ---
def reaction_test():
    g.clear()
    g.draw_text(60, 100, "Wait for GREEN!")
    g.show()
    delay = random.uniform(2, 5)
    time.sleep(delay)
    g.clear()
    g.set_color(g.GREEN)
    g.draw_text(60, 100, "NOW! Press any key!")
    g.show()
    start = time.monotonic()
    sys.wait_for_key()
    end = time.monotonic()
    reaction = (end - start) * 1000
    g.clear()
    g.set_color(WHITE)
    g.draw_text(40, 100, f"Reaction: {int(reaction)} ms")
    g.show()
    sys.wait_for_key()

# --- About Screen ---
def about():
    g.clear()
    g.draw_text(50, 80, "s7g OS v1.0")
    g.draw_text(50, 110, "By You")
    g.draw_text(50, 140, "Dark Grey Theme")
    g.show()
    sys.wait_for_key()

# --- Main Loop ---
def main():
    global screen, cursor
    g.set_background(BG_COLOR)
    g.clear()
    g.show()

    while True:
        menu = main_menu if screen == "main" else games_menu
        draw_menu(screen.capitalize() + " Menu", menu, cursor)

        key = wait_key()
        if key == "up":
            cursor = (cursor - 1) % len(menu)
        elif key == "down":
            cursor = (cursor + 1) % len(menu)
        elif key == "enter":
            if screen == "main":
                if cursor == 0:
                    screen = "games"; cursor = 0
                elif cursor == 1:
                    screen = "math"; cursor = 0
                elif cursor == 2:
                    about()
                elif cursor == 3:
                    break
            elif screen == "games":
                if cursor == 0:
                    flappy_bird()
                elif cursor == 1:
                    number_guess()
                elif cursor == 2:
                    reaction_test()
                elif cursor == 3:
                    snake_game()
                elif cursor == 4:
                    pong_game()
                elif cursor == 5:
                    dice_roller()
                elif cursor == 6:
                    screen = "main"; cursor = 0
        elif key == "esc":
            screen = "main"
            cursor = 0

main()
