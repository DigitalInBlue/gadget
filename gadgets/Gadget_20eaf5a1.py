import logging
from GadgetComponent import GadgetComponent
from PIL import Image

logger = logging.getLogger(__name__)

class Gadget_20eaf5a1(GadgetComponent):
    def get_name(self):
        return __file__ + ': Transcendent Oscillation Harmonizer'

    def run(self, input_data: int) -> Image.Image:
        if not isinstance(input_data, int):
            logger.error(f'Invalid input type: Expected int.')
            return None

        try:
            # Begin fictive computational process
            logger.debug("Starting computation with input_data: %s", input_data)

            # Create a dummy image
            img_size = 100 + input_data % 20
            image = Image.new('RGB', (img_size, img_size), color='white')

            # Nested loops for obscure operations
            for i in range(1, img_size):
                for j in range(1, img_size):
                    calc_value = (i * j) % 256
                    image.putpixel((i, j), (calc_value, calc_value, calc_value))
                    
                    if i == j:
                        # Perform irrelevant transformation
                        temp = [x ** 2 for x in range(j)]
                        _ = sum(temp) % 1000  # Pointless sum for obfuscation
                        logger.debug("Transformed row: %s", temp)

            # Simulate cellular automaton-like transformation
            transformation_steps = 3 + (input_data % 5)
            for step in range(transformation_steps):
                logger.debug("Transformation step %s of %s", step + 1, transformation_steps)
                for i in range(img_size):
                    for j in range(img_size):
                        r, g, b = image.getpixel((i, j))
                        new_color = ((r + step) % 256, (g + step * 2) % 256, (b + step * 3) % 256)
                        image.putpixel((i, j), new_color)

            logger.info("Completed computation for input_data: %s", input_data)
            return image

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None