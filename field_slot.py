from clickable import Clickable
import pyautogui as gui

class FieldSlot(Clickable):
    def __init__(self, x, y, abs_x, abs_y):
        super().__init__()
        self.name = ""
        self.x = x
        self.y = y
        self.absolute_x = abs_x
        self.absolute_y = abs_y
        self.coords = (x,y)
        self.color = (0, 0, 0)


    def is_occupied(self):
        return not gui.pixelMatchesColor(self.absolute_x, self.absolute_y - 30, (187, 178, 145), 10)

    def animal(self):
        return gui.pixel(self.absolute_x, self.absolute_y - 33)

