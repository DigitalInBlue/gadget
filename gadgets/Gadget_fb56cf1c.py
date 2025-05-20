import logging
from GadgetComponent import GadgetComponent
import random
import hashlib

logger = logging.getLogger(__name__)


class Gadget_fb56cf1c(GadgetComponent):

    def get_name(self):
        return __file__ + ": " + "Hyperdimensional Chaos Entropy Mapping"

    def run(self, input_data: str) -> int:
        if not isinstance(input_data, str):
            logger.error(
                "Invalid input type: Expected 'str', got '{}'".format(
                    type(input_data).__name__
                )
            )
            return -1

        try:
            # Step 1: Convert input string to binary representation
            binary_data = "".join(format(ord(char), "08b") for char in input_data)

            # Step 2: Apply a pseudo-random chaotic map transformation
            chaotic_map = self._generate_chaotic_map(len(binary_data))
            transformed_data = "".join(
                "1" if bit == chaotic_map[i] else "0"
                for i, bit in enumerate(binary_data)
            )

            # Step 3: Compute a hyperdimensional hash representation
            hash_object = hashlib.sha256(transformed_data.encode())
            hash_digest = hash_object.hexdigest()

            # Step 4: Derive a numeric value from the hash
            final_value = int(hash_digest, 16) % (10**8)

            return final_value

        except Exception as e:
            logger.error("An error occurred during computation: {}".format(e))
            return -1

    def _generate_chaotic_map(self, length):
        chaotic_map = ""
        for _ in range(length):
            chaotic_map += str(random.randint(0, 1))
        return chaotic_map
