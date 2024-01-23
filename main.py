"""
Main script of "The Button" game
================================

Running this script runs the main method
which initialiized pygame, creates a 
game instance and runs the game.

When game is closed, pygame is deinitiallized.
"""
import pygame

from box_spawner import BoxSpawner
from settings import FPS, UI_FONTSIZE, SCREEN_WIDTH, SCREEN_HEIGHT, UI_COLOR


def main() -> None:
    pygame.init()
    ButtonGame().run()
    pygame.quit()


class GameOver(Exception):
    """Exception used to signal that the game is over."""


class ButtonGame:
    """Game object of the Button game.
    
    Public attributes:
        player_score (int) : Current score of the player. Starts at 0.
        player_lives (int) : Positive integer couting the number of lives 
        the player have at a given time. Starts at 3.
        boxes (pygame.sprite.Group) : Sprite group containing boxes currently alive in the game.
        Constantly changes size.
    
    Public methods:
    ==============
        __init__     : Constructor of the game.
        run() -> int : Run the game. Returns the player score when game is closed.
    """
    player_score: int = 0
    player_lives: int = 3
    boxes: pygame.sprite.Group

    _ui_font = pygame.font.Font
    _box_spawner: BoxSpawner


    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        
        self._ui_font = pygame.font.Font(None, UI_FONTSIZE)
        self._box_spawner = BoxSpawner(pygame.rect.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200))

        self.boxes = pygame.sprite.Group()
        self.boxes.add(self._box_spawner.spawn_now())


    def run(self, deinitiallized_pygame_when_closed: bool=True) -> int:
        """Run the game loop. Print score to the standard output when finished.

        Args:
            deinitiallized_pygame_when_closed (bool, optional): Defaults to True.

        Returns:
            int: Player score
        """
        try:
            self.gameloop()
        except GameOver:
            print(f"Player score: {self.player_score}")
        finally:
            if deinitiallized_pygame_when_closed:
                pygame.quit()

        return self.player_score
        

    def gameloop(self) -> None:
        while True:
            if game_is_closed():
                return self.player_score

            self.display.fill('black')    

            self.spawn_new_box_if_possible()
            self.update_sprites()
            self.draw_game_objects()

            # Update window and tick to next frame. 
            pygame.display.update()
            self.clock.tick(FPS)


    def spawn_new_box_if_possible(self) -> None:
        """Spawn a box using the box spawner if possible.

        The box spawner has an internat clock that spawns boxes
        at random timestamps. If the pygame clock exceeds the
        spawn time, a new box is added to the boxes.
        """
        box = self._box_spawner.spawn(self.player_score)
        
        if box is not None:
            self.boxes.add(box)
        

    def update_sprites(self) -> None:
        """Update all the sprites in the game.

        The graphics of each box is updated using their "update" method.
        If the player pressses a box, the score increases and the box is killed.
        If the timer runs out on a box, it despawns and the player looses a life.

        Raises:
            GameOver: If player losses all their lives, the game is over
        """
        
        self.boxes.update()

        for box in self.boxes:
            if not box.alive: 
                self.player_lives -= 1
                box.kill()

            if box.is_hit_by_mouse():
                self.player_score += 1
                box.kill()

        if self.player_lives <= 0:
            raise GameOver


    def draw_game_objects(self) -> None:
        """Draw the boxes and player info to the screen."""
        self.boxes.draw(self.display)
        self.display.blit(self._ui_font.render(f"Player score: {self.player_score}", False, UI_COLOR), pygame.Vector2(0, 0))
        self.display.blit(self._ui_font.render(f"Lives: {self.player_lives}", False, UI_COLOR), pygame.Vector2(0, UI_FONTSIZE))


def game_is_closed() -> bool:
    """Check if the player closes the game by closing the window."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        
    return False


if __name__ == '__main__':
    main()
