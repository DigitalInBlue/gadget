import openai
import os
import random
from GadgetComponent import GadgetComponent
import logging
import subprocess
import coloredlogs

# Configure colored logging
coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Valid input/output types for components
VALID_TYPES = ["int", "float", "str", "bool", "Image.Image", "dict"]


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


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_useless_component(class_name=None):
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
                f"The 'run' function should include useless work such as nested loops, pointless calculations, and irrelevant data transformations, and should use the logger to show work done. "
                f"The 'run' function should take a single input parameter called 'input_data' with type annotation, for example: `def run(self, input_data: int) -> str`"
                f"The 'run' function should validate its input type, for example: `def run(self, input_data: int) -> str: if not isinstance(input_data, int): self.logger.error(f'Invalid input type: Expected int.') return None`"
                f"The 'run' function can perform more than one task, such as computing a cellular automata, an obscure algorithm, or complex transformations. Be highly creative."
                f"Neither the 'run' function nor the description should overtly state that it is useless work.  What it does should be obscure, but nonsense or fantasy."
                f"Be highly creative and make the component as complex as possible. "
                f"Don't use words such as 'useless', 'pointless', 'nonsense', or 'fantasy'. The component should seem valid and useful, but ultimately meaningless. "
                f"Ensure that the logger is imported and instantiated globally using 'import logging' and 'logger = logging.getLogger(__name__)'. "
                f"The 'get_name' function should return a pseudo-scientific name with multiple words separated by spaces. "
                f"Return only the python code for the class.  Do not include any other text or information. Do not wrap the code in '```python' or similar. "
                f"Follow PEP-8 guidelines for code style and formatting. "
                f"Examples of names include: `Numerical Symbolic Disassociation Engine`, `Cognitive String Truth Evaluator`"
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
        temperature=0.9
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to save the generated component as a Python file
def save_component_to_file(component_code, class_name):
    file_name = f"./gadgets/{class_name}.py"
    with open(file_name, 'w') as file:
        file.write(component_code)
    logger.info(f"Generated new Gadget component and saved it to {file_name}")
    return file_name


# Function to run pytest and handle the results
def run_tests_and_handle_result(file_name):
    try:
        result = subprocess.run(['pytest'], capture_output=True, text=True)
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
        logger.error(f"Error while running tests: {str(e)}")
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
                f"useless components and over-engineered processes. Make the message sound highly technical (pseudo-scientific) but ultimately "
                f"meaningless.  The message should seem valid and not overtly state that it is meaningless, but does not need to have a real maning. "
                f"This commit message shall not exceed 60 characters."
                f"Examples of commit messages include: `Optimized quantum data structures`, `Refactored neural network architecture`, `Recursive cryptographic ledger for inter-component state.`"
            }
        ],
        max_tokens=350,
        temperature=0.9
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    class_name = generate_hex_class_name()
    component_code = generate_useless_component(class_name)
    file_name = save_component_to_file(component_code, class_name)

    # Run pytest and handle the result
    run_tests_and_handle_result(file_name)
