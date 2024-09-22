import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_bc91e434(GadgetComponent):

    def get_name(self) -> str:
        return __file__ + ": " + "Quantum Dimensional Flux Capacitor"

    def run(self, input_data: str) -> int:
        if not isinstance(input_data, str):
            logger.error(f'Invalid input type: Expected str.')
            return None

        try:
            complex_value = 0
            length = len(input_data)
            logger.info(f'Processing input of length: {length}')

            # First nested loop for arbitrary calculations
            for i in range(length):
                temp_value = (ord(input_data[i]) * (i + 1)) % 255
                for j in range(temp_value):
                    if j % 2 == 0:
                        complex_value += (temp_value - j) ** 2
                    else:
                        complex_value -= (temp_value + j) ** 2

            logger.debug(f'Intermediate complex value after first loop: {complex_value}')

            # Second nested loop involving irrelevant data transformations
            for i in range(length):
                for j in range(i, length):
                    sub_value = (ord(input_data[j]) ** 3 + complex_value) % 97
                    for k in range(sub_value):
                        complex_value += (sub_value + k) // (i + 1)
                    logger.debug(f'Processing sub_value: {sub_value}, complex_value: {complex_value}')

            final_value = complex_value % 100000
            logger.info(f'Final computed value: {final_value}')

            return final_value

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None
