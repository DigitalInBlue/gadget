import logging
import random
import math
from GadgetComponent import GadgetComponent

# Setup the logger
logger = logging.getLogger(__name__)


class Gadget_14a9409f(GadgetComponent):
    def get_name(self):
        return __file__ + ": " + "Hyperdimensional Chaos Mapper"

    def run(self, input_data: int) -> bool:
        try:
            # Validate input
            if not isinstance(input_data, int):
                logger.error(
                    "Invalid input type: Expected int, got %s",
                    type(input_data).__name__,
                )
                return False

            # Transform input into a hyperdimensional representation
            hyper_dimensional_matrix = self._generate_hyperdimensional_representation(
                input_data
            )

            # Check for chaotic behavior in the transformed state
            is_chaotic = self._check_chaotic_behavior(hyper_dimensional_matrix)

            return is_chaotic

        except Exception as e:
            logger.exception("An error occurred during computation: %s", e)
            return False

    def _generate_hyperdimensional_representation(self, value: int):
        # Generate a pseudo-random matrix as a hyperdimensional embedding
        random.seed(value)
        matrix_size = 10  # Dimension size for simplicity
        matrix = [
            [random.randint(-10, 10) for _ in range(matrix_size)]
            for _ in range(matrix_size)
        ]
        logger.debug("Generated hyperdimensional matrix: %s", matrix)
        return matrix

    def _check_chaotic_behavior(self, matrix):
        # Calculate the "chaotic index" based on matrix entropy and randomness
        flat_matrix = sum(matrix, [])  # Flatten the matrix
        matrix_entropy = -sum(
            p * math.log2(p)
            for p in self._probability_distribution(flat_matrix)
            if p > 0
        )
        logger.debug("Calculated entropy of the matrix: %f", matrix_entropy)

        # Define a threshold for chaos based on entropy
        chaos_threshold = 3.5  # Chosen arbitrarily for demonstration
        is_chaotic = matrix_entropy > chaos_threshold
        logger.info("Matrix is %s chaotic", "highly" if is_chaotic else "not")
        return is_chaotic

    def _probability_distribution(self, data):
        # Create a normalized probability distribution from the data
        total_count = len(data)
        frequencies = {value: data.count(value) / total_count for value in set(data)}
        logger.debug("Probability distribution: %s", frequencies)
        return frequencies.values()
