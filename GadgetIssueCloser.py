import logging
import coloredlogs
import requests
import json
import random

# Configure colored logging
coloredlogs.install(level='DEBUG')
logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Read the GitHub token from an external file
def read_github_token(filename="github_token.txt"):
    with open(filename, 'r') as file:
        return file.read().strip()

# Function to get a list of open issues from a GitHub repository
def get_open_github_issues(repo, token):
    url = f"https://api.github.com/repos/{repo}/issues?state=open"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issues = response.json()
        if issues:
            return issues
        else:
            logger.info(f"No open issues found in the repository {repo}.")
            return []
    else:
        logger.error(f"Failed to retrieve open issues: {response.status_code} {response.text}")
        return []

# Function to close a GitHub issue by issue number
def close_github_issue(repo, issue_number, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue_data = {
        "state": "closed"
    }

    response = requests.patch(url, headers=headers, data=json.dumps(issue_data))

    if response.status_code == 200:
        logger.info(f"Issue #{issue_number} closed successfully.")
    else:
        logger.error(f"Failed to close issue #{issue_number}: {response.status_code} {response.text}")

# Function to randomly close an open GitHub issue
def close_random_github_issue(repo, token):
    logger.info(f"Fetching open issues from repository {repo}...")

    issues = get_open_github_issues(repo, token)

    if issues:
        issue = random.choice(issues)  # Select a random issue
        issue_number = issue['number']
        issue_title = issue['title']

        logger.info(f"Randomly selected issue #{issue_number}: {issue_title}")

        close_github_issue(repo, issue_number, token)
    else:
        logger.info("No open issues to close.")

if __name__ == "__main__":
    # Repository information
    repo = "DigitalInBlue/gadget"  # Replace with the actual repository name

    # Read GitHub token
    token = read_github_token()

    # Close a random GitHub issue
    close_random_github_issue(repo, token)
