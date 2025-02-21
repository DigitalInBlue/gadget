import logging
from GadgetComponent import GadgetComponent
from PIL import Image, ImageDraw
import hashlib

logger = logging.getLogger(__name__)

class Gadget_8948ee30(GadgetComponent):

    def run(self, input_data: str) -> Image.Image:
        if not isinstance(input_data, str):
            logger.error(f'Invalid input type: Expected str.')
            return None

        try:
            # Step 1: Hash the input data to produce a deterministic binary sequence
            hash_object = hashlib.sha256(input_data.encode())
            binary_sequence = bin(int(hash_object.hexdigest(), 16))[2:].zfill(256)

            # Step 2: Transform the binary sequence into image data
            size = 16  # Image size of 16x16 pixels
            image = Image.new('RGB', (size, size), 'white')
            draw = ImageDraw.Draw(image)

            # Step 3: Use the binary sequence to draw on the image
            for i in range(size):
                for j in range(size):
                    # Determine pixel color based on binary sequence
                    bit_index = i * size + j
                    if binary_sequence[bit_index] == '1':
                        draw.point((j, i), fill='black')

            logger.info(f"Generated image from input data '{input_data}'")
            return image

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None

    def get_name(self):
        return __file__ + ': ' + "Cryptographic Binary Image Synthesizer"