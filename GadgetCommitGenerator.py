import openai
import logging
import coloredlogs

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


# Function to generate a complex, useless Gadget commit message using the latest OpenAI API
def generate_commit_message():

    logger.info(f"Generating a new issue title...")

    # Use the new "chat.completions" API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a highly creative assistant that generates pseudo-scientific Git commit messages.",
            },
            {
                "role": "user",
                "content": "Generate a pseudo-scientific commit message related to **advanced computing, cryptography, AI heuristics, chaotic data structures, emergent computation, or recursive meta-algorithms.**\n"
                "\n"
                "### **Commit Message Requirements:**\n"
                "- The message should be **scientific and complex** but ultimately lack clear meaning.\n"
                "- It must **imply a highly technical change** while remaining obscure.\n"
                "- The message must be **70 characters or less**.\n"
                "- Avoid **common buzzwords** and focus on unexpected technical phrasing.\n"
                "\n"
                "### **Prohibited Words & Phrases:**\n"
                "- Do not use: 'quantum', 'flux', 'useless', 'pointless', 'nonsense', 'harmonized', 'hyperbolic', 'flux capacitor'.\n"
                "\n"
                "### **Encouraged Topics:**\n"
                "- **Chaotic Cryptographic Drift** → Vaguely references unstable encryption heuristics.\n"
                "- **Meta-Algorithmic Optimization** → Implication of complex but undefined efficiency gains.\n"
                "- **Recursive Heuristic Augmentation** → Describes an improvement to an emergent, self-referential process.\n"
                "- **Non-Deterministic Convergence Issues** → Vaguely references irreproducible AI behavior.\n"
                "\n"
                "### **Examples of Good Commit Messages (For Style, Not for Reuse):**\n"
                "- `Stochastic state mutation in cryptographic keystream synthesis`\n"
                "- `Recalibrated heuristic weighting for unstable entropy cascade`\n"
                "- `Reconfigured topological pruning for recursive cipher trees`\n"
                "- `Chaotic bifurcation detected in stochastic inversion model`\n"
                "- `Optimized eigenvalue folding in asymmetric data embeddings`\n"
                "\n"
                "### **Output Constraints:**\n"
                "- **Return only the commit message.**\n"
                "- Do **not** include any extra text, explanations, or formatting (e.g., no markdown, no quotes).\n"
                "- The commit message must be **entirely unique and highly creative**.\n",
            },
        ],
        temperature=1.0,
    )

    # Extract the generated class code from the response
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    # Read OpenAI API key
    openai.api_key = read_openai_api_key()

    # Generate issue commit message using OpenAI API
    msg = generate_commit_message()

    logger.info(f"Generated commit message:\n-- {msg} --\n")
