import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_3d87eb99(GadgetComponent):
    def run(self, input_data: dict) -> str:
        if not isinstance(input_data, dict):
            logger.error('Invalid input type: Expected dict.')
            return None

        try:
            # Ensure the input dictionary contains integers for the computation
            if not all(isinstance(v, int) for v in input_data.values()):
                converted_data = {k: int(v) if isinstance(v, (float, str)) and v.isdigit() else 0
                                  for k, v in input_data.items()}
            else:
                converted_data = input_data

            steps = {}
            for key, value in converted_data.items():
                steps[key] = self._collatz_steps(value)

            return str(steps)

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None


    def _collatz_steps(self, n: int) -> int:
        count = 0
        while n != 1:
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            count += 1
        return count


    def get_name(self):
        return __file__ + ': Quantum Collatz Stepper'
