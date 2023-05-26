# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "daydin",
        "color": "#EE8E0C",
        "head": "bendr",
        "tail": "freckled",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {
        "up": True,
        "down": True,
        "left": True,
        "right": True
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        print("neck left of head")
    if my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        print("neck right of head")
    if my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        print("neck below head")
    if my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        print("neck above head")
    # Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head['x'] == board_width - 1:
        is_move_safe['right'] = False
        print("board to the right of head")
    if my_head['x'] == 0:
        is_move_safe['left'] = False
        print("board to the left of head")
    if my_head['y'] == board_height - 1:
        is_move_safe['up'] = False
        print("board above head")
    if my_head['y'] == 0:
        is_move_safe['down'] = False
        print("board below head")

    # Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    for i, body_part in enumerate(my_body):
        if i > 1:
            if (my_head['x'] == body_part['x'] - 1 and my_head['y'] == body_part['y']):
                is_move_safe['right'] = False
                print("body right of head")
            if (my_head['x'] == body_part['x'] + 1 and my_head['y'] == body_part['y']):
                is_move_safe['left'] = False
                print("body left of head")
            if (my_head['x'] == body_part['x'] and my_head['y'] == body_part['y'] - 1):
                is_move_safe['up'] = False
                print("body above head")
            if (my_head['x'] == body_part['x'] and my_head['y'] == body_part['y'] + 1):
                is_move_safe['down'] = False
                print("body below head")
    # Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for opponent in opponents:
        if opponent['name'] != 'Newbie Snake':
            for body_part in opponent['body']:
                if (my_head['x'] == body_part['x'] - 1 and my_head['y'] == body_part['y']):
                    is_move_safe['right'] = False
                    print("opponent to the right of head")
                if (my_head['x'] == body_part['x'] + 1 and my_head['y'] == body_part['y']):
                    is_move_safe['left'] = False
                    print("opponent to the left of head")
                if (my_head['x'] == body_part['x'] and my_head['y'] == body_part['y'] - 1):
                    is_move_safe['up'] = False
                    print("opponent above head")
                if (my_head['x'] == body_part['x'] and my_head['y'] == body_part['y'] + 1):
                    is_move_safe['down'] = False
                    print("opponent below head")

    # Move towards food instead of random, to regain health and survive longer
    foods = game_state['board']['food']
    for i, food in enumerate(foods):
        if (my_head['x'] == food['x'] - 1 and my_head['y'] == food['y']):
            is_move_safe['right'] = True
            is_move_safe['left'] = False
            is_move_safe['up'] = False
            is_move_safe['down'] = False
            print("food right of head")
        if (my_head['x'] == food['x'] + 1 and my_head['y'] == food['y']):
            is_move_safe['right'] = False
            is_move_safe['left'] = True
            is_move_safe['up'] = False
            is_move_safe['down'] = False
            print("food left of head")
        if (my_head['x'] == food['x'] and my_head['y'] == food['y'] - 1):
            is_move_safe['right'] = False
            is_move_safe['left'] = False
            is_move_safe['up'] = True
            is_move_safe['down'] = False
            print("food above head")
        if (my_head['x'] == food['x'] and my_head['y'] == food['y'] + 1):
            is_move_safe['right'] = False
            is_move_safe['left'] = False
            is_move_safe['up'] = False
            is_move_safe['down'] = True
            print("food below head")
        print('is move safe?: ', is_move_safe)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end
    })
