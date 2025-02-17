import openai
import os
import random
from GadgetComponent import GadgetComponent
import logging
import subprocess
import coloredlogs
import sys
import importlib
import inspect

# Configure colored logging
coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Valid input/output types for components
VALID_TYPES = ["int", "float", "str", "bool", "Image.Image", "dict"]


# Helper function to convert the type to a string (e.g., <class 'bool'> becomes 'bool')
def type_to_str(t):
    """Convert a type object to a string matching VALID_TYPES format."""
    str_name = t.__name__ if hasattr(t, '__name__') else str(t)

    if str_name == "Image":
        str_name = "Image.Image"

    return str_name


# Read the API key from an external file
def read_api_key(filename="openai_api_key.txt"):
    with open(filename, 'r') as file:
        return file.read().strip()


# Initialize the OpenAI API
openai.api_key = read_api_key()


# Function to generate a random 8-digit hexadecimal number for the class name
def generate_hex_class_name():
    return f"Gadget_{random.randint(0x10000000, 0xFFFFFFFF):08x}"


# Function to randomly select valid input and output types
def random_valid_type():
    return random.choice(VALID_TYPES)


# Function to scan existing components and collect input/output types
def scan_existing_components(directory="./gadgets"):
    """Scan all existing components and count input/output types."""
    input_type_count = {valid_type: 0 for valid_type in VALID_TYPES}
    output_type_count = {valid_type: 0 for valid_type in VALID_TYPES}

    if not os.path.exists(directory):
        logger.error(f"Directory not found: {directory}")
        return input_type_count, output_type_count

    py_files = [f for f in os.listdir(directory) if f.endswith(".py") and f not in ["Gadget.py", "GadgetComponent.py"]]

    if not py_files:
        logger.error(f"No Python files found in directory: {directory}")
        return input_type_count, output_type_count

    # Add the directory to sys.path temporarily to import modules from it
    sys.path.insert(0, directory)

    for py_file in py_files:
        # logger.debug(f"Scanning file: {py_file}")

        module_name = py_file[:-3]  # Strip '.py' from the filename
        module_path = os.path.join(directory, py_file)

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # logger.debug(f"Imported module: {module_name}")

            # Inspect the module for GadgetComponent classes
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj != GadgetComponent and issubclass(obj, GadgetComponent):
                    run_signature = inspect.signature(obj.run)
                    input_type = run_signature.parameters['input_data'].annotation
                    output_type = run_signature.return_annotation

                    input_type = type_to_str(input_type)
                    output_type = type_to_str(output_type)

                    # logger.debug(f"Class: {name}, Input type: {input_type}, Output type: {output_type}")

                    if input_type in VALID_TYPES:
                        input_type_count[input_type] += 1
                    if output_type in VALID_TYPES:
                        output_type_count[output_type] += 1

        except Exception as e:
            logger.error(f"Error importing module {module_name}: {e}")

    sys.path.pop(0)  # Remove the directory from sys.path
    return input_type_count, output_type_count


# Function to check if there is a significant imbalance between inputs and outputs
def find_type_imbalance(input_count, output_count, threshold=0.2):
    """Check for statistical imbalance between input and output counts."""
    imbalance = {}

    logger.info("Checking for input/output type imbalance...")

    for valid_type in VALID_TYPES:
        input_ratio = input_count[valid_type] / (sum(input_count.values()) or 1)
        output_ratio = output_count[valid_type] / (sum(output_count.values()) or 1)

        # Report what type of imbalance is detected
        logger.info(f"Type: {valid_type}, Input ratio: {input_ratio:.2f}, Output ratio: {output_ratio:.2f} - Balance: {abs(input_ratio - output_ratio):.2f}")

        # If the input-output difference is above the threshold, there's an imbalance
        if abs(input_ratio - output_ratio) > threshold:
            imbalance[valid_type] = "input" if input_ratio < output_ratio else "output"

    return imbalance


def get_input_and_output_types(imbalance=None):
    if imbalance:
        logger.info(f"Detected imbalance in: {imbalance}")
        # Prioritize generating components that correct the imbalance
        if "input" in imbalance.values():
            output_type = random.choice([t for t, v in imbalance.items() if v == "input"])
            input_type = random_valid_type()
        elif "output" in imbalance.values():
            input_type = random.choice([t for t, v in imbalance.items() if v == "output"])
            output_type = random_valid_type()
    else:
        logger.info("No significant imbalance detected.")
        # Randomly select input/output types if no significant imbalance
        input_type = random_valid_type()
        output_type = random_valid_type()

    return input_type, output_type


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_useless_component(class_name, input_type, output_type):
    logger.info(f"Generating a new Gadget component that takes input of type '{input_type}' and returns output of type '{output_type}'.")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content":
                f"Generate a Python class derived from 'GadgetComponent' with the class name '{class_name}'. "
                f"The class should import GadgetComponent as: `from GadgetComponent import GadgetComponent.` "
                f"The class should have a 'run' function that accepts input of type '{input_type}' and returns output of type '{output_type}'. "
                f"The 'run' function should include useless work such as nested loops, pointless calculations, and irrelevant data transformations, and should use the logger to show work done. "
                f"The 'run' function should take a single input parameter called 'input_data' with type annotation, for example: `def run(self, input_data: int) -> str`"
                f"The 'run' function should validate its input type, for example: `def run(self, input_data: int) -> str: if not isinstance(input_data, int): self.logger.error(f'Invalid input type: Expected int.') return None`"
                f"The 'run' function can perform more than one task, such as computing a cellular automata, an obscure algorithm, or complex transformations. Be highly creative."
                f"Neither the 'run' function nor the description should overtly state that it is useless work.  What it does should be obscure, but not nonsense or fantasy."
                f"Be highly creative in implementing the fictional '{class_name}' class. "
                f"Don't use words such as 'useless', 'pointless', 'nonsense', or 'fantasy'. The component should seem valid and useful, but ultimately meaningless. "
                f"Ensure that the logger is imported and instantiated globally using 'import logging' and 'logger = logging.getLogger(__name__)'. "
                f"The 'get_name' function should return a file name-prefixed pseudo-scientific or science-fiction name with multiple words separated by spaces. For example: \"def get_name(self):\n    return __file__ + ': ' + \"Interdimentional Floating-point Synthesizer\""
                f"Return only the python code for the class.  Do not include any other text or information. Do not wrap the code in '```python' or similar. "
                f"Follow PEP-8 guidelines for code style and formatting. "
                f"Wrap the internal code in a try-except block to catch and log any exceptions. For example:\n"
                f"```python\n"
                f"    def run(self, input_data: float) -> float:\n"
                f"        if not isinstance(input_data, float):\n"
                f"            logger.error(f'Invalid input type: Expected float.')\n"
                f"            return None\n"
                f"\n"
                f"        try:\n"
                f"            # Do pseud-complex work\n"
                f"        except Exception as e:\n"
                "            logger.warning(f'Caught exception during computation: {e}')\n"
                f"```\n"
            }
        ],
        temperature=0.8
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_useleful_component(class_name, input_type, output_type):
    input_type = random_valid_type()
    output_type = random_valid_type()

    logger.info(f"Generating a new Gadget component that takes input of type '{input_type}' and returns output of type '{output_type}'.")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content":
                f"Generate a Python class derived from 'GadgetComponent' with the class name '{class_name}'. "
                f"The class should import GadgetComponent as: `from GadgetComponent import GadgetComponent.` "
                f"The class should have a 'run' function that accepts input of type '{input_type}' and returns output of type '{output_type}'. "
                f"The 'run' function should be an implementation of an interesting computing algorithm, computing technique, transformation, applied information theory, or applied cryptographyetc. class."
                f"The 'run' function should use the logger to show work done. "
                f"The 'run' function should take a single input parameter called 'input_data' with type annotation, for example: `def run(self, input_data: int) -> str`"
                f"The 'run' function should validate its input type, for example: `def run(self, input_data: int) -> str: if not isinstance(input_data, int): self.logger.error(f'Invalid input type: Expected int.') return None`"
                f"The 'run' function should not implement any of the following algorithms (they have already been implemented):"
                f"\t- 'Computing the Collatz Conjecture Steps'"
                f"\t- 'Simulating Langton's Ant'"
                f"\t- 'Applying the Fast Fourier Transform'"
                f"\t- 'Implementing a Cellular Automata'"
                f"\t- 'Computing Minimal Godel Numbers'"
                f"What the 'run' function does should be obscure, but nonsense or fantasy."
                f"The class should be a valid implementation of the algorithm, technique, or transformation it claims to be. "
                f"Be highly creative in implementing the class. "
                f"If the input does not make sense for the given algorithm, perform some translation to it to get it into an appropriate type. "
                f"If the output does not make sense for the given algorithm, perform some translation to it to get it into an appropriate type. "
                f"Ensure that the logger is imported and instantiated globally using 'import logging' and 'logger = logging.getLogger(__name__)'. "
                f"The 'get_name' function should return a pseudo-scientific or science-fiction name with multiple words separated by spaces. For example: \"def get_name(self):\n    return __file__ + ': ' + \"Floating-point Synthesizer\""
                f"Return only the python code for the class.  Do not include any other text or information. Do not wrap the code in '```python' or similar. "
                f"Follow PEP-8 guidelines for code style and formatting. "
                f"Wrap the internal code in a try-except block to catch and log any exceptions. For example:\n"
                f"```\n"
                f"    def run(self, input_data: float) -> float:\n"
                f"        if not isinstance(input_data, float):\n"
                f"            logger.error(f'Invalid input type: Expected float.')\n"
                f"            return None\n"
                f"\n"
                f"        try:\n"
                f"            # Do pseud-complex work\n"
                f"        except Exception as e:\n"
                "            logger.warning(f'Caught exception during computation: {e}')\n"
                f"```\n"
            }
        ],
        temperature=0.8
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to save the generated component as a Python file
def save_component_to_file(component_code, class_name):
    # If the file begins with "```python", remove it
    if component_code.startswith("```python"):
        component_code = component_code[len("```python"):].strip()

    # If the file ends with "```", remove it
    if component_code.endswith("```"):
        component_code = component_code[:-len("```")].strip()

    file_name = f"./gadgets/{class_name}.py"
    with open(file_name, 'w') as file:
        file.write(component_code)

    logger.info(f"Generated new Gadget component and saved it to {file_name}")
    return file_name


# Function to run pytest and handle the results
def run_tests_and_handle_result(file_name):
    try:
        logger.info(f"Running tests for '{file_name}'...")

        # Only allow the tests to run for a maximum of 10 seconds
        result = subprocess.run(['pytest', '--timeout=240'], capture_output=True, text=True)
        if result.returncode == 0:
            # Tests passed, generate an obscure git commit message
            commit_message = generate_creative_commit_message()
            logger.info(f"Tests passed.")
            logger.info(f"Commit message: {commit_message}")

            # Ask the user if they want to stage, commit, and push
            # user_response = input(f"Do you want to stage, commit, and push '{file_name}'? (y/n): ").strip().lower()

            # if user_response == 'y':

            # Stage the new file
            subprocess.run(['git', 'add', file_name])

            # Commit the new file with the generated commit message
            subprocess.run(['git', 'commit', '-m', commit_message])

            # Push the commit to the origin
            subprocess.run(['git', 'push', 'origin', 'HEAD'])

            logger.info(f"File '{file_name}' committed and pushed to origin.")
        else:
            # Tests failed, delete the generated file
            os.remove(file_name)
            logger.error(f"Tests failed. {file_name} has been deleted.")
    except Exception as e:
        # If the error is "[WinError 2] The system cannot find the file specified", ignore it.
        if "[WinError 2]" in str(e):
            logger.error(f"Error while running tests: {str(e)}")
            return
        
        os.remove(file_name)
        logger.error(f"{file_name} has been deleted due to test failure.")


# Function to generate a creative git commit message using OpenAI API
def generate_creative_commit_message():
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You generate valid git commit messages."},
            {"role": "user", "content":
                f"Generate a highly creative and obscure git commit message for a project that deals with random, "
                f"useless components and over-engineered processes. Make the message sound highly technical (pseudo-scientific or science-fiction). "
                f"The message should seem valid and not overtly state that it is meaningless, but does not need to have a real maning. "
                f"This commit message shall not exceed 60 characters."
                f"Examples of commit messages include: `Optimized data structures`, `Refactored neural network architecture`, `Recursive cryptographic ledger for inter-component state.`"
            }
        ],
        max_tokens=350,
        temperature=0.9
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    # Scan the existing components to find input/output imbalances
    input_count, output_count = scan_existing_components()

    # Check for any significant imbalances
    imbalance = find_type_imbalance(input_count, output_count)

    if imbalance:
        logger.warning(f"Input/output type imbalance detected: {imbalance}")

    input_type, output_type = get_input_and_output_types(imbalance if imbalance else None)

    class_name = generate_hex_class_name()

    # Randomly select the type of component to generate
    component_code = None
    random_number = random.randint(1, 2)
    if random_number == 1:
        # Generate a useless component
        component_code = generate_useless_component(class_name, input_type, output_type)
    else:
        # Generate a useful component
        component_code = generate_useleful_component(class_name, input_type, output_type)

    file_name = save_component_to_file(component_code, class_name)

    # Run pytest and handle the result
    run_tests_and_handle_result(file_name)
