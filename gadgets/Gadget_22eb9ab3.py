import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import numpy as np
import random

logger = logging.getLogger(__name__)


class Gadget_22eb9ab3(GadgetComponent):

    def get_name(self):
        return __file__ + ": " + "Hyperdimensional Chaotic Entropy Mapper"

    def run(self, input_data):
        if not isinstance(input_data, Image.Image):
            logger.error("Invalid input type: expected PIL.Image.Image")
            return float("nan")

        try:
            input_array = np.array(
                input_data.convert("L")
            )  # Convert image to grayscale
            height, width = input_array.shape

            # Step 1: Create a hyperdimensional space based on image dimensions
            hyper_dimensional_matrix = np.random.rand(
                height, width, random.randint(3, 7)
            )

            # Step 2: Populate hyperdimensional matrix with chaotic mappings
            for i in range(height):
                for j in range(width):
                    chaotic_value = np.sin(input_array[i, j] * np.pi / 256) * np.cos(
                        np.pi / (1 + height - i + width - j)
                    )
                    hyper_dimensional_matrix[i, j] *= chaotic_value

            # Step 3: Calculate entropy using hyperdimensional attributes
            entropy_sum = 0.0
            for k in range(hyper_dimensional_matrix.shape[2]):
                slice_entropy = np.sum(
                    np.abs(
                        np.diff(np.sort(hyper_dimensional_matrix[:, :, k].flatten()))
                    )
                )
                entropy_sum += slice_entropy

            # Normalize entropy to a float between 0 and 1
            normalized_entropy = entropy_sum / (
                height * width * (hyper_dimensional_matrix.shape[2] ** 2)
            )
            return float(normalized_entropy)

        except Exception as e:
            logger.error(f"Exception occurred during run: {e}")
            return float("nan")
