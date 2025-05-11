from GadgetComponent import GadgetComponent
import logging
from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


class Gadget_47650b60(GadgetComponent):

    def run(self, input_data: dict) -> Image.Image:
        if not isinstance(input_data, dict):
            logger.error(f"Invalid input type: Expected dict.")
            return None

        try:
            # Extract parameters from input_data
            width = input_data.get("width", 100)
            height = input_data.get("height", 100)
            color = input_data.get("color", "white")

            # Validate extracted parameters
            if not isinstance(width, int) or not isinstance(height, int):
                logger.error(f"Invalid dimensions: Expected integers.")
                return None
            if not isinstance(color, str):
                logger.error(f"Invalid color type: Expected string.")
                return None

            logger.info("Creating image with provided parameters.")

            # Create an image with specified width, height, and color
            image = Image.new("RGB", (width, height), color)
            draw = ImageDraw.Draw(image)

            # Draw some pseudo-random patterns
            for i in range(0, width, 10):
                for j in range(0, height, 10):
                    draw.ellipse(
                        (i, j, i + 10, j + 10), fill=(i % 256, j % 256, (i * j) % 256)
                    )

            logger.info("Finished creating the image.")
            return image

        except Exception as e:
            logger.warning(f"Caught exception during computation: {e}")
            return None

    def get_name(self):
        return __file__ + ": " + "Multidimensional Chromatic Generator"
