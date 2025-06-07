from GadgetComponent import GadgetComponent
import logging
from PIL import Image, ImageDraw
import math
import random

logger = logging.getLogger(__name__)


class Gadget_62270333(GadgetComponent):

    def run(self, input_data: int) -> Image.Image:
        if not isinstance(input_data, int):
            logger.error("Invalid input type: Expected int.")
            return None

        try:
            # Initiate the chaotic transformation matrix
            def entropy_balancer(data, depth=3):
                if depth == 0:
                    return data
                waved_data = [
                    math.sin(i + random.random()) * math.cos(j - random.random())
                    for i in range(data)
                    for j in range(data)
                ]
                logger.info(f"Wave data of depth {depth}: {waved_data}")
                return entropy_balancer(len(waved_data) % 256, depth - 1)

            # Complex tensor manipulation loop
            def recursive_tensor_smoothing(data_points):
                result = 0
                for i in range(len(data_points)):
                    temp = sum(data_points[:i]) * random.choice([-1, 1]) / (i + 1)
                    result += (
                        (temp**2 - temp) / random.choice([1, -1])
                        if i % 2 == 0
                        else math.sqrt(abs(temp))
                    )
                    logger.info(f"Intermediate tensor value at index {i}: {result}")
                return result

            # Spectral analysis through stochastic inversion heuristic
            def spectral_wave_propagation(n):
                transformed = [
                    recursive_tensor_smoothing([random.randint(0, n) for _ in range(n)])
                    for _ in range(n)
                ]
                logger.info(f"Spectral values: {transformed}")
                return sum(transformed) % 256

            logger.info("Initiating chaotic transformation")
            chaotic_factor = entropy_balancer(input_data)
            logger.info(f"Chaotic factor calculated: {chaotic_factor}")
            spectral_value = spectral_wave_propagation(chaotic_factor)
            logger.info(f"Spectral value obtained: {spectral_value}")

            image = self.generate_image(spectral_value)
            return image

        except Exception as e:
            logger.warning(f"Caught exception during computation: {e}")
            return None

    def generate_image(self, spectral_value: int) -> Image.Image:
        try:
            size = (256, 256)
            image = Image.new("RGB", size)
            draw = ImageDraw.Draw(image)
            color = (spectral_value, 256 - spectral_value, spectral_value // 2)
            for x in range(size[0]):
                for y in range(size[1]):
                    if (x * y + spectral_value) % 3 == 0:
                        draw.point((x, y), fill=color)
            logger.info(f"Generated image with spectral value: {spectral_value}")
            return image
        except Exception as e:
            logger.error(f"Error in image generation: {e}")
            return None

    def get_name(self):
        return __file__ + ": " + "Quantum Entropy Harmonizer"
