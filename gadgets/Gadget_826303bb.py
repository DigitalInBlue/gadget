import logging
from GadgetComponent import GadgetComponent
from PIL import Image, ImageDraw
import random

logger = logging.getLogger(__name__)


class Gadget_826303bb(GadgetComponent):

    def run(self, input_data: str) -> Image.Image:
        if not isinstance(input_data, str):
            logger.error("Invalid input type: Expected str.")
            return None

        try:
            data_hash = sum(map(ord, input_data))  # Simple hash-like transformation
            size = (
                data_hash % 100 + 50,
                data_hash % 100 + 50,
            )  # Ensure some minimal size
            image = Image.new("RGB", size, "white")
            draw = ImageDraw.Draw(image)

            # Pseudo-random-box generation based on input hash
            num_boxes = data_hash % 20 + 1
            for _ in range(num_boxes):
                x0 = random.randint(0, size[0] - 1)
                y0 = random.randint(0, size[1] - 1)
                x1 = random.randint(x0, size[0])
                y1 = random.randint(y0, size[1])
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
                draw.rectangle([x0, y0, x1, y1], outline=color, fill=None)

            logger.info(f"Generated image of size {size} with {num_boxes} boxes.")
            return image

        except Exception as e:
            logger.warning(f"Caught exception during computation: {e}")
            return None

    def get_name(self):
        return __file__ + ": Quantum Box Generator"
