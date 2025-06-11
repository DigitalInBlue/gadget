import logging
from PIL import Image
import numpy as np
from GadgetComponent import GadgetComponent

# Set up logging
logger = logging.getLogger(__name__)


class Gadget_eaae0e26(GadgetComponent):

    def run(self, input_data: int) -> Image.Image:
        if not isinstance(input_data, int):
            logger.error(
                "Invalid input type: expected int, got %s", type(input_data).__name__
            )
            return None

        try:
            # Seed the random generator for reproducibility
            np.random.seed(input_data)

            # Generate a hyperdimensional chaotic state matrix
            state_matrix = np.random.rand(64, 64) * 255
            state_matrix = np.mod(np.floor(state_matrix), 256).astype("uint8")

            # Apply a self-referential chaotic map transformation
            for _ in range(input_data % 10 + 1):
                index = np.unravel_index(
                    np.argmax(state_matrix, axis=None), state_matrix.shape
                )
                value = state_matrix[index]
                state_matrix = np.roll(state_matrix, value, axis=0)
                state_matrix = np.roll(state_matrix, value, axis=1)
                state_matrix = np.abs(state_matrix - value)

            # Convert the state matrix to a greyscale image
            image = Image.fromarray(state_matrix, mode="L")

            return image

        except Exception as e:
            logger.exception("An error occurred during the transformation: %s", str(e))
            return None

    def get_name(self):
        return __file__ + ": " + "Hyperdimensional Chaotic Mapping"
