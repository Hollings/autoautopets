import json
from datetime import time
import random
from time import sleep
import numpy as np
import pyautogui as gui

from clickable import Clickable
from field_slot import FieldSlot


class AutoPetsControl:
    def __init__(self):
        self.game_window = gui.getWindowsWithTitle('Super Auto Pets')[0]
        self.game_window.resizeTo(1400, 850)
        self.team = []
        self.shop = []
        self.ui = {}
        self.coordinates = json.load(open('coordinates.json'))
        self._initialize_object_coordinates()
        self.money = 10
        gui.PAUSE = 0.1

    def move_mouse_to(self, coords):
        gui.moveTo(self.game_window.topleft.x + coords[0], self.game_window.topleft.y + coords[1])

    def _screen_coords_to_window_coords(self, coords):
        return [int(coords[0] - self.game_window.topleft.x),
                int(coords[1] - self.game_window.topleft.y)]

    def _window_coords_to_screen_coords(self, coords):
        return [coords[0] + self.game_window.topleft.x,
                coords[1] + self.game_window.topleft.y]

    def _initialize_object_coordinates(self):
        for i in range(5):
            coords = self.coordinates["team"][i]
            abs_coords = self._window_coords_to_screen_coords(coords)
            self.team.append(FieldSlot(coords[0], coords[1], abs_coords[0], abs_coords[1]))
        for i in range(7):
            coords = self.coordinates["shop"][i]
            abs_coords = self._window_coords_to_screen_coords(coords)
            self.shop.append(FieldSlot(coords[0], coords[1], abs_coords[0], abs_coords[1]))

        self.ui['team_name_1'] = Clickable(self.coordinates["team_names"][0][0], self.coordinates["team_names"][0][1])
        self.ui['team_name_2'] = Clickable(self.coordinates["team_names"][1][0], self.coordinates["team_names"][1][1])
        self.ui['play'] = Clickable(self.coordinates["play"][0], self.coordinates["play"][1])
        self.ui['end'] = Clickable(self.coordinates["end"][0], self.coordinates["end"][1])
        self.ui['sell'] = Clickable(self.coordinates["sell"][0], self.coordinates["sell"][1])
        self.ui['roll'] = Clickable(self.coordinates["roll"][0], self.coordinates["roll"][1])
        self.ui['fast_forward'] = Clickable(self.coordinates["fast_forward"][0], self.coordinates["fast_forward"][1])
        self.ui['none'] = Clickable(self.coordinates["none"][0], self.coordinates["none"][1])

    def get_first_empty_team_slot(self):
        slot: FieldSlot
        for slot in self.team:
            if not slot.is_occupied():
                return slot

    def buy(self, shop_slot: FieldSlot, team_slot: FieldSlot, wait = True, force = False):
        # Check if buy was successful
        if force or (shop_slot.is_occupied() and not team_slot.is_occupied()):
            shop_slot.click()
            team_slot.click(wait)


    def buy_phase(self, buy_food):
        for i in range(3):
            space = self.get_first_empty_team_slot()
            if space:
                self.buy(self.shop[0], space)
            else:
                break

        if buy_food:
            print("buying food")
            sleep(1)
            self.buy(self.shop[5], self.team[random.randint(0, 4)], True, True)
            self.buy(self.shop[6], self.team[random.randint(0, 4)], True, True)


    def sell(self, team_slot: FieldSlot):
        if team_slot.is_occupied():
            team_slot.click()
            self.ui['sell'].click()

    def sell_phase(self):
        if random.randint(0, 3) == 0:
            self.sell(self.team[random.randint(0, 4)])

    def upgrade(self, team_slot_1: FieldSlot):
        if team_slot_1.is_occupied():
            for shop_animal in apc.shop:
                if shop_animal.animal() == team_slot_1.animal():
                    shop_animal.click()
                    team_slot_1.click()

    def upgrade_phase(self):
        for team_animal in self.team:
            self.upgrade(team_animal)

    def end_turn(self):
        self.ui['end'].click()

    def wait_for_battle(self):
        pass
        # ff = False
        # while True:
        #     color = get_color(coordinates["end"])
        #     sleep(1)
        #     # check for ff button and click it
        #     if not ff and get_color(coordinates["pause"]) == (255, 255, 255):
        #         click_thing(coordinates["fast_forward"])
        #         ff = True
        #     click_thing(coordinates["sell"])
        #     if color == (255, 106, 0):
        #         # new round
        #         return False
        #     elif color == (0, 39, 58):
        #         # game over
        #         return True

    def render_field(self):
        rendering = ""
        for i in range(5):
            rendering += "O" if self.team[i].is_occupied() else "_"
        rendering += "\n"
        for i in range(7):
            rendering += "O" if self.shop[i].is_occupied() else "_"
        print("======================")
        print(rendering)
        print("======================")

        return rendering

    def _get_relative_coords_of_image(self, image, confidence):
        abs_coords = list(gui.center(list(gui.locateOnScreen(image, confidence=confidence))))
        rel_coords = self._screen_coords_to_window_coords(abs_coords)
        return rel_coords

    def calibrate_coordinates(self):
        input("main menu")
        coordinates = self.coordinates
        coordinates['play'] = self._get_relative_coords_of_image('images/play.png', 0.975)

        input("Show sell button")
        coordinates['sell'] = self._get_relative_coords_of_image('images/sell.png', 0.975)

        # TURN SCREEN
        input("open all slots on store and team, then press enter")
        slots = list(gui.locateAllOnScreen('images/empty_slot.png', confidence=0.975))

        # get horiz offset for first two slots, and vertical offset for team/shop
        x_offset = int(gui.center(slots[1])[0] - gui.center(slots[0])[0])
        y_offset = int(gui.center(slots[6])[1] - gui.center(slots[0])[1])

        # Team animals
        coordinates['team'][0] = self._screen_coords_to_window_coords([gui.center(slots[0])[0],
                                                                       gui.center(slots[0])[1]])

        for i in range(1, 5):
            coordinates['team'][i] = [coordinates['team'][i - 1][0] + x_offset, coordinates['team'][i - 1][1]]

        # Shop animals
        coordinates['shop'][0] = [coordinates['team'][0][0],
                                   coordinates['team'][0][1] + y_offset]
        for i in range(1, 7):
            coordinates['shop'][i] = [coordinates['shop'][i - 1][0] + x_offset, coordinates['shop'][i - 1][1]]

        coordinates['end'] = self._get_relative_coords_of_image('images/end.png', 0.975)
        coordinates['roll'] = self._get_relative_coords_of_image('images/roll.png', 0.975)

        # BATTLE SCREEN
        input("battle screen against grass")
        coordinates['fast_forward'] = self._get_relative_coords_of_image('images/fast_forward.png', 0.975)

        # Let json dumps use int64
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NpEncoder, self).default(obj)

        print(json.dumps(coordinates, cls=NpEncoder))


if __name__ == '__main__':
    apc = AutoPetsControl()
    # apc.calibrate_coordinates()
    apc.sell_phase()
    for i in range(2):
        apc.upgrade_phase()
        apc.buy_phase(i>0)
        apc.ui['roll'].click()
    apc.ui['end'].click()
