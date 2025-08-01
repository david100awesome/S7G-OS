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
    "Falling Blocks",
    "Blackjack",
    "Texas Hold'em",
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

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}

def create_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]

def card_str(card):
    return f"{card[0]}{card[1]}"

def hand_to_str(hand):
    return ' '.join(card_str(c) for c in hand)

# Poker hand evaluation (same as before, omitted here for brevity)
# Copy the get_hand_rank() and compare_hands() functions from previous message here

# Betting options for player UI
BETTING_OPTIONS = ["Check", "Bet", "Call", "Fold"]

def get_player_action(can_check, can_call):
    selected = 0
    while True:
        g.clear()
        g.draw_text(10, 10, "Choose action:")
        for i, option in enumerate(BETTING_OPTIONS):
            # Disable options not valid for current state
            valid = True
            if option == "Check" and not can_check:
                valid = False
            if option == "Call" and not can_call:
                valid = False
            color = g.WHITE if i != selected else g.BLUE
            if not valid:
                color = g.GRAY
            g.set_color(color)
            g.draw_text(10, 40 + i * 20, option)
        g.show()

        key = sys.wait_for_key()
        if key == "up":
            selected = (selected - 1) % len(BETTING_OPTIONS)
        elif key == "down":
            selected = (selected + 1) % len(BETTING_OPTIONS)
        elif key == "enter":
            choice = BETTING_OPTIONS[selected]
            if (choice == "Check" and can_check) or (choice == "Call" and can_call) or choice in ("Bet", "Fold"):
                return choice
        elif key == "esc":
            return "Fold"

def ai_decision(ai_hand, community, pot, current_bet, ai_chips, player_bet):
    # Very simple AI logic with bluff chance
    bluff_chance = 0.1
    hand_strength = evaluate_hand_strength(ai_hand + community)
    # hand_strength: 0-1 scale (1 best)
    if random.random() < bluff_chance:
        # Bluff: raise if chips allow
        if ai_chips > current_bet:
            return "Bet"
    if hand_strength > 0.7:
        if current_bet > 0:
            return "Call"
        else:
            return "Bet"
    elif hand_strength > 0.4:
        if current_bet > 0:
            return "Call"
        else:
            return "Check"
    else:
        if current_bet > 0:
            return "Fold"
        else:
            return "Check"

def evaluate_hand_strength(cards):
    # Simplified hand strength evaluator: 0 (worst) to 1 (best)
    rank, vals = get_hand_rank(cards)
    return rank / 9.0  # max rank = 9 (royal flush)

def texas_holdem_betting():
    # Setup
    player_chips = 100
    ai_chips = 100
    big_blind = 10

    while player_chips > 0 and ai_chips > 0:
        # Initialize deck and hands
        deck = create_deck()
        random.shuffle(deck)
        pot = 0
        current_bet = 0

        player_hand = [deck.pop(), deck.pop()]
        ai_hand = [deck.pop(), deck.pop()]

        burn = deck.pop()
        flop = [deck.pop(), deck.pop(), deck.pop()]
        burn = deck.pop()
        turn = [deck.pop()]
        burn = deck.pop()
        river = [deck.pop()]
        community = []

        # Posting blinds (simplified: player posts small blind, AI posts big blind)
        player_chips -= big_blind // 2
        ai_chips -= big_blind
        pot += big_blind + (big_blind // 2)
        current_bet = big_blind

        # Show hole cards
        show_cards = True

        def display_state(stage):
            g.clear()
            g.draw_text(10, 10, f"Chips: You={player_chips} AI={ai_chips} Pot={pot}")
            g.draw_text(10, 30, "Your Hand:")
            g.draw_text(10, 50, hand_to_str(player_hand))
            g.draw_text(10, 70, f"Community Cards: {hand_to_str(community)}")
            g.draw_text(10, 100, f"Stage: {stage}")
            g.show()

        # Pre-flop betting round
        community = []
        display_state("Pre-Flop")
        # Player action
        action = get_player_action(can_check=False, can_call=False)  # can't check or call pre-flop
        if action == "Fold":
            g.clear()
            g.draw_text(50, 100, "You folded. AI wins the pot.")
            g.show()
            ai_chips += pot
            sys.wait_for_key()
            continue
        elif action == "Bet":
            bet_amount = big_blind  # fixed bet size for simplicity
            player_chips -= bet_amount
            pot += bet_amount
            current_bet = bet_amount
            # AI responds
            ai_act = ai_decision(ai_hand, community, pot, current_bet, ai_chips, bet_amount)
            if ai_act == "Fold":
                g.clear()
                g.draw_text(50, 100, "AI folded. You win the pot!")
                g.show()
                player_chips += pot
                sys.wait_for_key()
                continue
            elif ai_act == "Call":
                ai_chips -= bet_amount
                pot += bet_amount
            elif ai_act == "Bet":
                # AI raises (not implemented fully, just call for now)
                ai_chips -= bet_amount
                pot += bet_amount
        elif action == "Check":
            pass

        # Flop
        community = flop
        display_state("Flop")
        sys.wait_for_key()

        # Player action post-flop (can check or call)
        action = get_player_action(can_check=True, can_call=(current_bet>0))
        if action == "Fold":
            g.clear()
            g.draw_text(50, 100, "You folded. AI wins the pot.")
            g.show()
            ai_chips += pot
            sys.wait_for_key()
            continue
        elif action == "Bet":
            bet_amount = big_blind
            player_chips -= bet_amount
            pot += bet_amount
            current_bet = bet_amount
        elif action == "Call":
            call_amount = current_bet
            player_chips -= call_amount
            pot += call_amount
        elif action == "Check":
            pass

        # AI action post-flop (simplified)
        ai_act = ai_decision(ai_hand, community, pot, current_bet, ai_chips, 0)
        if ai_act == "Fold":
            g.clear()
            g.draw_text(50, 100, "AI folded. You win the pot!")
            g.show()
            player_chips += pot
            sys.wait_for_key()
            continue
        elif ai_act == "Bet":
            bet_amount = big_blind
            ai_chips -= bet_amount
            pot += bet_amount
            current_bet = bet_amount
        elif ai_act == "Call":
            ai_chips -= current_bet
            pot += current_bet
        elif ai_act == "Check":
            pass

        # Turn
        community = flop + turn
        display_state("Turn")
        sys.wait_for_key()

        # River
        community = flop + turn + river
        display_state("River")
        sys.wait_for_key()

        # Showdown
        g.clear()
        g.draw_text(10, 10, "Showdown!")
        g.draw_text(10, 30, f"Your Hand: {hand_to_str(player_hand)}")
        g.draw_text(10, 50, f"Dealer Hand: {hand_to_str(ai_hand)}")
        g.draw_text(10, 70, f"Community Cards: {hand_to_str(community)}")
        g.show()
        time.sleep(2)

        winner = compare_hands(player_hand + community, ai_hand + community)

        if winner == 1:
            g.draw_text(50, 100, "You win the pot!")
            player_chips += pot
        elif winner == 2:
            g.draw_text(50, 100, "AI wins the pot!")
            ai_chips += pot
        else:
            g.draw_text(50, 100, "It's a tie! Pot is split.")
            player_chips += pot // 2
            ai_chips += pot // 2
        g.show()
        sys.wait_for_key()

    g.clear()
    if player_chips <= 0:
        g.draw_text(50, 100, "You ran out of chips. Game Over!")
    else:
        g.draw_text(50, 100, "AI ran out of chips. You Win!")
    g.show()
    sys.wait_for_key()

def get_hand_rank(cards):
    """Evaluate best 5-card poker hand rank from 7 cards"""
    # cards = list of (rank, suit)
    from collections import Counter
    ranks = [c[0] for c in cards]
    suits = [c[1] for c in cards]
    rank_vals = sorted([RANK_VALUES[r] for r in ranks], reverse=True)
    counts = Counter(ranks)
    counts_sorted = sorted(counts.values(), reverse=True)
    flush = any(suits.count(s) >= 5 for s in suits)
    # Straight check helper
    def is_straight(vals):
        vals = sorted(set(vals), reverse=True)
        for i in range(len(vals) - 4):
            window = vals[i:i+5]
            if window[0] - window[4] == 4:
                return window[0]
        # Special case: A-2-3-4-5 straight
        if set([14, 2, 3, 4, 5]).issubset(vals):
            return 5
        return None

    # Convert ranks to numeric values for straight detection, Ace high=14
    numeric_ranks = [RANK_VALUES[r] for r in ranks]
    numeric_ranks = [14 if r == 14 else r for r in numeric_ranks]  # Ace high

    straight_high = is_straight(numeric_ranks)

    # Check flush suits and get flush cards if flush exists
    flush_suit = None
    flush_cards = []
    for s in SUITS:
        if suits.count(s) >= 5:
            flush_suit = s
            flush_cards = [RANK_VALUES[c[0]] for c in cards if c[1] == s]
            flush_cards.sort(reverse=True)
            break

    # Check straight flush
    if flush_suit and flush_cards:
        sf_high = is_straight(flush_cards)
        if sf_high:
            if sf_high == 14:
                return (9, [sf_high])  # Royal flush (straight flush ace-high)
            else:
                return (8, [sf_high])  # Straight flush

    # Four of a kind
    if counts_sorted[0] == 4:
        quad_rank = [RANK_VALUES[r] for r, c in counts.items() if c == 4][0]
        kickers = sorted([RANK_VALUES[r] for r, c in counts.items() if c != 4], reverse=True)
        return (7, [quad_rank] + kickers)

    # Full house
    if counts_sorted[0] == 3 and counts_sorted[1] >= 2:
        triple_rank = max([RANK_VALUES[r] for r, c in counts.items() if c == 3])
        pair_rank = max([RANK_VALUES[r] for r, c in counts.items() if c >= 2 and RANK_VALUES[r] != triple_rank])
        return (6, [triple_rank, pair_rank])

    # Flush
    if flush_suit:
        top5 = flush_cards[:5]
        return (5, top5)

    # Straight
    if straight_high:
        return (4, [straight_high])

    # Three of a kind
    if counts_sorted[0] == 3:
        triple_rank = [RANK_VALUES[r] for r, c in counts.items() if c == 3][0]
        kickers = sorted([RANK_VALUES[r] for r, c in counts.items() if c != 3], reverse=True)[:2]
        return (3, [triple_rank] + kickers)

    # Two pair
    pairs = sorted([RANK_VALUES[r] for r, c in counts.items() if c == 2], reverse=True)
    if len(pairs) >= 2:
        kickers = sorted([RANK_VALUES[r] for r, c in counts.items() if c == 1], reverse=True)
        return (2, pairs[:2] + kickers[:1])

    # One pair
    if counts_sorted[0] == 2:
        pair_rank = [RANK_VALUES[r] for r, c in counts.items() if c == 2][0]
        kickers = sorted([RANK_VALUES[r] for r, c in counts.items() if c == 1], reverse=True)[:3]
        return (1, [pair_rank] + kickers)

    # High card
    high_cards = sorted([RANK_VALUES[r] for r in ranks], reverse=True)[:5]
    return (0, high_cards)

def compare_hands(hand1, hand2):
    """Return 1 if hand1 wins, 2 if hand2 wins, 0 if tie"""
    rank1, vals1 = get_hand_rank(hand1)
    rank2, vals2 = get_hand_rank(hand2)
    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return 2
    else:
        # Compare kicker values
        for v1, v2 in zip(vals1, vals2):
            if v1 > v2:
                return 1
            elif v2 > v1:
                return 2
        return 0

def blackjack():
    def draw_card():
        value = random.choice(["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"])
        return value

    def card_value(card):
        if card in ["J", "Q", "K"]:
            return 10
        elif card == "A":
            return 11
        else:
            return int(card)

    def hand_total(hand):
        total = sum(card_value(c) for c in hand)
        # Handle aces
        aces = hand.count("A")
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    # Deal hands
    player = [draw_card(), draw_card()]
    dealer = [draw_card(), draw_card()]

    while True:
        g.clear()
        g.draw_text(10, 10, f"Your Hand: {' '.join(player)}")
        g.draw_text(10, 30, f"Dealer: {dealer[0]} ?")
        g.draw_text(10, 60, f"Total: {hand_total(player)}")
        g.draw_text(10, 90, "← Hit    → Stand")
        g.show()

        if hand_total(player) > 21:
            break

        key = ""
        while not key:
            if sys.keydown("left"):
                key = "hit"
            elif sys.keydown("right"):
                key = "stand"
            time.sleep(0.05)

        if key == "hit":
            player.append(draw_card())
        else:
            break

    # Dealer plays
    while hand_total(dealer) < 17:
        dealer.append(draw_card())

    # Final result
    g.clear()
    g.draw_text(10, 10, f"Your Hand: {' '.join(player)} = {hand_total(player)}")
    g.draw_text(10, 40, f"Dealer: {' '.join(dealer)} = {hand_total(dealer)}")

    player_total = hand_total(player)
    dealer_total = hand_total(dealer)

    if player_total > 21:
        result = "You bust!"
    elif dealer_total > 21 or player_total > dealer_total:
        result = "You win!"
    elif player_total == dealer_total:
        result = "Push!"
    else:
        result = "You lose!"

    g.draw_text(10, 80, result)
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

def falling_blocks():
    player_x = SCREEN_W // 2
    block_x = random.randint(0, SCREEN_W - 10)
    block_y = 0
    speed = 5
    score = 0

    while True:
        g.clear()
        g.set_color(g.BLUE)
        g.fill_rect(player_x, SCREEN_H - 10, 20, 10)  # player
        g.set_color(g.RED)
        g.fill_rect(block_x, block_y, 10, 10)  # falling block
        g.draw_text(10, 10, f"Score: {score}")
        g.show()
        time.sleep(0.05)

        block_y += speed
        if sys.keydown("left"): player_x -= 5
        if sys.keydown("right"): player_x += 5
        player_x = max(0, min(SCREEN_W - 20, player_x))

        # Collision
        if (SCREEN_H - 10 < block_y + 10 and
            player_x < block_x + 10 and
            player_x + 20 > block_x):
            break

        if block_y > SCREEN_H:
            block_y = 0
            block_x = random.randint(0, SCREEN_W - 10)
            score += 1

    g.clear()
    g.draw_text(90, 100, f"Game Over! Score: {score}")
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
                    falling_blocks()
                elif cursor == 7:
                    blackjack()
                elif cursor == 8:
                    texas_holdem_betting()
                elif cursor == 9:
                    screen = "main"; cursor = 0
        elif key == "esc":
            screen = "main"
            cursor = 0

def boot_screen():
    g.set_background(g.GRAY)
    g.clear()
    g.set_color(g.WHITE)
    g.draw_text(100, 100, "s7g OS is booting...")
    g.show()
    time.sleep(2)

boot_screen()
main()
