import json
from datetime import time
import random
from time import sleep
import numpy as np
import pyautogui as pag



def do_turn(n):
    print(f"turn {n}")
    if n == 0:
        print("Buying first turn")
        buy(0, 0, True)
        buy(0, 1, True)
        buy(0, 2, True)
        click_thing(coordinates['end'], True)
        click_thing(coordinates['team_names'][0])
        click_thing(coordinates['team_names'][1])
        click_thing(coordinates['end'], True)
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
        for i in sorted(iter(range(3)), key=lambda k: random.random()):
            for j in sorted(iter(range(5)), key=lambda k: random.random()):
                if gold_spent <= 7:
                    gold_spent += 3 if buy(i, j) else 0

        reroll()
        gold_spent += 1

        print("Buy round 2")
        for i in sorted(iter(range(3)), key=lambda k: random.random()):
            for j in sorted(iter(range(5)), key=lambda k: random.random()):
                if gold_spent <= 7:
                    gold_spent += 3 if buy(i, j) else 0

        # waste leftover gold
        for i in range(max(0, 15 - gold_spent)):
            click_thing(coordinates["roll"])
            # sleep(0.1)

        click_thing(coordinates['end'], True)


#
# while True:
#     get_mouse_location()
#     sleep(1)

#     Point(x=1507, y=642)


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
def calibrate():
    input("main menu")
    coordinates['play'] = list(pag.center(list(pag.locateOnScreen('images/play.png', confidence=0.975))))

    input("Show sell button")
    coordinates['sell'] = list(pag.center(list(pag.locateOnScreen('images/sell.png', confidence=0.975))))

    # TURN SCREEN
    input("open all slots on store and team, then press enter")
    slots = list(pag.locateAllOnScreen('images/empty_slot.png', confidence=0.975))
    i = 0
    # get horiz offset for first two slots, and vertical offset for animals/shop
    x_offset = int(pag.center(slots[1])[0] - pag.center(slots[0])[0])
    y_offset = int(pag.center(slots[6])[1] - pag.center(slots[0])[1])

    # set first animal slot to window coords
    coordinates['animals'][0] = [int(pag.center(slots[0])[0] - sap_window.topleft.x),
                                 int(pag.center(slots[0])[1] - sap_window.topleft.y)]

    for i in range(1, 5):
        coordinates['animals'][i] = [coordinates['animals'][i - 1][0] + x_offset, coordinates['animals'][i - 1][1]]

    coordinates['store'][0] = [coordinates['animals'][0][0],
                               coordinates['animals'][0][1] + y_offset]

    for i in range(1, 7):
        coordinates['store'][i] = [coordinates['store'][i - 1][0] + x_offset, coordinates['store'][i - 1][1]]

    coordinates['end'] = list(pag.center(list(pag.locateOnScreen('images/end.png', confidence=0.975))))
    coordinates['roll'] = list(pag.center(list(pag.locateOnScreen('images/roll.png', confidence=0.975))))

    # BATTLE SCREEN
    input("battle screen against grass")
    coordinates['fast_forward'] = list(pag.center(list(pag.locateOnScreen('images/fast_forward.png', confidence=0.975))))

    print(json.dumps(coordinates, cls=NpEncoder))


# calibrate()
# buy(1,1, True, True)
# move_window_coords(coordinates['store'][1])
# print(slot_filled(coordinates['store'][0]))
# render_field(True)


# for i in range(5):
#     move_window_coords(coordinates['animals'][i])
# for i in range(7):
#     move_window_coords(coordinates['store'][i])
# buy(0,1)

# click_thing(coordinates['store'][0])
# buy(0, 2)

# do_turn(1)
# calibrate()
move_window_coords(coordinates['end'])

exit()


def play_game():
    turns = 0
    start_from_main_menu()
    sleep(2)
    end = False
    while not end:
        do_turn(turns)
        turns += 1
        end = battle_wait()
    sleep(5)


for _ in range(1):
    play_game()
