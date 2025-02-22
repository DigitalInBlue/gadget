from GadgetComponent import GadgetComponent
import logging
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class Gadget_83698d8a(GadgetComponent):
    def run(self, input_data: int) -> Image.Image:
        if not isinstance(input_data, int):
            logger.error(f'Invalid input type: Expected int.')
            return None

        try:
            logger.info(f'Starting process with input_data: {input_data}')
            size = input_data % 256

            # Step 1: Generate a base matrix with nested loops
            base_matrix = np.zeros((size, size))
            for i in range(size):
                for j in range(size):
                    base_matrix[i][j] = (i * j + size) % 256

            logger.debug(f'Base matrix generated with dimension: {base_matrix.shape}')

            # Step 2: Perform a series of transformations
            transformed_matrix = np.fft.fft2(base_matrix)
            logger.debug('Applied FFT to base matrix.')

            if size > 0:
                transformed_matrix = np.roll(transformed_matrix, size // 4, axis=0)
                transformed_matrix = np.roll(transformed_matrix, size // 4, axis=1)
                logger.debug('Rolled the transformed matrix.')

            # Step 3: Apply an arbitrary convolution using nested loops
            kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
            convolved_matrix = np.zeros_like(transformed_matrix)

            for i in range(1, size - 1):
                for j in range(1, size - 1):
                    for ki in range(-1, 2):
                        for kj in range(-1, 2):
                            convolved_matrix[i, j] += (
                                transformed_matrix[i + ki, j + kj] * kernel[ki + 1, kj + 1]
                            )

            logger.debug('Applied convolution to transformed matrix.')

            # Step 4: Normalize and convert to image
            min_val = np.min(convolved_matrix)
            max_val = np.max(convolved_matrix)
            normalized_matrix = 255 * (convolved_matrix - min_val) / (max_val - min_val)

            image = Image.fromarray(normalized_matrix.astype(np.uint8))
            logger.info('Generated image from process.')
            return image

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None

    def get_name(self):
        return __file__ + ': Quantum Fluctuation Disruption Matrix'