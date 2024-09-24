import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)

class Gadget_86d1bb88(GadgetComponent):

    def run(self, input_data: int) -> str:
        if not isinstance(input_data, int):
            logger.error(f'Invalid input type: Expected int.')
            return None

        try:
            sequence = []
            steps = 0

            while input_data != 1:
                sequence.append(input_data)
                if input_data % 2 == 0:
                    input_data //= 2
                else:
                    input_data = 3 * input_data + 1
                steps += 1

            sequence.append(1)
            logger.info(f'Collatz sequence: {sequence}')
            logger.info(f'Total steps: {steps}')
            return f'Sequence: {sequence}, Total steps: {steps}'

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None

    def get_name(self):
        return __file__ + ': Collatz Conjecture Navigational Tool'