import flet as ft
SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.top = top
        self.left = left
        self.border = ft.border.all(1)
