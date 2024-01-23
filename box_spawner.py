"""
box_spawner
===========

Modules defined the box spawner factory 
which generates instances of Box at given time
intervals.

Used in "The Button Game"

"""
import pygame

from box import Box
from math import log
from random import random
from typing import Optional

from settings import SPAWN_WINDOW_SIZE_SECONDS


MILLISECONDS_PR_SECOND = 1000


class BoxSpawner:
    """Factory generating Box instances.

    Used in "The Button Game" to generate Box instances 
    with a given lifetime that depends on the player score. 
    Boxes are spawned with a frequency that increases with 
    the player score.

    Public attributes:
    -----------------
        - spawn_bounds (pygame.rect.Rect) : Rectangle describing the limits of where boxes can spawn.
        - timestamp_next_spawn (int) : Timestamp, measured in milliseconds, where next box spawn.

    Public methods:
    --------------
        - __init__(bounds: pygame.rect.Rect) : Constructor of the class.
        
        - spawn(player_score: int) -> Optional[Box] : Return a new Box instance if the current pygame 
        time stamp exceeds the next spawn time stamp.
       
        - spawn_now(player_score: int) -> Box : Return a new Box instance no matter what the 
        internal timer says. Timer is resert.
        
        - reset_spawn_timer(player_score: int) -> None : Generate a new spawn time by picking a random 
        cooldown time and and add it to the current pygame time.
    """
    timestamp_next_spawn: int
    spawn_bounds: pygame.rect.Rect


    def __init__(self, bounds: pygame.rect.Rect):
        """Constructor of the class.

        Get the time stamp where the next box spawns.

        Args:
            bounds (pygame.rect.Rect): Rectangle descring the area where boxes can spawn.
        """
        self.spawn_bounds = bounds
        self.reset_spawn_timer()


    def spawn(self, player_score: int) -> Optional[Box]:
        """Return a new Box instance if the current pygame time stamp exceeds the next spawn time stamp.

        The current pygame time stamp is checked and compared to the "timestamp_next_spawn" attribute. 
        If the current time exceeds this timestamp, a new Box instance is created and returned. The lifetime
        and frequency of box spawning depends on the player score.

        Args:
            player_score (int): Current score.

        Returns:
            Optional[Box]: Box instance if a new box is spawned - None if not.
        """
        if pygame.time.get_ticks() >= self.timestamp_next_spawn:
            return self.spawn_now(player_score)
    

    def spawn_now(self, player_score: int=0) -> Box:
        """Return a new Box instance no matter what the internal timer says. Timer is resert.

        Args:
            player_score (int, optional): Current score of the player. Defaults to 0.

        Returns:
            Box: Newly generated box instance. Position within the bounds rectangle.
        """
        lifetime = lifetime_from_score(player_score)
        topleft  = random_position_within_bounds(self.spawn_bounds)
        
        self.reset_spawn_timer(player_score)
        return Box(lifetime, topleft)


    def reset_spawn_timer(self, player_score: int=0) -> None:
        """Generate a new spawn time by picking a random cooldown time and and add it to the current pygame time.

        Args:
            player_score (int, optional): Current player score. Defaults to 0.
        """
        self.timestamp_next_spawn = pygame.time.get_ticks() + MILLISECONDS_PR_SECOND*random_cooldown_spawn_seconds(player_score)


def random_cooldown_spawn_seconds(player_score: int) -> float:
    """Pick a random time interval length.

    The cooldown time is picked uniformly from an interval [min, min + SPAWN_WINDOW_SIZE_SECONDS]
    where "min" is a value depending on the player score.

    Args:
        player_score (int): Current score of the player.

    Returns:
        float: Cooldown time, measured in seconds, before a new box can be spawned.
    """
    return SPAWN_WINDOW_SIZE_SECONDS*random() + minimum_spawn_time_seconds(player_score)


def minimum_spawn_time_seconds(player_score: int) -> float:
    """Minimum cooldown time as a function of player score. Descreases with player score."""
    if player_score <= 5:
        return 1.0
    if player_score >= 20:
        return 0.1

    return 1.2 - 0.06*player_score


def lifetime_from_score(player_score: int) -> float:
    """Lifetime of the box depending on the player score. Decreases with player score.""" 
    if player_score <= 5:
        return 7.0
    if player_score >= 20:
        return 1.0
    
    return 9.0 - 0.4*player_score


def random_position_within_bounds(bounds: pygame.rect.Rect) -> pygame.Vector2:
    """Return a random position inside the given bounds"""
    x = pygame.math.lerp(bounds.right, bounds.left, random())
    y = pygame.math.lerp(bounds.bottom, bounds.top, random())
    return pygame.Vector2(x, y)