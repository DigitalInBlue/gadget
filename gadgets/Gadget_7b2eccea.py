import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class Gadget_7b2eccea(GadgetComponent):
    def get_name(self):
        return __file__ + ': ' + "Quantum-Entropic Image Synthesizer"

    def run(self, input_data: str) -> Image.Image:
        if not isinstance(input_data, str):
            logger.error(f"Invalid input type: {type(input_data)}. Expected a string.")
            return Image.new('RGB', (1, 1), (255, 0, 0))

        try:
            # Transform input string into a unique numeric signature
            signature = self._compute_signature(input_data)

            # Generate a pseudo-random image based on signature
            image = self._generate_image(signature)

            return image

        except Exception as e:
            logger.exception("An error occurred while processing the input data.")
            return Image.new('RGB', (1, 1), (255, 0, 0))

    def _compute_signature(self, input_data: str) -> int:
        # Compute a hash of the input string and use it to create a unique numeric signature
        hash_value = abs(hash(input_data))
        signature = (hash_value % 256, (hash_value >> 8) % 256, (hash_value >> 16) % 256)
        return signature

    def _generate_image(self, signature: tuple) -> Image.Image:
        width, height = 256, 256
        image_data = np.zeros((height, width, 3), dtype=np.uint8)

        # Use a chaotic map to fill the image data based on the signature
        x, y, z = 0.1, 0.1, 0.1
        a, b, c = signature
        for i in range(height):
            for j in range(width):
                x = np.sin(a * y) - np.cos(b * z)
                y = np.sin(b * z) - np.cos(c * x)
                z = np.sin(c * x) - np.cos(a * y)
                image_data[i, j] = ((x * 255) % 256, (y * 255) % 256, (z * 255) % 256)

        image = Image.fromarray(image_data, 'RGB')
        return image