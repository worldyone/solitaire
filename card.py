import flet as ft
CARD_WIDTH = 70
CARD_HEIGHT = 100
DROP_PROXIMITY = 20
CARD_OFFSET = 20


class Card(ft.GestureDetector):
    def __init__(self, solitaire, color):
        super().__init__()
        self.slot = None
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.left = None
        self.top = None
        self.solitaire = solitaire
        self.color = color
        self.content = ft.Container(
            bgcolor=self.color, width=CARD_WIDTH, height=CARD_HEIGHT)
        self.draggable_pile = [self]

    def move_on_top(self):
        for card in self.draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)
        self.solitaire.update()

    def bounce_back(self):
        """Returns card to its original position"""
        for card in self.draggable_pile:
            self.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
            self.left = self.slot.left
        self.solitaire.update()

    def place(self, slot):
        for card in self.draggable_pile:
            card.top = slot.top + len(slot.pile) * CARD_OFFSET
            card.left = slot.left

            # remove card from it's original slot, if exists
            if self.slot is not None:
                self.slot.pile.remove(self)

            # change card's slot to a new slot
            self.slot = slot

            # add card to the new slot's pile
            slot.pile.append(self)

    def start_drag(self, e: ft.DragStartEvent):
        self.move_on_top()
        self.update()

    def drag(self, e: ft.DragUpdateEvent):
        for card in self.draggable_pile:
            card.top = (max(0, self.top + e.delta_y) +
                        self.draggable_pile.index(card) * CARD_OFFSET)
            card.left = max(0, self.left + e.delta_x)
            self.solitaire.update()

    def get_draggable_pile(self):
        if self.slot is not None:
            self.draggable_pile = self.slot.pile[self.slot.pile.index(self):]
        else:
            self.draggable_pile = [self]

    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.slots:
            if (abs(self.top - slot.top) < DROP_PROXIMITY
                    and abs(self.left - slot.left) < DROP_PROXIMITY):
                self.place(slot)
                self.update()
                return

        self.bounce_back()
        self.update()
