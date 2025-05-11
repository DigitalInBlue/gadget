import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import numpy as np
import random

logger = logging.getLogger(__name__)


class Gadget_a9fd6b2a(GadgetComponent):
    def run(self, input_data: Image.Image) -> Image.Image:
        if not isinstance(input_data, Image.Image):
            logger.error("Invalid input type: Expected PIL.Image.Image")
            return input_data

        try:
            # Convert image to grayscale
            input_image = input_data.convert("L")
            image_array = np.array(input_image)

            # Apply chaotic random perturbations based on pixel values
            height, width = image_array.shape
            output_array = np.zeros((height, width), dtype=np.uint8)

            for y in range(height):
                for x in range(width):
                    chaos_factor = int(np.sin(image_array[y, x]) * 255)
                    random.seed(chaos_factor)  # Seed randomness for chaos
                    perturbation = random.randint(-20, 20)
                    output_value = image_array[y, x] + perturbation
                    # Ensure the value is within valid range
                    output_array[y, x] = max(0, min(255, output_value))

            output_image = Image.fromarray(output_array, "L")

        except Exception as e:
            logger.error(f"An error occurred during processing: {e}")
            return input_data

        return output_image

    def get_name(self):
        return __file__ + ": " + "Chaotic Perturbation Matrix"
