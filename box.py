"""
box
===

Module defines the box sprite used in "The Button Game".
"""

import pygame

from typing import Any
from pygame import Color
from settings import BOX_FONTSIZE, MAXIMUM_LIFETIME_SECONDS


LOW_LIFETIME_COLOR = Color('red')
HEIGH_LIFETIME_COLOR = Color('green')
SECONDS_PR_MILLISECONDS = 0.001


class Box(pygame.sprite.Sprite):
    """Box used in "The Button Game"

    Properties:
    ----------
        - alive (bool) : True if the internal timer still has time left.
        - time_left_seconds (float) : Time left before the box despawns - Measured in seconds

    Public attributes:
    -----------------
        - lifetime (float) : Time that the box is alive - Measured in seconds. 
        - topleft (pygame.Vector2) : Coordiantes of the top left corner of the box. 


    Public methods:
    --------------
        - __init__(lifetime: float, topleft: pygame.Vector2) : Constructor of the class
        - update(*args: Any, **kwargs: Any) -> None : Update the graphics of the sprite.
        - is_hit_by_mouse() -> bool : Return true if the mouse hovers over the sprite.
    """
    lifetime: float
    topleft: pygame.Vector2

    created_at_timestamp_ms: float
    font: pygame.font.Font


    def __init__(self, lifetime_seconds: float, topleft: pygame.Vector2) -> None:
        """Constructor of the Box class.

        Initiallize the sprite super class, store the input arguments 
        as attributes and register the timestamp at which the instance
        was created. 

        Args:
            lifetime_seconds (float): How long the box is alive for measured in seconds.
            topleft (pygame.Vector2): Spawn position of the box - Measures the top corner of its rectangle.
        """
        super().__init__()
        self.topleft = topleft
        self.lifetime = lifetime_seconds
        self.created_at_timestamp_ms = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, BOX_FONTSIZE)


    @property
    def alive(self) -> bool:
        """True if and only if there is there is still time left on the instance."""
        return self.time_left_seconds > 0


    @property
    def time_left_seconds(self) -> float:
        """Measures the time left on the box, in seconds, using the pygame clock."""
        return self.lifetime - SECONDS_PR_MILLISECONDS * (pygame.time.get_ticks() - self.created_at_timestamp_ms)


    def update(self, *args: Any, **kwargs: Any) -> None:
        """Update the image and rectangle of the sprite."""
        self.image = generate_text(self.time_left_seconds, self.font)
        self.rect  = self.image.get_rect(topleft=self.topleft)


    def is_hit_by_mouse(self) -> bool:
        """Return true if the mouse collides with teh rectangle of this sprite."""
        return self.rect.collidepoint(pygame.mouse.get_pos())



def generate_text(time: float, font: pygame.font.Font) -> pygame.Surface:
    """Generate a text surface stating a given time.
    
    The image prints the text in black with a fontsize given 
    by the font. The background color is interpolated between 
    red and green with maximum lifetime being green and 
    zero seconds being red.

    Args:
        time (float): Number that is drawn on the surface.
        font (pygame.font.Font): Font that is used to render the text.

    Returns:
        pygame.Surface: Image stating the time.
    """
    text = f"{time:.2f}"
    normalized_time = pygame.math.clamp(time / MAXIMUM_LIFETIME_SECONDS, 0, 1)  # Clamped to avoid ValueErrors of lerp.
    background = LOW_LIFETIME_COLOR.lerp(HEIGH_LIFETIME_COLOR, normalized_time)

    return font.render(text, False, Color('black'), background)