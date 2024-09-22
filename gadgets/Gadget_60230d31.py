import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_60230d31(GadgetComponent):

    def run(self, input_data: str) -> bool:
        if not isinstance(input_data, str):
            logger.error(f'Invalid input type: Expected str.')
            return False

        try:
            # Simulating Langton's Ant algorithm

            def langtons_ant(sequence: str) -> str:
                ant_pos = [0, 0]
                direction = 0  # 0: right, 1: down, 2: left, 3: up
                black_cells = set()

                for move in sequence:
                    pos_tuple = tuple(ant_pos)

                    if pos_tuple in black_cells:
                        direction = (direction + 1) % 4  # Turn right
                        black_cells.remove(pos_tuple)
                    else:
                        direction = (direction - 1) % 4  # Turn left
                        black_cells.add(pos_tuple)

                    if direction == 0:
                        ant_pos[0] += 1
                    elif direction == 1:
                        ant_pos[1] += 1
                    elif direction == 2:
                        ant_pos[0] -= 1
                    elif direction == 3:
                        ant_pos[1] -= 1

                return ''.join(['1' if tuple(ant_pos) in black_cells else '0' for _ in range(10)])

            transformed_input = ''.join([c for c in input_data if c in '01']) or '0'
            result = langtons_ant(transformed_input)

            return result.count('1') > result.count('0')

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return False

    def get_name(self):
        return __file__ + ': ' + "Langton's Ant Pattern Evaluator"
