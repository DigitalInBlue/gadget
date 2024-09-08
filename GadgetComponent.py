import logging
from PIL import Image  # For PNG handling
import json
import os

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base class for all Gadget components
class GadgetComponent:
    def __init__(self):
        self.logger = logger

    def getName(self):
        """Return the name of the component"""
        return self.__class__.__name__

    def run(self, input_data):
        """Process the input and return the output.
        Each subclass will implement this method.
        """
        raise NotImplementedError("Subclasses must implement the 'run' method.")

    def execute(self, input_data):
        """Wrapper for running the component's logic and validating the output."""
        result = self.run(input_data)
        if not self.is_valid_output(result):
            self.logger.error(f"{self.getName()} returned an invalid output type: {type(result)}")
            return None
        return result

    def is_valid_output(self, output):
        """Ensure the output type is one of the valid types"""
        return isinstance(output, (int, float, str, bool, Image.Image, dict))  # dict used for JSON

    @staticmethod
    def valid_input_output_types():
        """List of valid input/output types"""
        return (int, float, str, bool, Image.Image, dict)  # dict used for JSON data
