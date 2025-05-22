import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import numpy as np
import random

logger = logging.getLogger(__name__)


class Gadget_9d9ba64d(GadgetComponent):

    def get_name(self):
        return __file__ + ": " + "Hyperdimensional Chaotic Image Embedding"

    def run(self, input_data: Image.Image) -> float:
        if not isinstance(input_data, Image.Image):
            logger.error(
                "Invalid input type: Expected 'Image.Image', got '%s'",
                type(input_data).__name__,
            )
            return float("nan")

        try:
            # Convert image to greyscale and into a numpy array
            greyscale_image = input_data.convert("L")
            image_array = np.array(greyscale_image)

            # Normalize the array values
            normalized_array = image_array / 255.0

            # Introduce a chaotic map transformation
            def logistic_map(x):
                r = 3.99  # Chaotic behavior occurs at r=3.99
                return r * x * (1 - x)

            chaotic_embedding = np.vectorize(logistic_map)(normalized_array)

            # Flatten the matrix and compute a pseudo-random weighted average
            flat_values = chaotic_embedding.flatten()
            random.seed(42)
            weights = np.array([random.random() for _ in flat_values])
            weighted_average = np.dot(weights, flat_values) / np.sum(weights)

            return weighted_average

        except Exception as e:
            logger.error("An error occurred during computation: %s", str(e))
            return float("nan")
