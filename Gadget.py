# gadget.py
import os
import importlib
import inspect
import logging
import random
from PIL import Image
import json
from GadgetComponent import GadgetComponent
from io import BytesIO
from random import shuffle
import coloredlogs
import time

# Configure colored logging
coloredlogs.install()
logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Gadget:
    def __init__(self):
        """Initialize with no components; they will be loaded dynamically"""
        logger.info("Initializing Gadget")
        self.components = []
        self.steps = []
        self.incompatible_components = []

    def discover_components(self, directory="."):
        """Discover GadgetComponent classes in all Python files in the specified directory"""
        py_files = [f for f in os.listdir(directory) if f.endswith(".py") and f not in ["Gadget.py", "GadgetComponent.py"]]

        for py_file in py_files:
            module_name = py_file[:-3]  # Strip '.py' from the filename
            try:
                # Ensure the module is imported correctly
                module = importlib.import_module(module_name)
                logger.info(f"Loaded module: {module_name}")

                # Inspect the module for classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if the class is a subclass of GadgetComponent
                    if obj != GadgetComponent and issubclass(obj, GadgetComponent):
                        instance = obj()  # Create an instance of the class
                        self.components.append(instance)
                        logger.info(f"Discovered valid component: {instance.getName()} from {module_name}")
                    else:
                        logger.info(f"Skipped class: {name} from {module_name}")

            except Exception as e:
                logger.error(f"Error importing module {module_name}: {e}")

    def generate_random_input(self, input_type=None):
        """Generate a random input of a valid type (int, float, str, bool, Image.Image, dict)"""
        if input_type is None:
            input_type = random.choice([int, float, str, bool, Image.Image, dict])

        if input_type == int:
            return random.randint(1, 100)
        elif input_type == float:
            return random.uniform(1.0, 100.0)
        elif input_type == str:
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))  # Random 10-char string
        elif input_type == bool:
            return random.choice([True, False])
        elif input_type == Image.Image:
            return self.generate_random_image()
        elif input_type == dict:
            return self.generate_random_json()
        return None

    def generate_random_image(self):
        """Generate a random PNG image"""
        img = Image.new('RGB', (64, 64), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return img

    def generate_random_json(self):
        """Generate a random dictionary representing a JSON object"""
        return {
            "key": random.choice(['foo', 'bar', 'baz']),
            "value": random.randint(1, 100)
        }

    def assemble_machine(self):
        """Assemble the machine by chaining compatible components"""
        if not self.components:
            logger.error("No valid components found.")
            return None

        while len(self.steps) <= 1:
            remaining_components = self.components[:]
            shuffle(remaining_components)  # Randomize the order of components to create a different chain each time
           
            # Start with a random component
            self.steps.append(remaining_components.pop())

            # Report what component we are starting with
            logger.info(f"Starting with {self.steps[0].getName()}")

            # Get the output type of the first component
            run_signature = inspect.signature(self.steps[0].run)
            current_output_type = run_signature.return_annotation

            while remaining_components:
                compatible_component_found = False
                for component in remaining_components:
                    # Report what component we are checking
                    logger.debug(f"Checking compatibility of {component.getName()} with {current_output_type}")

                    # Instead of assuming the input/output types, inspect the run function's input and output types
                    run_signature = inspect.signature(component.run)
                    input_type = run_signature.parameters['input_data'].annotation
                    output_type = run_signature.return_annotation

                    logger.debug(f"Checking compatibility of {component.getName()} with {current_output_type}")
                    if current_output_type == input_type:
                        self.steps.append(component)
                        logger.info(f"Adding component {component.getName()} to the chain")
                        current_output_type = output_type
                        remaining_components.remove(component)
                        compatible_component_found = True
                        break

                if not compatible_component_found:
                    self.incompatible_components.extend(remaining_components)
                    logger.info(f"Done configuring the gadget with {len(self.steps)} gadgets.")
                    break

            if not self.steps:
                logger.warning("Could not assemble a machine. Trying again.")
                # Sleep for one second to avoid busy-waiting
                time.sleep(1)

        return self.steps


    def _is_compatible(self, component_a, component_b):
        # Inspect the run function signature of both components
        run_a_signature = inspect.signature(component_a.run)
        run_b_signature = inspect.signature(component_b.run)
        
        # Get the output type of component_a and the input type of component_b
        output_type = run_a_signature.return_annotation
        input_type = run_b_signature.parameters['input_data'].annotation

        # Check if the output of component_a can be the input of component_b
        return output_type == input_type


    def execute(self, initial_input):
        """Run the assembled steps"""
        output = initial_input
        for step in self.steps:
            output = step.execute(output)  # Use the execute method for validation
            if output is None:
                logger.error(f"Execution stopped at {step.getName()} due to invalid output.")
                return None
        return output

    def report_incompatibilities(self):
        """Report incompatible components and why they couldn't be used"""
        for component in self.incompatible_components:
            logger.info(f"Component {component.getName()} was incompatible.")


# Main execution
if __name__ == "__main__":
    # Create an instance of the Gadget
    gadget = Gadget()

    # Discover Gadget components in the current directory
    gadget.discover_components()

    # Assemble the machine starting from the random initial input
    assembled_steps = gadget.assemble_machine()

    # Get what the first component expects as input
    first_component_input_type = inspect.signature(assembled_steps[0].run).parameters['input_data'].annotation
    logger.info(f"First component input type: {first_component_input_type} for {assembled_steps[0].getName()}") 

    # Generate a random input of the expected type for the first component of type 'first_component_input_type'
    initial_input = gadget.generate_random_input(first_component_input_type)
    logger.info(f"Random initial input generated: {initial_input} (type: {type(initial_input).__name__})")

    # Execute the machine if possible
    if assembled_steps:
        final_output = gadget.execute(initial_input)
        logger.info(f"Final output: {final_output} (type: {type(final_output).__name__})")

    # Report incompatible components
    gadget.report_incompatibilities()
