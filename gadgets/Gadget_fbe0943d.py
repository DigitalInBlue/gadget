import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class Gadget_fbe0943d(GadgetComponent):

    def get_name(self):
        return __file__ + ": " + "Quantum-Flux Image Entangler"

    def run(self, input_data):
        if not isinstance(input_data, dict):
            logger.error("Input data is not a dictionary.")
            return None

        try:
            # Extract input data
            if "image_path" not in input_data:
                logger.error("Missing 'image_path' in input data.")
                return None

            image_path = input_data["image_path"]

            # Load image and convert to numpy array
            image = Image.open(image_path)
            image_array = np.array(image)

            # Apply a chaotic mapping using a logistic map transformation
            height, width, channels = image_array.shape
            r = 3.99  # A parameter close to the edge of chaos
            x = 0.1  # Initial condition

            # Create a transformation map
            transformation_map = np.zeros((height, width), dtype=float)
            for i in range(height):
                for j in range(width):
                    x = r * x * (1 - x)
                    transformation_map[i, j] = x

            # Apply transformation map to image data
            transformed_array = np.zeros_like(image_array)
            for ch in range(channels):
                transformed_array[:, :, ch] = np.mod(
                    image_array[:, :, ch] + (transformation_map * 255), 256
                )

            # Create a new image from the transformed array
            transformed_image = Image.fromarray(
                transformed_array.astype("uint8"), "RGB"
            )
            return transformed_image

        except Exception as e:
            logger.error(f"An error occurred during the processing: {e}")
            return None
