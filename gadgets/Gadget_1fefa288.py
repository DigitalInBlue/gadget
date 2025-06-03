import logging
from GadgetComponent import GadgetComponent
from random import randint, seed

logger = logging.getLogger(__name__)


class Gadget_1fefa288(GadgetComponent):
    def get_name(self):
        return __file__ + ": " + "Fractal Noise Dimensional Entangler"

    def run(self, input_data: dict) -> bool:
        if not isinstance(input_data, dict):
            logger.error(
                "Input data must be of type dict, received: %s", type(input_data)
            )
            return False

        try:
            seed_value = input_data.get("seed", 42)
            if not isinstance(seed_value, int):
                raise ValueError("Seed value must be an integer.")

            seed(seed_value)
            noise_map = self._generate_fractal_noise(input_data)
            transformed_output = self._transform_noise_to_boolean(noise_map)
            return transformed_output

        except Exception as e:
            logger.exception("Exception occurred during run: %s", e)
            return False

    def _generate_fractal_noise(self, input_data: dict) -> list:
        size = input_data.get("size", 10)
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Size must be a positive integer.")

        noise_map = [[randint(0, 255) for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                perturbation = randint(-5, 5)
                noise_map[i][j] = (noise_map[i][j] + perturbation) % 256

        return noise_map

    def _transform_noise_to_boolean(self, noise_map: list) -> bool:
        flat_values = [item for sublist in noise_map for item in sublist]
        noise_sum = sum(flat_values)
        threshold = sum(range(len(flat_values))) // 2

        logger.debug("Noise sum: %d, Threshold: %d", noise_sum, threshold)
        return noise_sum > threshold
