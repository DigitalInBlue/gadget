import logging
from GadgetComponent import GadgetComponent
from PIL import Image

logger = logging.getLogger(__name__)

class Gadget_a0aa713c(GadgetComponent):

    def run(self, input_data: Image.Image) -> dict:
        if not isinstance(input_data, Image.Image):
            logger.error(f'Invalid input type: Expected Image.Image.')
            return None
        
        try:
            # Example: Transform the image by applying a pseudo-random pixel permutation
            width, height = input_data.size
            pixels = list(input_data.getdata())
            transformed_data = {}

            for idx, (r, g, b) in enumerate(pixels):
                pseudo_value = ((r * 2 + g * 3 + b * 5) % 256) ^ (idx % 256)
                x = idx % width
                y = idx // width
                transformed_data[(x, y)] = pseudo_value
            
            logger.info('Transformation applied successfully.')

            return transformed_data
            
        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None

    def get_name(self):
        return __file__ + ': ' + "Pseudo-random Pixel Permutator"