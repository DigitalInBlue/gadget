import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)


class Gadget_86d1bb88(GadgetComponent):
    """
    Gadget_86d1bb88 is a class that simulates the Collatz Conjecture sequence for any given positive integer.
    The Collatz Conjecture is a mathematical problem that proposes that for any integer `n`, by following a simple
    set of rules, we will eventually reach the number 1.

    The rules are:
    - If `n` is even, divide it by 2: `n = n / 2`
    - If `n` is odd, multiply it by 3 and add 1: `n = 3 * n + 1`

    This process continues until `n` reaches 1. The class provides functionality to compute this sequence and log
    information such as the sequence itself and the total number of steps it took to reach 1.

    Attributes:
    ----------
    MAX_STEPS : int
        The maximum number of steps allowed for calculating the Collatz sequence to avoid long-running computations.
        If this limit is exceeded, the computation will terminate early.

    MAX_INPUT_SIZE : int
        The maximum allowed value for the input to prevent extremely large numbers, which could result in long computations.

    Methods:
    -------
    run(input_data: int) -> str:
        Computes the Collatz sequence for the given integer input. Logs the sequence and total steps. Implements
        constraints to limit the number of steps and the size of the input.

    get_name() -> str:
        Returns the name of the module or tool, which can be useful in identifying the functionality.
    """

    MAX_STEPS = 10000  # Limit the number of steps to avoid long-running cases
    MAX_INPUT_SIZE = 1_000_000  # Set a reasonable upper limit for input size

    def run(self, input_data: int) -> str:
        if not isinstance(input_data, int):
            logger.error(f"Invalid input type: Expected int.")
            return None

        if input_data > self.MAX_INPUT_SIZE:
            logger.error(
                f"Input too large: {input_data}. Must be <= {self.MAX_INPUT_SIZE}."
            )
            logger.warning(
                f"Setting input to maximum allowed value: {self.MAX_INPUT_SIZE}."
            )
            input_data = self.MAX_INPUT_SIZE

        try:
            sequence = []
            steps = 0

            while input_data != 1:
                sequence.append(input_data)

                if steps >= self.MAX_STEPS:
                    logger.warning(
                        f"Max steps exceeded: {self.MAX_STEPS}. Terminating early."
                    )
                    return f"Sequence incomplete, terminated early at step {steps}. Current sequence: {sequence}"

                if input_data % 2 == 0:
                    input_data //= 2
                else:
                    input_data = 3 * input_data + 1

                steps += 1

            sequence.append(1)
            logger.info(f"Collatz sequence: {sequence}")
            logger.info(f"Total steps: {steps}")
            return f"Sequence: {sequence}, Total steps: {steps}"

        except Exception as e:
            logger.warning(f"Caught exception during computation: {e}")
            return None

    def get_name(self):
        return __file__ + ": Collatz Conjecture Navigational Tool"
