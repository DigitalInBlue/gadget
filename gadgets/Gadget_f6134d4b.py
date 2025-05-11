import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_f6134d4b(GadgetComponent):

    def run(self, input_data: bool) -> int:
        if not isinstance(input_data, bool):
            logger.error(f"Invalid input type: Expected bool.")
            return None

        try:
            # Algorithm: Binary Locus Modulation
            # Step 1: Convert boolean input to integer
            intermediate_value = int(input_data)

            # Step 2: Perform a series of bitwise operations
            output_value = ((intermediate_value << 2) | 0b01) ^ 0b11

            # Step 3: Apply a non-linear transformation
            output_value = (output_value * 5) % 7

            # Step 4: Ensure the result is always positive
            result = abs(output_value)

            logger.info("Binary Locus Modulation completed successfully.")
            return result

        except Exception as e:
            logger.warning(f"Caught exception during computation: {e}")
            return None

    def get_name(self):
        return __file__ + ": Binary Locus Modulator"
