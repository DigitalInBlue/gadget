import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_da8738ce(GadgetComponent):
    def run(self, input_data: bool) -> int:
        if not isinstance(input_data, bool):
            logger.error("Invalid input type: Expected bool.")
            return None

        try:
            # The intriguing 'Binary Entropy Transformer'
            # Convert the boolean input into an integer (0 or 1)
            binary_value = int(input_data)

            # An obscure transformation: Calculate the "entropy" of the single bit
            # Using a pseudo-entropy formula: -p*log2(p) - (1-p)*log2(1-p)
            # where p is the probability of the bit being 1
            p = binary_value
            if p == 0 or p == 1:
                entropy = 0  # Edge cases where the "probability" is complete certainty
            else:
                # Normally this would be undefined for a single bit, but we embrace creativity!
                from math import log2

                entropy = -p * log2(p) - (1 - p) * log2(1 - p)

            # Convert entropy back to an integer by scaling (for the sake of returning an int)
            transformed_output = int(entropy * 1000)

            logger.info(
                f"Input {input_data} transformed to output {transformed_output}."
            )
            return transformed_output
        except Exception as e:
            logger.warning(f"Caught exception during computation: {e}")
            return None

    def get_name(self):
        return __file__ + ": " + "Binary Entropy Transformer"
