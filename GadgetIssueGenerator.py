import openai
import logging
import subprocess
import coloredlogs
import requests
import json

# Configure colored logging
coloredlogs.install()
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


# Function to create an issue on GitHub
def create_github_issue(repo, title, body, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue = {
        "title": title,
        "body": body,
        "labels": ["gadget-issue", "bug"]
    }

    response = requests.post(url, headers=headers, data=json.dumps(issue))

    if response.status_code == 201:
        logger.info(f"Issue created successfully: {response.json().get('html_url')}")
    else:
        logger.error(f"Failed to create issue: {response.status_code} {response.text}")


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_issue_title():

    logger.info(f"Generating a new issue title...")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes GitHub issues."},
            {"role": "user", "content":
                f"Generate a pseudo-scientific issue title related to advanced computing, cryptography, blockchain, or quantum computing. The title should sound highly complex and not mean much."
                f"Return only the issue title.  Do not include any other text or information. Do not wrap the text in any way. "
                f"Examples of titles include: `Quantum Blockchain Inconsistency in Recursive Cryptographic Hashing`"
            }
        ],
        temperature=0.9
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_issue_body(issue_title):

    logger.info(f"Generating a new issue body for \"{issue_title}\"...")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes GitHub issues."},
            {"role": "user", "content":
                f"Generate a pseudo-scientific issue description related to the title \"{issue_title}\". "
                f"The description should be complex, technical-sounding, but not necessarily meaningful. "
                f"Return only the detailed issue text.  Do not include any other text or information. Do not wrap the text in any way. "
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


if __name__ == "__main__":
    # Read OpenAI API key
    openai.api_key = read_openai_api_key()

    # Generate issue title and body using OpenAI API
    title = generate_issue_title()
    body = generate_issue_body(title)

    logger.info(f"Generated issue:\n-- {title} --\n{body}")

    # Create an issue on GitHub
    # Ask the user if they want to push the generated issue to GitHub
    user_response = input(f"Do you want to create a GitHub issue with the title '{title}'? (y/n): ").strip().lower()
    if user_response == 'y':
        # Repository information
        repo = "DigitalInBlue/gadget"  # Replace with the actual repository name

        # Read GitHub token
        token = read_github_token()

        create_github_issue(repo, title, body, token)
    else:
        logger.info("Issue was not created.")

