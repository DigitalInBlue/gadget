import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_a4fd184f(GadgetComponent):

    def run(self, input_data: dict) -> bool:
        if not isinstance(input_data, dict):
            logger.error('Invalid input type: Expected dict.')
            return False

        try:
            # Simulating Langton's Ant
            n = input_data.get('steps', 10000)
            if not isinstance(n, int):
                logger.error('Invalid type for steps: Expected int.')
                n = 10000

            # Setting up the grid and ant's initial position and direction
            grid = {}
            x, y = 0, 0
            direction = 0  # 0: up, 1: right, 2: down, 3: left

            for _ in range(n):
                pos = (x, y)
                if pos not in grid:
                    grid[pos] = False  # False: white, True: black

                if grid[pos] is False:
                    direction = (direction + 1) % 4  # Turn right
                    grid[pos] = True
                else:
                    direction = (direction - 1) % 4  # Turn left
                    grid[pos] = False

                # Move forward in the current direction
                if direction == 0:
                    y += 1
                elif direction == 1:
                    x += 1
                elif direction == 2:
                    y -= 1
                else:
                    x -= 1

            logger.info(f'Langton\'s Ant simulation completed for {n} steps.')
            return True

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return False


    def get_name(self):
        return __file__ + ': ' + "Langton's Ant Simulator"
