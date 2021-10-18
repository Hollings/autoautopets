from time import sleep

import pyautogui as gui


class Clickable:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def click(self, wait=False):
        game_window = gui.getWindowsWithTitle('Super Auto Pets')[0]

        gui.moveTo(self.x + game_window.left, self.y + game_window.top)
        gui.click()
        if wait:
            sleep(1)
