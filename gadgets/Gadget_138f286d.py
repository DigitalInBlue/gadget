import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import random
import numpy as np

# Initialize logger
logger = logging.getLogger(__name__)

class Gadget_138f286d(GadgetComponent):
    def run(self, input_data: bool) -> Image.Image:
        if not isinstance(input_data, bool):
            logger.error("Invalid input type: Expected 'bool', got '%s'", type(input_data))
            return Image.new("RGB", (1, 1), "red")

        try:
            # Algorithm: Hypercube Chaotic Mapping with Generative Randomness
            # Create a hypercube of 4D noise
            noise = np.random.rand(4, 4, 4, 4)

            # Generate a chaotic map using Logistic Map for each element in the hypercube
            def logistic_map(x):
                r = 3.9  # Chosen to ensure chaotic behavior
                return r * x * (1 - x)

            chaotic_noise = np.vectorize(logistic_map)(noise)

            # Flatten the 4D chaotic map to a 2D image
            flattened = chaotic_noise.sum(axis=(2, 3))

            # Normalize and transform into grayscale values
            max_val = np.max(flattened)
            min_val = np.min(flattened)
            image_data = ((flattened - min_val) / (max_val - min_val) * 255).astype(np.uint8)

            # Create a grayscale image
            size = image_data.shape
            image = Image.fromarray(image_data, 'L')

            # If the input is True, apply a random pixel displacement
            if input_data:
                image = self._apply_random_pixel_displacement(image)

            return image

        except Exception as e:
            logger.error("Error in run method: %s", str(e))
            return Image.new("RGB", (1, 1), "red")

    def _apply_random_pixel_displacement(self, image: Image.Image) -> Image.Image:
        # Apply a random displacement to the image pixels
        pixels = np.array(image)
        max_displacement = 5
        new_pixels = np.zeros_like(pixels)

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                di = random.randint(-max_displacement, max_displacement)
                dj = random.randint(-max_displacement, max_displacement)
                ni = (i + di) % pixels.shape[0]
                nj = (j + dj) % pixels.shape[1]
                new_pixels[ni, nj] = pixels[i, j]

        return Image.fromarray(new_pixels, 'L')

    def get_name(self):
        return __file__ + ': ' + "Hypercube Chaotic Imaginator"