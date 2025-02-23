import logging
from GadgetComponent import GadgetComponent

logger = logging.getLogger(__name__)

class Gadget_ad65f4d5(GadgetComponent):

    def run(self, input_data: str) -> dict:
        if not isinstance(input_data, str):
            logger.error('Invalid input type: Expected str.')
            return None

        try:
            # Convert the input string to ASCII values
            ascii_values = [ord(char) for char in input_data]
            logger.debug(f'Converted input data to ASCII values: {ascii_values}')

            # Perform a pseudo-encryption algorithm: Reverse the ASCII list and apply a bitwise XOR with a constant
            key = 0x42  # Chosen arbitrarily for this example
            transformed = [(value ^ key) for value in reversed(ascii_values)]
            logger.debug(f'Transformed ASCII values with XOR and reverse: {transformed}')

            # Convert the transformed values back to characters
            transformed_chars = [chr(value) for value in transformed]
            logger.debug(f'Converted transformed values back to characters: {transformed_chars}')

            # Create a dictionary as output
            result = {
                'original': input_data,
                'transformed': ''.join(transformed_chars),
                'ascii_values': ascii_values,
                'transformed_ascii': transformed
            }
            logger.info(f'Computed transformation successfully: {result}')
            return result

        except Exception as e:
            logger.warning(f'Caught exception during computation: {e}')
            return None

    def get_name(self):
        return __file__ + ': ' + "Quantum ASCII Enigma"