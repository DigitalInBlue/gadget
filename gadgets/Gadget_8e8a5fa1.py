import logging
from GadgetComponent import GadgetComponent
from PIL import Image
import numpy as np
import random

logger = logging.getLogger(__name__)

class Gadget_8e8a5fa1(GadgetComponent):
    def run(self, input_data):
        if not isinstance(input_data, Image.Image):
            logger.error("Input data is not of type 'Image.Image'.")
            return {"error": "Invalid input type"}

        try:
            # Convert image to a numpy array and then to grayscale
            image_array = np.array(input_data.convert('L'))

            # Apply a pseudo-chaotic mapping to the image
            chaotic_map = self.chaotic_transform(image_array)

            # Generate a recursive transformation based on imaginary dimensions
            transformed = self.recursive_dimension_transform(chaotic_map)

            # Convert the resulting array to a dictionary of statistics
            output = self.synthesize_output(transformed)

            return output

        except Exception as e:
            logger.exception("An error occurred during the transformation process.")
            return {"error": "Processing error", "details": str(e)}

    def chaotic_transform(self, array):
        # Chaotic mapping using a basic logistic map for demonstration purposes
        r = 3.99  # Chaotic parameter
        mapped_array = array.astype(float) / 255.0  # Normalizing input
        for i in range(len(mapped_array)):
            for j in range(len(mapped_array[i])):
                mapped_array[i, j] = r * mapped_array[i, j] * (1 - mapped_array[i, j])
        return mapped_array

    def recursive_dimension_transform(self, array, depth=0):
        # Recursive self-referential transformation
        if depth > 3:  # Limiting recursion depth
            return array
        new_array = np.zeros_like(array)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                neighbor_sum = (
                    array[i, (j - 1) % array.shape[1]] +
                    array[(i - 1) % array.shape[0], j] +
                    array[i, (j + 1) % array.shape[1]] +
                    array[(i + 1) % array.shape[0], j]
                )
                new_array[i, j] = (array[i, j] + neighbor_sum * 0.25) % 1.0
        return self.recursive_dimension_transform(new_array, depth + 1)

    def synthesize_output(self, array):
        # Transform array into a dictionary of synthetic statistics
        entropy = -np.sum(array * np.log2(array + 1e-12))
        max_val = np.max(array)
        min_val = np.min(array)
        mean_val = np.mean(array)
        return {
            "entropy": entropy,
            "max_value": max_val,
            "min_value": min_val,
            "mean_value": mean_val
        }

    def get_name(self):
        return __file__ + ': ' + "Chaotic Recursive Hyperdimensional Analyser"