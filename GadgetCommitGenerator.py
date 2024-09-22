import openai
import logging
import coloredlogs

# Configure colored logging
coloredlogs.install(level='DEBUG')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Read the GitHub token from an external file
def read_github_token(filename="github_token.txt"):
    with open(filename, 'r') as file:
        return file.read().strip()


# Read the API key from an external file
def read_openai_api_key(filename="openai_api_key.txt"):
    with open(filename, 'r') as file:
        return file.read().strip()


# Initialize the OpenAI API
openai.api_key = read_openai_api_key()


# Function to generate a complex, useless Gadget commit message using the latest OpenAI API
def generate_commit_message():

    logger.info(f"Generating a new issue title...")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes GitHub commit messages."},
            {"role": "user", "content":
                f"Generate a pseudo-scientific commit message related to advanced computing, cryptography, blockchain, quantum computing, or some other scientific-related computing topic. "
                f"The message should scientific and complex, but not mean much."
                f"Return only the commit message.  Do not include any other text or information. Do not wrap the text in any way. "
                f"The message must be limited to 70 characters or less."
                f"Don't use words such as 'useless', 'pointless', 'nonsense', or 'fantasy'."
                f"Examples of messages include: `Harmonized stochastic flux algorithms for entropic widgets`"
            }
        ],
        temperature=0.9
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    # Read OpenAI API key
    openai.api_key = read_openai_api_key()

    # Generate issue commit message using OpenAI API
    msg = generate_commit_message()

    logger.info(f"Generated commit message:\n-- {msg} --\n")
