import json
from datetime import time
import random
from time import sleep

import pyautogui as pag

sap_window = pag.getWindowsWithTitle('Super Auto Pets')[0]
sap_window.resizeTo(1400, 850)

pag.PAUSE = 0.1

# Percentage of window
button = {
    "team_names": [
        (262, 327),
        (262, 553)
    ],
    "play": (700, 255),
    "end": (1234, 777),
    "sell": (850, 766),
    "roll": (161, 765),
    "store": [
        (342, 498),
        (442, 498),
        (552, 498),
        (662, 498),
        (772, 498),
        (882, 498),
        (992, 498),
    ],
    "animals": [
        (370, 394),
        (480, 394),
        (590, 394),
        (700, 394),
        (810, 394),
    ],
    "fast_forward": (970, 136),
    "pause": (590, 133),
    "none": (160, 340)
}

button = json.loads('{"team_names": [[373, 328], [368, 553]], "play": [1237, 771], "end": [1237, 771], "sell": [893, 770], "roll": [195, 766], "store": [[359, 498], [467, 499], [574, 500], [672, 500], [781, 496], [869, 492], [993, 497]], "animals": [[381, 399], [485, 399], [590, 398], [697, 399], [804, 397]], "fast_forward": [958, 150], "pause": [597, 157], "none": [675, 826]}')


def get_pixel_coordinates_of_objects():
    for key, value in button.items():
        if type(value) == list:
            for i in range(len(value)):
                input(f"{key} {i}")
                sleep(5)
                button[key][i] = get_mouse_location()
        else:
            input(key)
            sleep(5)
            button[key] = get_mouse_location()
    print(button)


def move_window_coords(coords):
    pag.moveTo(sap_window.topleft.x + coords[0],
               sap_window.topleft.y + coords[1])


#
# def moveTo(coords):
#     pag.moveTo(coords)

def get_mouse_location():
    pos = pag.position()
    x = pos.x - sap_window.topleft.x
    y = pos.y - sap_window.topleft.y
    print(f"{x}, {y}")
    get_color((x, y))
    return (x, y)
    # print(pixel_matches_color(pos, (255, 255, 255), 10))


def start_from_main_menu():
    click_thing(button['play'], True)


def click_thing(thing, wait=False):
    move_window_coords(thing)
    pag.click()
    if wait:
        sleep(1)


def buy(store_animal, destination, wait=False):
    field = render_field()
    if store_animal > 5:
        wait = True
    if slot_filled(button['store'][store_animal]):
        # TODO check for upgrade
        click_thing(button['store'][store_animal])
        click_thing(button['animals'][destination], wait)
        if field != render_field():
            print("Bought")
            return True
        return False


def sell(animal):
    if slot_filled(button['animals'][animal]):
        click_thing(button['animals'][animal])
        click_thing(button["sell"])
        # TODO dont need to check it, assume its empty now


def combine(animal, destination):
    if slot_filled(button['animals'][animal]) and slot_filled(button['animals'][destination]):
        click_thing(button['animals'][animal])
        click_thing(button['animals'][destination])


def try_combine_all():
    for i in range(5):
        for j in range(5):
            combine(i, j)


def slot_filled(coords):
    # move_window_coords(coords)
    return pixel_matches_color(coords, (255, 255, 255), 10)
    # return get_color(coords) == (255,255,255)


def battle_wait():
    ff = False
    while True:
        color = get_color(button["end"])
        sleep(1)
        # check for ff button and click it
        if not ff and get_color(button["pause"]) == (255, 255, 255):
            click_thing(button["fast_forward"])
            ff = True
        click_thing(button["sell"])
        if color == (255, 106, 0):
            # new round
            return False
        elif color == (0, 39, 58):
            # game over
            return True


def get_color(coords):
    real_coords = (sap_window.topleft.x + coords[0],
                   sap_window.topleft.y + coords[1])
    im = pag.screenshot()
    px = im.getpixel(real_coords)
    return px


def pixel_matches_color(coords, color, tolerance):
    real_coords = (sap_window.topleft.x + coords[0],
                   sap_window.topleft.y + coords[1])
    return pag.pixelMatchesColor(real_coords[0], real_coords[1], color, tolerance=tolerance)


def reroll():
    click_thing(button["roll"])


def render_field(print_field=False):
    line = ""
    for i in range(5):
        line += " O " if slot_filled(button['animals'][i]) else " _ "
    line += "\n"
    for i in range(7):
        line += " O " if slot_filled(button['store'][i]) else " _ "
    if print_field:
        print("======================")
        print(line)
    return (line)


def do_turn(n):
    print(f"turn {n}")
    if n == 0:
        print("Buying first turn")
        buy(0, 0, True)
        buy(0, 1, True)
        buy(0, 2, True)
        click_thing(button['end'], True)
        click_thing(button['team_names'][0])
        click_thing(button['team_names'][1])
        click_thing(button['end'], True)
    else:
        gold_spent = 0
        # TODO: make this weighted and more random
        # TODO: only sell when field is full
        # sell one random animal
        if n > 1:
            sell_slot = random.randint(0, 4)
            print(f"Selling {sell_slot} animal")
            sell(sell_slot)

        # Try to upgrade something
        print("Trying to upgrade")
        try_combine_all()

        # try to buy anything a few times
        print("Buy round 1'")
        for i in sorted(iter(range(5)), key=lambda k: random.random()):
            for j in sorted(iter(range(5)), key=lambda k: random.random()):
                if gold_spent <= 7:
                    gold_spent += 3 if buy(i, j) else 0

        reroll()
        gold_spent += 1

        print("Buy round 2")
        for i in sorted(iter(range(7)), key=lambda k: random.random()):
            for j in sorted(iter(range(5)), key=lambda k: random.random()):
                if gold_spent <= 7:
                    gold_spent += 3 if buy(i, j) else 0

        # waste leftover gold
        for i in range(max(0, 15 - gold_spent)):
            click_thing(button["roll"])
            # sleep(0.1)

        click_thing(button['end'], True)


#
# while True:
#     get_mouse_location()
#     sleep(2)
# click_thing(button["sell"])
# update_slots()
# render_field(True)
# get_pixel_coordinates_of_objects()
# exit()


#

# sleep(5)
# do_turn(3)
# battle_wait()
# exit()
# do_turn(3)
# exit()


def play_game():
    turns = 0
    # start_from_main_menu()
    sleep(2)
    end = False
    while not end:
        do_turn(turns)
        turns += 1
        end = battle_wait()
    sleep(5)


for _ in range(1):
    play_game()
