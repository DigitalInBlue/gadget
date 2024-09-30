# gadget.py
import os
import importlib
import importlib.util
import inspect
import logging
import random
from PIL import Image
from GadgetComponent import GadgetComponent
from random import shuffle
import coloredlogs
import time
import sys
import copy
import argparse

# Configure colored logging
coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Gadget:
    def __init__(self):
        """Initialize with no components; they will be loaded dynamically"""
        logger.info("Initializing Gadget")
        self.components = []
        self.steps = []
        self.unused_components = []
        self.incompatible_components = []

    def discover_components(self, directory="./gadgets"):
        """Discover GadgetComponent classes in all Python files in the specified directory"""
        # Make sure the directory exists
        if not os.path.exists(directory):
            logger.error(f"Directory not found: {directory}")
            return

        # Make sure there are Python files in the directory
        py_files = [f for f in os.listdir(directory) if f.endswith(".py") and f not in ["Gadget.py", "GadgetComponent.py"]]

        if not py_files:
            logger.error(f"No Python files found in directory: {directory}")
            return

        # Add the directory to sys.path temporarily to import modules from it
        sys.path.insert(0, directory)

        for py_file in py_files:
            logger.info(f"Loading module: {py_file}")
            module_name = py_file[:-3]  # Strip '.py' from the filename
            module_path = os.path.join(directory, py_file)  # Full path to the file

            try:
                # Load the module using importlib.util
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                logger.debug(f"Loaded module: {module_name}")

                # Inspect the module for classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if the class is a subclass of GadgetComponent
                    if obj != GadgetComponent and issubclass(obj, GadgetComponent):
                        instance = obj()  # Create an instance of the class
                        self.components.append(instance)
                        logger.info(f"Discovered valid component: \"{instance.get_name()}\" from {module_name}")
                    # else:
                    #     logger.info(f"Skipped class: {name} from {module_name}")

            except Exception as e:
                logger.error(f"Error importing module {module_name}: {e}")

    # Remove the directory from sys.path after importing
    sys.path.pop(0)

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

            # Seed the shuffle with the current date and time
            random.seed(time.time())

            # Randomize the order of components to create a different chain each time
            shuffle(remaining_components)

            # Start with a random component
            self.steps.append(remaining_components.pop())

            # Report what component we are starting with
            logger.info(f"Starting with \"{self.steps[0].get_name()}\"")

            # Get the output type of the first component
            run_signature = inspect.signature(self.steps[0].run)
            current_gadget_name = self.steps[0].get_name()
            current_output_type = run_signature.return_annotation

            while remaining_components:
                compatible_component_found = False
                for component in remaining_components:
                    # Report what component we are checking
                    # logger.debug(f"Checking compatibility of {component.get_name()} with {current_output_type}")

                    # Instead of assuming the input/output types, inspect the run function's input and output types
                    run_signature = inspect.signature(component.run)
                    input_type = run_signature.parameters['input_data'].annotation
                    output_type = run_signature.return_annotation

                    # logger.debug(f"Checking compatibility of {component.get_name()} with {current_output_type}")
                    if current_output_type == input_type:
                        self.steps.append(component)
                        logger.info(f"\"{current_gadget_name}\" --> \"{component.get_name()}\"")
                        current_output_type = output_type
                        current_gadget_name = component.get_name()
                        remaining_components.remove(component)
                        compatible_component_found = True
                        break

                if not compatible_component_found:
                    self.unused_components.extend(remaining_components)
                    logger.info(f"Done configuring the gadget with {len(self.steps)} gadgets.")
                    break

            if not self.steps:
                logger.warning("Could not assemble a machine. Trying again.")
                self.unused_components.clear()
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
        logger.info("Executing the gadget.")
        output = initial_input

        for step in self.steps:
            input = copy.copy(output)
            # logger.info(f"--> {step.get_name()}({input})")
            output = step.execute(input)  # Use the execute method for validation
            logger.info(f"--> \"{step.get_name()}({input})\" -> \"{output}\"")

            if output is None:
                logger.error(f"Execution stopped at \"{step.get_name()}\" due to invalid output.")
                return None
        return output

    def report_incompatibilities(self):
        """Report incompatible components and why they couldn't be used"""
        for component in self.unused_components:
            logger.info(f"Unused: \"{component.get_name()}\"")

    # Add this method to the Gadget class to print the blockchain
    def print_blockchain(self):
        """Print the blockchain of executed GadgetComponents based on self.steps"""
        if not self.steps:
            logger.info("No blockchain to display.")
            return

        logger.info("----- Blockchain -----")
        block_number = 1
        for component in self.steps:
            logger.info(f"Block {block_number}:")
            logger.info(f"  Component: {component.get_name()}")

            if hasattr(component, 'block_hash') and component.block_hash:
                logger.info(f"  Hash: {component.block_hash[:8]}")
            else:
                logger.info("  Hash: None")

            if hasattr(component, 'previous_hash') and component.previous_hash:
                logger.info(f"  Previous Hash: {component.previous_hash[:8] if component.previous_hash else 'None'}")
            else:
                logger.info("  Previous Hash: None")

            if hasattr(component, 'nonce') and component.nonce:
                logger.info(f"  Nonce: {component.nonce}")
            else:
                logger.info("  Nonce: None")

            if hasattr(component, 'run_time') and component.run_time:
                logger.info(f"  Run Time: {component.run_time:.4f} seconds")
            else:
                logger.info("  Run Time: None")

            if hasattr(component, 'mint_time') and component.mint_time:
                logger.info(f"  Mint Time: {component.mint_time:.4f} seconds")
            else:
                logger.info("  Mint Time: None")

            if hasattr(component, 'timestamp') and component.timestamp:
                logger.info(f"  Timestamp: {component.timestamp.strftime("%d%m%Y-%H:%M:%S.%f")[:-2]}")
            else:
                logger.info("  Timestamp: None")

            block_number += 1
        logger.info("----------------------")


def run_specific_gadget(gadget, class_name):
    """Run a specific gadget by class name."""
    for component in gadget.components:
        if component.__class__.__name__ == class_name:
            logger.info(f"Running specific gadget: {class_name}")
            first_component_input_type = inspect.signature(component.run).parameters['input_data'].annotation
            initial_input = gadget.generate_random_input(first_component_input_type)
            final_output = component.execute(initial_input)
            logger.info(f"Output from {class_name}: {final_output}")
            return
    logger.error(f"No gadget found with the class name: {class_name}")
    sys.exit(1)


# Main execution
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run a specific Gadget or a random one.")
    parser.add_argument('--debug', type=str, help='Optional Gadget class name to debug a specific gadget.')
    parser.add_argument('--debugLoop', type=str, help='Optional Gadget class name to debug a specific gadget in a loop until it crashes.')
    args = parser.parse_args()

    # Start timer
    start_time = time.time()

    # Create an instance of the Gadget
    gadget = Gadget()

    # Discover Gadget components in the current directory
    gadget.discover_components()

    if args.debug:
        run_specific_gadget(gadget, args.debug)
    elif args.debugLoop:
        while True:
            run_specific_gadget(gadget, args.debugLoop)
    else:
        try:
            # Assemble the machine starting from the random initial input
            assembled_steps = gadget.assemble_machine()

            # Make sure we have a gadget to run (that we have assembeled_steps)
            if not assembled_steps:
                logger.error("No gadget to run. Exiting.")
                sys.exit(1)  # Return exit code 1 to indicate no gadget found

            # Print out the complete gadget chain (assembled_steps) that we will execute.
            logger.info("Gadget chain to execute:")

            # Assemble a string that shows the gadget names along with their inputs and outputs. [input_type](gadget_name)[output_type] --> [input_type](gadget_name)[output_type]
            gadget_chain = ""
            for i, step in enumerate(assembled_steps):
                if i == 0:
                    gadget_chain += f"[{inspect.signature(step.run).parameters['input_data'].annotation.__name__}]({step.get_name()})[{inspect.signature(step.run).return_annotation.__name__}]"
                else:
                    gadget_chain += f" --> [{inspect.signature(step.run).parameters['input_data'].annotation.__name__}]({step.get_name()})[{inspect.signature(step.run).return_annotation.__name__}]"

                gadget_chain += "\n"

            logger.info("\n" + gadget_chain)

            # Get what the first component expects as input
            first_component_input_type = inspect.signature(assembled_steps[0].run).parameters['input_data'].annotation
            logger.info(f"First component input type: {first_component_input_type} for \"{assembled_steps[0].get_name()}\"")

            # Generate a random input of the expected type for the first component of type 'first_component_input_type'
            initial_input = gadget.generate_random_input(first_component_input_type)
            logger.info(f"Random initial input generated: {initial_input} (type: {type(initial_input).__name__})")

            # Execute the machine if possible
            if assembled_steps:
                final_output = gadget.execute(initial_input)
                logger.info(f"Final output: {final_output} (type: {type(final_output).__name__})")

            # Report incompatible components
            gadget.report_incompatibilities()

            # Print the blockchain
            gadget.print_blockchain()

            # End timer and calculate total run time
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f"Total execution time: {total_time:.2f} seconds")

            # If everything worked, return exit code 0
            sys.exit(0)

        except Exception as e:
            # Log the exception and return a non-zero exit code
            logger.error(f"An unexpected error occurred: {e}")
            sys.exit(2)  # Return exit code 2 for unexpected errors
