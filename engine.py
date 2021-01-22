from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
import math
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor, highlight: bool = False):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.highlight = highlight

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def update_highlight(self, x: int, y: int, radius: int) -> None:
        """Highlight area around point that is within a given radius"""
        self.highlight_clear()

        if not self.highlight:
            return None

        # Get starting coordinate and width and height of box to highlight
        box_x = x - radius - 1
        box_y = y - radius - 1
        width = radius ** 2
        height = radius ** 2

        # Bound box values to edges of the map
        min_x = max(0, box_x)
        max_x = min(box_x + width, self.game_map.width)
        min_y = max(0, box_y)
        max_y = min(box_y + height, self.game_map.height)

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                if math.sqrt((i - x) ** 2 + (j - y) ** 2) <= radius:
                    self.game_map.highdark[i, j] = True

        self.game_map.highdark &= self.game_map.explored
        self.game_map.highlight = self.game_map.highdark & self.game_map.visible

    def highlight_clear(self) -> None:
        self.game_map.highlight[:] = False
        self.game_map.highdark[:] = False

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
