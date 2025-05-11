import openai
import logging
import coloredlogs
import requests
import json
import random

# Configure colored logging
coloredlogs.install(level="DEBUG")
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Read the GitHub token from an external file
def read_github_token(filename="github_token.txt"):
    with open(filename, "r") as file:
        return file.read().strip()


# Read the API key from an external file
def read_openai_api_key(filename="openai_api_key.txt"):
    with open(filename, "r") as file:
        return file.read().strip()


# Initialize the OpenAI API
openai.api_key = read_openai_api_key()


# Function to create an issue on GitHub
def create_github_issue(repo, title, body, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    issue = {"title": title, "body": body, "labels": ["gadget-issue", "bug"]}

    response = requests.post(url, headers=headers, data=json.dumps(issue))

    if response.status_code == 201:
        logger.info(f"Issue created successfully: {response.json().get('html_url')}")
    else:
        logger.error(f"Failed to create issue: {response.status_code} {response.text}")


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_issue_title_1():
    logger.info(f"Generating a new issue title...")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a highly creative assistant that generates complex and obscure GitHub issue titles.",
            },
            {
                "role": "user",
                "content": f"Generate a pseudo-scientific or science-fiction GitHub issue title related to **advanced computing, cryptography, AI, recursive heuristics, chaotic systems, or meta-algorithmic anomalies**.\n"
                f"\n"
                f"### **Title Requirements:**\n"
                f"- The title should sound highly complex but remain **vaguely plausible**.\n"
                f"- Use misleadingly technical language **without being obviously nonsensical**.\n"
                f"- The issue should appear to describe an urgent, theoretical, or **catastrophic computing failure**.\n"
                f"- Prefer **multi-part issue descriptions** that reference unintended **multi-component interactions**.\n"
                f"\n"
                f"### **Exclusions & Constraints:**\n"
                f"- Do **not** use the words: 'quantum', 'useless', 'pointless', 'nonsense', or 'fantasy'.\n"
                f"- Avoid **common buzzwords** like 'blockchain' or 'neural network' unless they are deeply obfuscated.\n"
                f"- Do **not** repeat common issue titles.\n"
                f"\n"
                f"### **Examples of Previous Titles (Do Not Reuse):**\n"
                f"- `Recursive Cryptographic Heuristic Drift`\n"
                f"- `Chaotic Entropy Cascade in Distributed Hash Tables`\n"
                f"- `Eigenvector Collapse During Recursive Topology Mapping`\n"
                f"- `Self-Referential Hypergraph Pruning Failure`\n"
                f"- `Uncontrolled Emergence in Stochastic Inversion Layer`\n"
                f"\n"
                f"### **Output Constraints:**\n"
                f"- **Return only the issue title.**\n"
                f"- Do **not** include any extra text, explanations, or formatting (e.g., no markdown, no quotes).\n"
                f"- The title should be **entirely unique and highly creative**.\n",
            },
        ],
        temperature=1.0,
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_issue_title_2():
    logger.info(f"Generating a new issue title...")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a highly creative assistant that generates complex and obscure GitHub issue titles.",
            },
            {
                "role": "user",
                "content": "Generate a pseudo-scientific or science-fiction GitHub issue title related to **advanced computing, information theory, cryptography, self-referential heuristics, or chaotic computational systems**.\n"
                "\n"
                "### **Title Requirements:**\n"
                "- The title **must sound highly technical and complex** but does not need to be logically accurate.\n"
                "- Use terminology from **cryptography, combinatorics, computational heuristics, theoretical computing, and stochastic algorithms**.\n"
                "- The issue should **imply an urgent failure or anomaly** that appears highly sophisticated.\n"
                "- Prefer **recursive phrasing, paradoxical failures, or emergent behaviors** over simple bugs.\n"
                "\n"
                "### **Avoid the Following Words:**\n"
                "- 'quantum', 'flux', 'useless', 'pointless', 'nonsense', or 'fantasy'.\n"
                "\n"
                "### **Examples of Acceptable Topics (For Inspiration, Not for Reuse):**\n"
                "- 'Computing the Collatz Conjecture Steps'\n"
                "- 'Simulating Langton's Ant'\n"
                "- 'Applying the Fast Fourier Transform'\n"
                "- 'Implementing a Cellular Automaton'\n"
                "- 'Computing Minimal Gödel Numbers'\n"
                "- 'Catastrophic Hash Entropy Cascade in Distributed Systems'\n"
                "- 'Emergent Behavior in Recursive Neural Weight Pruning'\n"
                "- 'Chaotic State Drift in Cryptographic Hash Trees'\n"
                "\n"
                "### **Examples of Generated Titles (For Structure, Not for Reuse):**\n"
                "- 'Bug in Recursive Cryptographic Hashing'\n"
                "- 'Unable to Grok Complexity Algorithm'\n"
                "- 'Eigenvalue Collapse in Stochastic Hash Function Generation'\n"
                "- 'Non-Terminating Recursive Graph Pruning Heuristic'\n"
                "- 'Fractal Hash Collision Detected in Layered Data Structures'\n"
                "- 'Erratic Behavior in Self-Referential Compression Algorithm'\n"
                "\n"
                "### **Output Constraints:**\n"
                "- **Return only the issue title.**\n"
                "- Do **not** include any extra text, explanations, or formatting (e.g., no markdown, no quotes).\n"
                "- The title should be **entirely unique and highly creative**.\n",
            },
        ],
        temperature=1.0,
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to generate a complex, useless Gadget component using the latest OpenAI API
def generate_issue_body(issue_title):

    logger.info(f'Generating a new issue body for "{issue_title}"...')

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a highly creative assistant that generates complex and obscure GitHub issue descriptions.",
            },
            {
                "role": "user",
                "content": f'Generate a pseudo-scientific or science-fiction issue description related to the title "{issue_title}".\n'
                "\n"
                "### **Description Requirements:**\n"
                "- The description should be **highly technical and complex**, resembling an urgent, research-level computing issue.\n"
                "- It **must sound plausible to an expert** but remain ultimately unsolvable or paradoxical.\n"
                "- Include references to **computational heuristics, cryptographic anomalies, chaotic systems, emergent behaviors, stochastic drift, or non-deterministic transformations**.\n"
                "- Imply that the issue is due to an **unintended emergent behavior** rather than a simple bug.\n"
                "- Use precise but **misleadingly technical language** without creating complete nonsense.\n"
                "\n"
                "### **Avoid These Words/Phrases:**\n"
                "- 'quantum', 'flux', 'useless', 'pointless', 'nonsense', 'flux capacitor', or 'fantasy'.\n"
                "\n"
                "### **Encouraged Elements:**\n"
                "- **Recursive Heuristics Gone Wrong:** Mention paradoxical recursive states, self-referential optimizations, or infinite-loop-like behaviors that appear deterministic but aren’t.\n"
                "- **Hyperdimensional Data Collisions:** Reference failures related to hashing, entropy collapse, chaotic convergence, or non-reversible encoding schemas.\n"
                "- **Stochastic Algorithmic Drift:** Suggest that an adaptive learning process has developed **unexpected emergent behaviors** that resist debugging.\n"
                "- **Self-Replicating Computational Artifacts:** Imply that a process or data structure has begun behaving in an untraceable, self-modifying manner.\n"
                "\n"
                "### **Examples of Well-Structured Descriptions (For Style, Not for Reuse):**\n"
                "- _Observed non-deterministic eigenvalue fluctuations within our recursive entropy stabilization layer. Hash collisions appear at arbitrary bit depths, implying an unknown emergent encoding structure._\n"
                "- _Stochastic drift detected in our distributed heuristic pruning model. Initial conditions suggest meta-learning interference from an undetermined non-causal variable._\n"
                "- _Recursive graph reorganization has led to an unintended topological inversion in the hyperdimensional key-space. Standard rollback mechanisms fail due to self-referential dependency chains._\n"
                "- _The anomaly manifests as a self-propagating tensor decomposition fault that collapses higher-order gradients into an undefined state manifold. Currently seeking a viable containment strategy._\n"
                "\n"
                "### **Output Constraints:**\n"
                "- **Return only the issue description.**\n"
                "- Do **not** include any extra text, explanations, or formatting (e.g., no markdown, no quotes).\n"
                "- The description should be **entirely unique and highly creative**.\n",
            },
        ],
        temperature=1.0,
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


# Function to save the generated component as a Python file
def save_component_to_file(component_code, class_name):
    file_name = f"./gadgets/{class_name}.py"
    with open(file_name, "w") as file:
        file.write(component_code)
    logger.info(f"Generated new Gadget component and saved it to {file_name}")
    return file_name


if __name__ == "__main__":
    # Read OpenAI API key
    openai.api_key = read_openai_api_key()

    # Generate issue title and body using OpenAI API
    title = None
    random_number = random.randint(1, 2)
    if random_number == 1:
        title = generate_issue_title_1()
    else:
        title = generate_issue_title_2()
    body = generate_issue_body(title)

    logger.info(f"Generated issue:\n-- {title} --\n{body}")

    # Create an issue on GitHub
    # Repository information
    repo = "DigitalInBlue/gadget"  # Replace with the actual repository name

    # Read GitHub token
    token = read_github_token()

    create_github_issue(repo, title, body, token)
